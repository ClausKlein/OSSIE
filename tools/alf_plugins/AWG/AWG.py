#!/usr/bin/env python

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

''' This file mostly contians wx GUI code.  To edit signals, see sources.py.
    This tool will get signals from sources.py and send them to the specified 
    provides port. '''

import sources    # within the AWG directory.  This will generate the signals
import wx         # needed for display stuff
from omniORB import CORBA      # use this for the CORBA orb stuff 
                               # (pushing packets)
import sys       # for system commands (e.g., argv and argc stuff)
import CosNaming   # narrowing naming context stuff

try:   # mac/older ossie versions
    import standardInterfaces__POA
    import CF, CF__POA    # core framework stuff
    import profile   # profile provides the same interface as cProfile
                     # cProfile is not available in older versions of Python

except ImportError: # 0.6.2
    import ossie.standardinterfaces.standardInterfaces__POA as standardInterfaces__POA
    import ossie.cf.CF as CF
    import ossie.cf.CF__POA as CF__POA
    import cProfile as profile

from wx.lib.anchors import LayoutAnchors  # used by splitter window
import threading
import time


class AWG:
    '''this class makes the calls to get the actual signal from the 
       sources class'''

    def __init__(self, parent):        
        self.parent = parent

    def get_signal(self, signal_type, file_name):
        self.signal_type = signal_type

        # get length of packet from the gui
        self.signal_len = int(self.parent.packetLenEditor.GetLineText(0))

        # TODO: setup cycles per packet in GUI
        self.frequency = 5   # cycles per packet

        # TODO: setup random data type in GUI
        # TODO: setup random variable variance in GUI
        self.rand_type = 'random'
        self.file_name = file_name
        self.delimiter = ','

        my_signal = sources.sources(self)    # instance of signals class
        self.the_signal = my_signal.gen_signal()

        return self.the_signal              
    

def create(parent,namespace, interface, ns_name, port_name):
    ''' Public.  Returns the wx.Frame for the AWG tool.
        create(parent, namespace, interface, ns_name, port_name)'''
    return MainFrame(parent, -1, '',namespace, interface, ns_name, port_name)

def create_from_other_tool(parent):
    ''' Public.  This allows other tools (e.g., the Connect Tool) to connect 
        to the AWG.
        create_from_other_tool(parent)'''
    namespace = None
    ns_name = None
    port_name = None

    # In OSSIE 0.6.2, only complexShort is supported.  For future
    # versions of OSSIE that could allow for additional data types
    # the "interface" variable should change based on the user input
    # to the GUI
    interface = "complexShort"
    return MainFrame(parent, -1, "", 
                     namespace, interface, ns_name, port_name, "tool")


