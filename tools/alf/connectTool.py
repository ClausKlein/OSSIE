## Copyright 2005, 2006, 2007, 2008 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE ALF Waveform Application Visualization Environment
##
## ALF is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## ALF is distributed in the hope that it will be useful, but WITHOUT ANY
## WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE Waveform Developer; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import wx

from omniORB import CORBA      # use this for the CORBA orb stuff 
                               # (pushing packets)
import sys       # for system commands (e.g., argv and argc stuff)
import CosNaming   # narrowing naming context stuff

try:   #mac / older OSSIE versions
    import standardInterfaces__POA
    import CF, CF__POA    # core framework stuff
except ImportError:   #0.6.2
    import ossie.standardinterfaces.standardInterfaces__POA as standardInterfaces__POA
    import ossie.cf.CF as CF
    import ossie.cf.CF__POA as CF__POA    

from wx.lib.anchors import LayoutAnchors  # used by splitter window

import loadAutomationFile

def create(parent):
    ''' returns a wx frame representing the connect tool'''
    return MainFrame(parent, -1)



def errorMsg(self,msg):
    ''' Brings up a wx error message that says msg (first argument)'''
    dlg = wx.MessageDialog(self,msg,'Error', wx.OK | wx.ICON_INFORMATION)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    return



class MainFrame(wx.Frame):
    ''' The main window where all of the connect tool's wx stuff resides'''

    def __init__(self, parent, id):
        self.alfFrameRef = parent

        self._init_CORBA()     # will get me an orb and a reference to the Domain Manager   
        
        self._init_ctrls(self.alfFrameRef)   # initialize the wx stuff
       
        if __name__ != '__main__':      # this statement allows me to run the tool
                                        # as a standalone without OSSIE to do 
                                        # design work
         self.getAvailableConnections()    
         self.setAvailableApplications()

        self.uPortNameEditor.write('(uses port name)')
        self.pPortNameEditor.write('(provides port name)')

        # This argument sets a default value for the automations file
        #self.automationFileEditor.write('/sdr/automation_files/AM_FM_router.xml')
        self.automationFileEditor.write('automationFileExamples')

        self.parent = parent

        if False:        
         # Now Create the menu bar and items
         self.mainmenu = wx.MenuBar()

         menu = wx.Menu()
         menu.Append(205, 'E&xit', 'Enough of this already!')
         self.Bind(wx.EVT_MENU, self.OnFileExit, id=205)
         self.mainmenu.Append(menu, '&File')
        
         menu = wx.Menu()
         menu.Append(300, '&About', 'About this thing...')
         self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=300)
         self.mainmenu.Append(menu, '&Help')

         self.SetMenuBar(self.mainmenu)

         # Bind the close event so we can disconnect the ports
         self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Show(True)
        

    def _init_CORBA(self):
        """Initialize an orb and try to connect to the DomainManager"""

        self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        self.obj = self.orb.resolve_initial_references("NameService")
        try:
            self.rootContext = self.obj._narrow(CosNaming.NamingContext)
        except:
            ts = "Failed to narrow the root naming context.\n"
            ts += "Are the Naming Service and nodeBooter running?"
            print ts
            self.rootContext = None
            self.domMgr = None
            return
        
        if self.rootContext is None:
            print "Failed to narrow the root naming context"
            self.domMgr = None
            return

        name = [CosNaming.NameComponent("DomainName1",""),
            CosNaming.NameComponent("DomainManager","")]
            
        try:
            self.obj = self.rootContext.resolve(name)
        except:
            print "DomainManger name not found"
            self.domMgr = None
            return

        self.domMgr = self.obj._narrow(CF.DomainManager)
	
        self.domain = "DomainName1"



    def _init_ctrls(self, prnt):
        ''' Initialize the wx controls'''

        frame_size = wx.Size(770, 350)

        wx.Frame.__init__(self, id=-1, name='', parent=prnt,
                          pos=wx.Point(10, 20), size=frame_size,
                          style=wx.DEFAULT_FRAME_STYLE, 
                          title='Connection Tool')


        panel = wx.Panel(self, -1)


        # --------------------------------------------------------------------
        # create the top sizer
        # Uses editors:
        self.uPortNameEditor = wx.TextCtrl(id=-1,
                                        name=u'uPortNameEditor', 
                                        size=wx.Size(250, 30), 
                                        parent=panel, 
                                        style=0, value=u'')
        self.pPortNameEditor = wx.TextCtrl(id=-1,
                                        name=u'pPortNameEditor', 
                                        parent=panel, 
                                        size=wx.Size(250, 30), 
                                        style=0, value=u'')


        # Static Texts (labels)
        self.blankLabel  = wx.StaticText(id=-1, label='',
                                        name='blankLabel', parent=panel, 
                                        size=wx.Size(150, 30), style=0)
        #self.blankLabel2  = wx.StaticText(id=-1, label='',
        #                                name='blankLabel2', parent=panel, 
        #                                size=wx.Size(150, 30), 
        #                                style=wx.ALIGN_RIGHT)
        self.appLabel  = wx.StaticText(id=-1, label='Application: ',
                                        name='appLabel', parent=panel, 
                                        size=wx.Size(150, 30), 
                                        style=wx.ALIGN_RIGHT)
        self.compLabel = wx.StaticText(id=-1, label='Component: ',
                                        name='compLabel', parent=panel, 
                                        size=wx.Size(150, 30), 
                                        style=wx.ALIGN_RIGHT)
        self.portLabel = wx.StaticText(id=-1, label='Port:',
                                        name='portLabel', parent=panel, 
                                        size=wx.Size(150, 30), 
                                        style=wx.ALIGN_RIGHT)
        self.usesLabel = wx.StaticText(id=-1, label='Uses Port:',
                                        name='usesLabel', parent=panel, 
                                        size=wx.Size(250, 30), 
                                        style=wx.ALIGN_CENTER)
        self.providesLabel = wx.StaticText(id=-1, label='Provides Port:',
                                        name='providesLabel', parent=panel, 
                                        size=wx.Size(250, 30), 
                                        style = wx.ALIGN_CENTER)
        
        # wx choices
        # application choices
        self.uAppChoice = wx.Choice(choices=[' '], id=-1,
                                    name=u'uAppChoice', 
                                    parent=panel,
                                    size=wx.Size(250, 30), style=0)
        self.uAppChoice.Bind(wx.EVT_CHOICE, self.OnUAppSelection, id =-1)

        self.pAppChoice = wx.Choice(choices=[' '], id=-1,
                                    name=u'pAppChoice', 
                                    parent=panel,
                                    size=wx.Size(250, 30), style=0)
        self.pAppChoice.Bind(wx.EVT_CHOICE, self.OnPAppSelection, id =-1)

        # component choices
        self.uCompChoice = wx.Choice(choices=[' '], id=-1,
                                    name=u'uCompChoice', 
                                    parent=panel,
                                    size=wx.Size(250, 30), style=0)
        self.pCompChoice = wx.Choice(choices=[' '], id=-1,
                                    name=u'pCompChoice', 
                                    parent=panel,
                                    size=wx.Size(250, 30), style=0)


        #  port choices
        #self.uPortChoice = wx.Choice(choices=[' '], id=-1,
        #                            name=u'uPortChoice', 
        #                            parent=panel,
        #                            size=wx.Size(250, 30), style=0)
        #self.pPortChoice = wx.Choice(choices=[' '], id=-1,
        #                            name=u'pPortChoice', 
        #                            parent=panel,
        #                            size=wx.Size(250, 30), style=0)


        # connect button
        self.ConnectBtn = wx.Button(id = -1, label='Connect',
                                    parent=panel, 
                                    size=wx.Size(145, 50))
        self.ConnectBtn.Bind(wx.EVT_BUTTON, self.OnConnectBtn, id=-1)
        blankLabel3 = wx.StaticText(label = '', parent = panel)
        blankLabel4 = wx.StaticText(label = '', parent = panel)


        flexSizer1 = wx.FlexGridSizer(cols=3, hgap=6, vgap = 6)
        flexSizer1.AddMany([self.blankLabel, self.usesLabel, self.providesLabel, 
                  self.appLabel, self.uAppChoice, self.pAppChoice, 
                  self.compLabel, self.uCompChoice, self.pCompChoice,
                  # self.portLabel, self.uPortChoice, self.pPortChoice,
                  self.portLabel, self.uPortNameEditor, self.pPortNameEditor,
                  blankLabel3, self.ConnectBtn, blankLabel4])
        # --------------------------------------------------------------------

        
        # --------------------------------------------------------------------
        # second sizer
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.automationFileEditor = wx.TextCtrl(id=-1,
                                        name=u'automationFileEditor', 
                                        parent=panel, 
                                        size=wx.Size(250, 30), 
                                        style=0, value=u'')
        self.loadAutomationBtn = wx.Button(id = -1, 
                                           label='Load Automation File',
                                    parent=panel, 
                                    size=wx.Size(210, 50))
        self.loadAutomationBtn.Bind(wx.EVT_BUTTON, 
                                    self.onLoadAutomationFileButton,
                                    id=-1)
        hSizer1.Add(self.automationFileEditor, 0, wx.ALL, 5)
        hSizer1.Add(self.loadAutomationBtn, 0, wx.ALL, 5)
        # --------------------------------------------------------------------



        # --------------------------------------------------------------------
        # assemble main sizer from other sizers

        # topLabel = wx.StaticText(label = 'Connect Tool.  OSSIE 0.6.2', 
        #                         parent = panel)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # mainSizer.Add(topLabel, 0 , wx.ALL, 5)
        # mainSizer.Add(wx.StaticLine(panel), 0 , wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        mainSizer.Add(flexSizer1, 0 , wx.EXPAND|wx.ALL, 10)

        mainSizer.Add(wx.StaticLine(panel), 0 , wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        mainSizer.Add(hSizer1, 0, wx.EXPAND|wx.ALL, 10)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        # --------------------------------------------------------------------
        


    def getAvailableConnections(self):
        ''' Get a list of objects I can potentially connect to'''

        # Set the application selection to an instruction:
        #self.uAppChoice.Clear()
        #self.uAppChoice.Append('(Select Uese Waveform)')
        #self.pAppChoice.Clear()
        #self.pAppChoice.Append('(Select Provides Waveform)')
        
        # Initialize my dictionary 
        self.avail_connects = {}

        dom_obj = self.alfFrameRef.rootContext.resolve(
                            [CosNaming.NameComponent("DomainName1","")])
        dom_context = dom_obj._narrow(CosNaming.NamingContext) 
        if dom_context is None:
            return

        # get a list of applications running in the domain
        appSeq =  self.alfFrameRef.domMgr._get_applications()
        members = dom_context.list(1000) 
        for m in members[0]:
            wav_name = str(m.binding_name[0].id)
            wav_obj = dom_context.resolve(
                                [CosNaming.NameComponent(wav_name,"")])
            wav_context = wav_obj._narrow(CosNaming.NamingContext)
            if wav_context is None:
                continue

            contextApp = None
            foundApp = False
            for app in appSeq:
                compNameCon = app._get_componentNamingContexts()
              

                for compElementType in  compNameCon:
                    if wav_name in compElementType.elementId:
                        comp_name = compElementType.elementId.split("/")
                        comp_name = comp_name[2]
 
                        if self.avail_connects.has_key(wav_name):
                            self.avail_connects[wav_name].append(comp_name)
                        else:
                            self.avail_connects[wav_name] = [comp_name]
                        waveformApp = app
                        foundApp = True

            if not foundApp:
                print "Could not find associated application for: " + wav_name
                continue


    def setAvailableApplications(self):
        ''' Assumes that I have a list of available applications.  Sets the
            application wx.choice to list "choose waveform" followed by 
            a list of the available applications'''

        # Set the application selection to an instruction:
        self.uAppChoice.Clear(); self.uAppChoice.Append("(Choose Application)")
        self.pAppChoice.Clear(); self.pAppChoice.Append("(Choose Application)")
         
        # add all of the available waveforms to my wx.choice
        for w in self.avail_connects.keys():
            self.uAppChoice.Append(w)
            self.pAppChoice.Append(w)

        # Set the choice to display 0th choice "(Choose Application)"
        self.uAppChoice.SetSelection(0)
        self.pAppChoice.SetSelection(0) 

    def OnPAppSelection(self, event):
        ''' Should occur when the user has selected a provides application.
            Adds a list of the available components in the selected application
            to the wx.choice for provides components.'''

        choice = str(self.pAppChoice.GetStringSelection())
        self.pCompChoice.Clear()
        self.pCompChoice.Append('(Choose Component)')
        for c in self.avail_connects[choice]:
            self.pCompChoice.Append(c)
        self.pCompChoice.SetSelection(0)
        event.Skip()
    
    def OnUAppSelection(self,event):
        ''' Should occur when the user has selected a uses application.
            Adds a list of the available components in the selected application
            to the wx.choice for uses components.'''

        choice = str(self.uAppChoice.GetStringSelection())
        self.uCompChoice.Clear()
        self.uCompChoice.Append('(Choose Component)')
        for c in self.avail_connects[choice]:
            self.uCompChoice.Append(c)
        self.uCompChoice.SetSelection(0)
        event.Skip()



    def OnConnectBtn(self,event):
        ''' This is what happens when you press the connect button.
            Retrieves the selected apps, components, and ports.
            Then calls connect method.'''

        pPortName = str(self.pPortNameEditor.GetLineText(0))
        uPortName = str(self.uPortNameEditor.GetLineText(0))

        uAppInstName = str(self.uAppChoice.GetStringSelection())
        pAppInstName = str(self.pAppChoice.GetStringSelection())
        uCompInstName = str(self.uCompChoice.GetStringSelection())
        pCompInstName = str(self.pCompChoice.GetStringSelection())

        self.Connect( uAppInstName, uCompInstName, uPortName,
                      pAppInstName, pCompInstName, pPortName)
       
        event.Skip()


    def Connect(self, uAppInstName, uCompInstName, uPortName,
                      pAppInstName, pCompInstName, pPortName):
 

        if self.rootContext is None:
            print "Failed to narrow the root naming context"
            sys.exit(1)

        # get a reference to the provides port:
        # don't forget OSSIE:: in waveform name
        pname = [CosNaming.NameComponent(self.domain,''),
                 CosNaming.NameComponent(pAppInstName,''),
                 CosNaming.NameComponent(pCompInstName,'')]
        
        try:
            pResourceRef = self.rootContext.resolve(pname)
        except:
            print "provides resource not found"
            sys.exit(1)
     
        pResourceHandle = pResourceRef._narrow(CF.Resource)
        pPortReference = pResourceHandle.getPort(pPortName)
        

        # get a reference to the uses port:
        # don't forget OSSIE:: in waveform name
        uname = [CosNaming.NameComponent(self.domain,''),
                 CosNaming.NameComponent(uAppInstName,''),
                 CosNaming.NameComponent(uCompInstName,'')]
        try:
            uResourceRef = self.rootContext.resolve(uname)
     
        except:
            print "uses resource not found"
            sys.exit(1)
     
        uResourceHandle = uResourceRef._narrow(CF.Resource)

        # get a reference to the uses port
        uPortReference = uResourceHandle.getPort(uPortName)
        if uPortReference is None:
            print "Failed to get Port reference"
            return
        uPortHandle = uPortReference._narrow(CF.Port)
         

        # connect to the Uses port by passing a ref to my provides port
        # make up some arbitrary connectionid that will be used for 
        # disconnectPort later
        uPortHandle.connectPort(pPortReference,
                                "thisismyconnectionid_" + uPortName)

        # It is important to the the user know that the connection is made
        # otherwise it looks like the connect button is not responding
        print "Connection made successfully."
      

    def onLoadAutomationFileButton(self,event):
        ''' This is what happens when the Load Automation File button is pressed.
            Will get the filename from the GUI and then start up the loadAutomationFile
            modue '''

        # get the name of the file
        automations_file = self.automationFileEditor.GetLineText(0)
        self.automation = loadAutomationFile.automation(self, automations_file)
        event.Skip()

    def pushPacket(self, I , Q):
        ''' Other ports in the Domain can call push packet on me.  I will forward the
            packet to the instance of loadAutomationFile'''
        self.automation.pushPacket(I,Q)


    def pushPacketMetaData(self, I, Q, metadata):
        ''' Other ports in the Domain can call push packet on me.  I will forward the
            packet to the instance of loadAutomationFile'''

        # depeding on how metadata is defined, this method might change !!

        self.automation.pushPacketMetaData(I,Q, metadata)



    # --------------------------------------------------------------
    # Wx details:

    def OnFileExit(self, event):
        ''' This is what will happen when you select File -> Exit 
            in the menu bar'''
        self.Close()      #close the frame
  
    def OnHelpAbout(self, event):
        '''Stuff that gets displayed when you select Help -> About in the menu bar'''
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, "Connection Tool.\nA product of Wireless@VT.\n\nOSSIE 0.6.2.", "About...")
        about.ShowModal()

    def OnCloseWindow(self,event):
        '''This is what happens when you close the GUI'''
        if hasattr(self.parent, 'removeToolFrame'):
            self.parent.removeToolFrame(self)
        self = None
        event.Skip()


class MyApp(wx.App):
    '''for development purposes only'''
    def OnInit(self):
        frame = create(None)
        self.SetTopWindow(frame)
        return True


if __name__ == '__main__':
    '''for development and debugging purposes only'''
    print "WARNING:  Running this tool in the command line is intended for testing new GUI layouts only.  For this tool to function properly, it must be called from ALF"
    app= MyApp(0)
    app.MainLoop()