#generate wx ids for my wx controls
[wxID_MAINFRAME, wxID_SPLITTERWINDOW1, wxID_PUSHPACKETBTN, wxID_ISOURCECHOICE, wxID_IFILENAMEEDITOR, wxID_QSOURCECHOICE, wxID_QFILENAMEEDITOR, wxID_ISOURCESTATICTEXT, wxID_QSOURCESTATICTEXT, wxID_IFILESTATICTEXT,wxID_QFILESTATICTEXT] = [wx.NewId() for _init_ctrls in range(11)]


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title, namespace, interface, 
                 component_name, port_name, connecting_to = "component"):

        self.profile_counter = 0
        self.my_profile = profile.Profile()

        self.numPacks = -1
        
        self.header_count = 0
        self.headers = []
        self.sending_headers = False

        tmp_sources_instance = sources.sources(self)
        self.available_sources = tmp_sources_instance.get_sources_list()

        self.start_event = threading.Event()

        self._init_ctrls(parent)
         
        self.parent = parent
        self.other_tool_ref = parent
        self.namespace = namespace
        self.interface = interface
        self.my_local_controls = None
        self.component_name = component_name
        self.port_name = port_name
        if connecting_to == 'component':
            self.setup_component_connection()
        elif connecting_to == "tool":
            self.setup_tool2tool_connection()
        
        # Now Create the menu bar and items
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(205, 'Exit', 'Enough of this already!')
        self.Bind(wx.EVT_MENU, self._OnFileExit, id=205)
        self.mainmenu.Append(menu, '&File')
        
        menu = wx.Menu()
        menu.Append(300, '&About', 'About this thing...')
        self.Bind(wx.EVT_MENU, self._OnHelpAbout, id=300)
        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

        self.Bind(wx.EVT_CLOSE, self._OnCloseWindow)

        self.Show(True)
        
        self.packetLenEditor.write('1024')

        self.iFileNameEditor.write('i.dat')
        self.qFileNameEditor.write('q.dat')

        #set the default source
        #this way if the user presses the "PushPacket" button before selecting
        #a source, the source that is being displayed will be used
        self.iSourceChoice.SetSelection(0)
        self.qSourceChoice.SetSelection(0)

        self.dataTypeChoice.SetSelection(0)
        self.sendIDChoice.SetSelection(1)  # 1 = No, 0 = Yes
        self.timeUnitsChoice.SetSelection(1)
        
        # start a thread that will recursively send data when the start
        # button is pressed
        self.is_running = True
        self.send_data_thread = threading.Thread(target=self._send_data_loop)
        self.send_data_thread.start()


    def _init_ctrls(self, prnt):
        ''' Private.  Sets up all of the wx controls '''

        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='', parent=prnt,
                          pos=wx.Point(30, 30), size=wx.Size(760, 530),
                          style=wx.DEFAULT_FRAME_STYLE, 
                          title='Arbitrary Waveform Generator')

        panel = wx.Panel(self, -1)

        # First Row
        dataTypeLabel = wx.StaticText(label = 'Data Type', parent = panel)

        self.dataTypeChoice = wx.Choice(choices=['Complex Short'], 
                                         parent=panel, 
                                         size=wx.Size(136, 28))
        placeHolder1 = wx.StaticText(label = '', parent = panel)
        placeHolder2 = wx.StaticText(label = '', parent = panel)

        # Second Row
        packetHeaderLabel = wx.StaticText(label = 'Packet Headers: ', 
                                          parent = panel)
        self.packetHeaderEditor = wx.TextCtrl(parent=panel, 
                                           size=wx.Size(250, 30))
        placeHolder3 = wx.StaticText(label = '', parent = panel)

        # Third Row
        sendPacketIDLabel = wx.StaticText(label = 'Send packet ID', 
                                          parent = panel)
        self.sendIDChoice = wx.Choice(choices=['Yes', 'No'], 
                                         parent=panel, 
                                         size=wx.Size(70, 30))
        placeHolder4 = wx.StaticText(label = '', parent = panel)

        # Fourth Row
        packetLenLabel = wx.StaticText(label = 'Packet Length:', parent = panel)
        self.packetLenEditor = wx.TextCtrl(parent=panel, 
                                           size=wx.Size(250, 30))
        placeHolder5 = wx.StaticText(label = '', parent = panel)

        # Fifth Row
        numPacksLabel = wx.StaticText(label = 'Number of Packets:', 
                                                        parent = panel)
        self.numPacksEditor = wx.TextCtrl(parent=panel, 
                                           size=wx.Size(250, 30))
        placeHolder16 = wx.StaticText(label = '', parent = panel)


        # spacer Row 1
        placeHolder9 = wx.StaticText(label = '', parent = panel)
        placeHolder10 = wx.StaticText(label = '', parent = panel)
        placeHolder11 = wx.StaticText(label = '', parent = panel)


        # 6th Row
        placeHolder6 = wx.StaticText(label = '', parent = panel)
        IChannelLabel = wx.StaticText(label = 'I Channel', parent = panel)
        QChannelLabel = wx.StaticText(label = 'Q Channel', parent = panel)

        # 7th Row
        dataLabel = wx.StaticText(label = 'Data', parent = panel)
        self.iSourceChoice = wx.Choice(choices=self.available_sources.keys(), 
                                       parent=panel, 
                                       size=wx.Size(136, 30))
        self.iSourceChoice.Bind(wx.EVT_CHOICE, self._OnSourceChoiceChoice,
                                id=wxID_ISOURCECHOICE)
        self.qSourceChoice = wx.Choice(choices=self.available_sources.keys(), 
                                       parent = panel, 
                                       size=wx.Size(136, 30))
        self.qSourceChoice.Bind(wx.EVT_CHOICE, self._OnSourceChoiceChoice,
                                id=wxID_QSOURCECHOICE)

        # 8th Row
        fileLabel = wx.StaticText(label = 'File Name', parent = panel)
        self.iFileNameEditor = wx.TextCtrl(parent=panel, size=wx.Size(250, 30))
        self.qFileNameEditor = wx.TextCtrl(parent=panel, size=wx.Size(250, 30))

        # 9th Row
        delayLabel = wx.StaticText(label = 'Delay between packets: ',
                                   parent = panel)
        self.delayEditor = wx.TextCtrl(parent = panel, size = wx.Size(50,30),
                                       value = "500")
        # TODO: make sure this event is binding correctly
        # not working on the mac, but might work on linux
        self.delayEditor.Bind(wx.EVT_TEXT_ENTER, self.onSetDelay)
        self.timeUnitsChoice = wx.Choice(choices=['seconds', 'miliseconds'], 
                                         parent=panel, 
                                         size=wx.Size(136, 30))
        self.timeUnitsChoice.Bind(wx.EVT_CHOICE, self.onSetDelay)


        # 10th Row
        profilingLabel = wx.StaticText(label = "Python Profiling: ", 
                                        parent = panel)
        self.profilingCheckBox = wx.CheckBox(label = "",
                                        parent = panel)
        self.profilingCheckBox.SetValue(False)
        placeHolder15 = wx.StaticText(label = '', parent = panel)


        # spacer row 2     
        placeHolder12 = wx.StaticText(label = '', parent = panel)
        placeHolder13 = wx.StaticText(label = '', parent = panel)
        placeHolder14 = wx.StaticText(label = '', parent = panel)
        
        # 11th Row
        self.PushPacketBtn = wx.Button(id=wxID_PUSHPACKETBTN, 
                                       label='Push Packet', 
                                       parent = panel, 
                                       size = wx.Size(145, 50))
        self.PushPacketBtn.Bind(wx.EVT_BUTTON, self.OnPushPacketBtnButton,
                                id=wxID_PUSHPACKETBTN)
 
        placeHolder7 = wx.StaticText(label = '', parent = panel)
        placeHolder8 = wx.StaticText(label = '', parent = panel)

        # 12th ROW
        self.StartBtn = wx.Button(label='Start', 
                                  parent = panel, 
                                  size = wx.Size(145, 50))
        self.StartBtn.Bind(wx.EVT_BUTTON, self.OnStartBtn)
        self.StopBtn = wx.Button(label = "Stop", parent = panel, 
                                  size = wx.Size(145, 50))
        self.StopBtn.Bind(wx.EVT_BUTTON, self._OnStopBtn)
        placeHolder15 = wx.StaticText(label = '', parent = panel)

        placeHolder17 = wx.StaticText(label = '', parent = panel)

        # set up the grid
        sizer = wx.FlexGridSizer(cols = 3, hgap = 6, vgap = 6)
        sizer.AddMany([dataTypeLabel, self.dataTypeChoice, placeHolder2,
                       packetHeaderLabel, self.packetHeaderEditor, placeHolder3,
                       sendPacketIDLabel, self.sendIDChoice, placeHolder4, 
                       packetLenLabel, self.packetLenEditor, placeHolder5,
                       numPacksLabel, self.numPacksEditor, placeHolder16, 
                       placeHolder9, placeHolder10, placeHolder11,
                       placeHolder6, IChannelLabel, QChannelLabel,
                       dataLabel, self.iSourceChoice, self.qSourceChoice,
                       fileLabel, self.iFileNameEditor, self.qFileNameEditor,
                       delayLabel,self.delayEditor, self.timeUnitsChoice,
                       profilingLabel, self.profilingCheckBox, placeHolder15, 
                       placeHolder12, placeHolder13, placeHolder14,
                       self.PushPacketBtn, placeHolder7, placeHolder8,
                       self.StartBtn, self.StopBtn, placeHolder17     ])

        panel.SetSizer(sizer)

    def onSetDelay(self, event):
        '''This happens when the user types a number in the delay editor 
           and presses enter.  Gets the value from the editor and saves 
           it in a variable'''
        self.getDelay()
        event.Skip()

    def getDelay(self):
        '''Gets the value from the editor, modifies it by the units, and 
           saves the value in self.delay_between_packets'''

        self.delay_between_packets = float(self.delayEditor.GetLineText(0))

        if str(self.timeUnitsChoice.GetStringSelection()) == "miliseconds":
            self.delay_between_packets = self.delay_between_packets/1000
        elif str(self.timeUnitsChoice.GetStringSelection()) == "seconds":
            self.delay_between_packets = self.delay_between_packets
        else:
            print "WARNING: missing support for units other than miliseconds and seconds"
            print "see getDelay method in AWG.py"


    def _OnSourceChoiceChoice(self,event):
        ''' Private.  If a source option other than "file" is selected, 
            "grey out" the file input field'''

        i_source = self.iSourceChoice.GetStringSelection()
        if i_source == 'file':
            self.iFileNameEditor.Enable(True)
        else:
            self.iFileNameEditor.Enable(False)

        q_source = self.qSourceChoice.GetStringSelection()
        if q_source == 'file':
            self.qFileNameEditor.Enable(True)
        else:
            self.qFileNameEditor.Enable(False)
        

    def _send_data_loop(self):
        ''' Private.  Should be started as a thread durring startup.
            Sends data when start button is pressed, waits when stop
            button is pressed '''

        self.getDelay()  # Gets the initial value for the delay 
                         # between packets.  The delay between 
                         # packets will change later if it is edited
                         # in the GUI.
 
        self.packet_counter = 0

        # When the 'start' button has been pressed, recursively
        # send data.  Halt and wait when "stop" button is preseed.
        while self.is_running:
            self.start_event.wait()

            if self.packet_counter == self.numPacks:
                self.start_event.clear()  # like hitting the stop button
                print "done" 
                self.header_count = 0
                self.packet_counter = 0 
                continue                  

            if self.is_running == False:  # for shutdown
                break    
            self.sendSignal()

            if (self.i_source_selected == 'random' or 
                                    self.q_source_selected == 'random'):
                self.DefineSignalFromGUIInput()
            
            self.packet_counter += 1
            
            time.sleep(self.delay_between_packets)


    def DefineSignalFromGUIInput(self):
        self.i_file_name = self.iFileNameEditor.GetLineText(0)
        self.q_file_name = self.qFileNameEditor.GetLineText(0)
        AWG_instance = AWG(self)
        self.i_source_selected = self.iSourceChoice.GetStringSelection()
        self.q_source_selected = self.qSourceChoice.GetStringSelection()
        self.I = AWG_instance.get_signal(self.i_source_selected, 
                                         self.i_file_name)
        self.Q = AWG_instance.get_signal(self.q_source_selected, 
                                         self.q_file_name)


        # For OSSIE 0.6.2, only ComplexShort is supported
        # skip the data type conversion for data that is already integers
        # because the data type conversion is inefficient and not robust
        # because the python max module is not robust
        # For later versions of OSSIE that support more data types,
        # this method will need to be fixed appropriately.
        if self.i_source_selected == 'file' or\
           self.i_source_selected == 'zeros' or\
           self.i_source_selected == 'ones': 
            self.I = [int(x) for x in self.I]    #convert from string to integer
        else:        #convert from float to integer
            self.I = self.convert_data_type(self.I, self.interface)

        if self.q_source_selected == 'file' or\
           self.q_source_selected == 'zeros' or\
           self.q_source_selected == 'ones': 
            self.I = [int(x) for x in self.I]
        else:
            self.Q = self.convert_data_type(self.Q, self.interface)

    def sendSignal(self):
        ''' self.I and self.Q must already be defined from 
            DefineSignalFromGUIInput'''

        if self.PortHandle is not None:  # I am connected to a port
            if self.sending_headers:
                self.I.insert(0, int(self.headers[self.header_count]))
                self.Q.insert(0, int(self.headers[self.header_count]))

                self.header_count += 1
                if self.header_count >= len(self.headers):
                    self.header_count = 0

            if self.profilingCheckBox.GetValue() == True:
                tmp_filename = "profiles/_tmp" + str(self.profile_counter) + ".profile"
                self.my_profile.runctx(
                      "tmp_self.PortHandle.pushPacket(tmp_self.I, tmp_self.Q)", 
                      None, 
                      {"tmp_self": self})
                self.my_profile.dump_stats(tmp_filename)
                self.profile_counter += 1

            else:               # profiling is off
                self.PortHandle.pushPacket(self.I,self.Q)


    # Button methods
    def OnPushPacketBtnButton(self,event):
        '''accesses the AWG class to get a signal, then sends the signal'''
        self.headers = self.packetHeaderEditor.GetLineText(0)
        self.headers = self.headers.split(',')
        if self.headers[0] == u"":
            self.sending_headers = False
        else:
            self.sending_headers = True

        self.DefineSignalFromGUIInput()
        self.sendSignal()


    def OnStartBtn(self, event):
        self.DefineSignalFromGUIInput()
        self.headers = self.packetHeaderEditor.GetLineText(0)
        self.headers = self.headers.split(',')
        if self.headers[0] == u"":
            self.sending_headers = False
        else:
            self.sending_headers = True

        self.numPacks = self.numPacksEditor.GetLineText(0)

        if self.numPacks == "":
            self.numPacks = -1
        self.numPacks = int(self.numPacks)

        self.onSetDelay(event)

        self.start_event.set()


    def _OnStopBtn(self, event):
        ''' Will halt the send_data_loop loop.  Occurs when the stop button
            is preseed '''
        self.start_event.clear()
        self.header_count = 0
        self.packet_counter = 0

    def convert_data_type(self, data, type):
        ''' Public.  Converts first argument into the data type specified by
            the second argument (e.g., Short to Float) '''

        if type == "complexShort":   #short and int are the same in python
            #TODO: test the robustness of the max() module
            #WARNING: if the maximum value of the data is greater than 1, this will probably crash 
            #data_max = max(data)
            data_max = 1
            SHRT_MAX = 32767    #have to use -1 because round might round up to 32768
            data = [int(round(float(x)*(SHRT_MAX/data_max))) for x in data]  #conver to integer format
        elif type == "complexFloat":
            data = [float(x) for x in data]
        else:
            print "types other than complexFloat and complexShort are not yet supported in sources.convert"
        
        return data


    def _OnFileExit(self, event):
        '''This is what will happen when you select File -> Exit 
           in the menu bar'''
        self.Close()      #close the frame
  

    def _OnHelpAbout(self, event):
        ''' Stuff that gets displayed when you select Help -> About 
            in the menu bar'''
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, "Arbitrary Waveform Generator.\nA product of Wireless@VT.\n\nFor OSSIE 0.6.2.", "About...")
        about.ShowModal()


    def setup_component_connection(self):
        ''' Mostly contains CORBA stuff.
            Will create self.PortHandle.  
            This is an outbound connection.'''

        self.CORBA_being_used = False

        if True:		
         self.CORBA_being_used = True
         self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
         obj = self.orb.resolve_initial_references("NameService")
         rootContext = obj._narrow(CosNaming.NamingContext)
         if rootContext is None:
             print "Failed to narrow the root naming context"
             sys.exit(1)
         name = [CosNaming.NameComponent(self.component_name[0],""),
         CosNaming.NameComponent(self.component_name[1],""),
         CosNaming.NameComponent(self.component_name[2],"")]
     
         try:
             ResourceRef = rootContext.resolve(name)
     
         except:
             print "Required resource not found"
             sys.exit(1)
     
         #connect to an existing port
         ResourceHandle = ResourceRef._narrow(CF.Resource)
         PortReference = ResourceHandle.getPort(self.port_name)
         if PortReference is None:
             print "Failed to get Port reference"
         self.PortHandle = PortReference._narrow(standardInterfaces__POA.complexShort)

         # TODO: support fan out?


    def setup_tool2tool_connection(self):
        self.PortHandle = self.other_tool_ref

    def disconnect(self):
        ''' Disconnects the connection between the AWG and whatever
            it happens to be connected to. '''

        # Since only one connection is established, this is easy'''
        self.PortHandle = None

    def _OnCloseWindow(self,event):
        ''' Private.  Happens when AWG main window is shut down.  
            Ends the _send_data_loop thread '''

        self.start_event.clear()  # tells the send_data_loop loop to halt
        time.sleep(self.delay_between_packets) # wait for it to finish

        self.is_running = False    # Get out of the send_data_loop loop
        self.start_event.set()   

        if hasattr(self.parent, 'removeToolFrame'):
            self.parent.removeToolFrame(self)
        self = None
        event.Skip()



