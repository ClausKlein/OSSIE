#!/usr/bin/env python

## Copyright 2007 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE ALF write_to_file tool.
##
## OSSIE ALF write_to_file is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## OSSIE ALF write_to_file is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE ALF write_to_file; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


'''Write incomming packet(s) to file(s)'''

import wx         #needed for display stuff
from omniORB import CORBA      #use this for the CORBA orb stuff (pushing packets)
import sys       #for system commands (e.g., argv and argc stuff)
import CosNaming   #narrowing naming context stuff
from ossie.cf import CF, CF__POA    #core framework stuff
from ossie.standardinterfaces import standardInterfaces__POA
from wx.lib.anchors import LayoutAnchors  #used by splitter window
# import wx.lib.buttons as buttons #for special wx buttons

class write_to_file_short(standardInterfaces__POA.complexShort):
    '''Writes I and Q data to 2 files'''

    def __init__(self, orb, gui):        
        self.orb = orb 
        self.gui = gui    #usually parent
        self.delimiter = ','

    def pushPacket(self, I_data, Q_data):
        '''Store the data to be written to file when the Write Packet 
           button is bushed'''
        self.gui.I_data = I_data
        self.gui.Q_data = Q_data
  


def create(parent,namespace, interface, ns_name, port_name):
    #return MainFrame(parent, -1, namespace, interface, ns_name, port_name)
    return MainFrame(parent, -1, "Don't know what this should be", 
                     namespace, interface, ns_name, port_name)

#generate wx ids for my wx controls
[wxID_MAINFRAME, wxID_SPLITTERWINDOW1, wxID_WRITEPACKETBTN, wxID_WRITEBUFFERBTN, wxID_IFILENAMEEDITOR, wxID_QFILENAMEEDITOR, wxID_IFILESTATICTEXT,wxID_QFILESTATICTEXT] = [wx.NewId() for _init_ctrls in range(8)]


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title, namespace, interface, 
                 component_name, port_name):

        self._init_ctrls(parent)

        self.I_data = []
        self.Q_data = []
         
        self.parent = parent
        self.namespace = namespace
        self.interface = interface
        self.my_local_controls = None
        self.component_name = component_name
        self.port_name = port_name
        self.setup_graphics()
        
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
        
        self.iFileNameEditor.write('i_out.dat')
        self.qFileNameEditor.write('q_out.dat')


    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='', parent=prnt,
              pos=wx.Point(530, 680), size=wx.Size(520, 320),
              style=wx.DEFAULT_FRAME_STYLE, title='Write to File Tool')

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_SPLITTERWINDOW1,
              name='splitterWindow1', parent=self, point=wx.Point(1, 1),
              size=wx.Size(570, 270), style=wx.SP_3D)
        self.splitterWindow1.SetConstraints(LayoutAnchors(self.splitterWindow1,
              True, True, True, True))

        self.WritePacketBtn = wx.Button(id=wxID_WRITEPACKETBTN, label='Write Packet',
              name='WritePacketBtn', parent=self.splitterWindow1, pos=wx.Point(155, 150),
              size=wx.Size(165, 50))
        self.WritePacketBtn.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.WritePacketBtn.SetBackgroundColour("green")
        self.WritePacketBtn.Bind(wx.EVT_BUTTON, self.OnWritePacketBtnButton,
              id=wxID_WRITEPACKETBTN)

        self.WriteBufferBtn = wx.Button(id=wxID_WRITEBUFFERBTN, label='Write BUFFER',
              name='WriteBufferBtn', parent=self.splitterWindow1, pos=wx.Point(155, 210),
              size=wx.Size(165, 50))
        self.WriteBufferBtn.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.WriteBufferBtn.SetBackgroundColour("green")
        self.WriteBufferBtn.Bind(wx.EVT_BUTTON, self.OnWriteBufferBtnButton,
              id=wxID_WRITEBUFFERBTN)

        #####
        ## if you want an image on the button
        # button_bmp = wx.Image("../AWG/my_image.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # self.WritePacketBtn = buttons.GenBitmapTextButton(self.splitterWindow1,
        #       wxID_WRITEPACKETBTN,button_bmp, 'Write Packet',
        #       name='WritePacketBtn', pos=wx.Point(155, 250),
        #       size=wx.Size(300, 100), style=0)
        # self.WritePacketBtn.Bind(wx.EVT_BUTTON, self.OnWritePacketBtnButton,
        #       id=wxID_WRITEPACKETBTN)
        #####

       
        self.iFileNameEditor = wx.TextCtrl(id=wxID_IFILENAMEEDITOR,
              name=u'iFileNameEditor', parent=self.splitterWindow1, pos=wx.Point(215, 50),
              size=wx.Size(250, 30), style=0, value=u'')
			  

        self.qFileNameEditor = wx.TextCtrl(id=wxID_QFILENAMEEDITOR,
              name=u'qFileNameEditor', parent=self.splitterWindow1, pos=wx.Point(215, 100),
              size=wx.Size(250, 30), style=0, value=u'')


        self.iFileStaticText = wx.StaticText(id=wxID_IFILESTATICTEXT,
              label=u'I channel file:', name='qFileStaticText', parent=self.splitterWindow1,
              pos=wx.Point(55, 50), size= wx.Size(100, 20), style=0)
        self.iFileStaticText.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.BOLD,True,u'Sans'))

        self.qFileStaticText = wx.StaticText(id=wxID_QFILESTATICTEXT,
              label=u'Q channel file:', name='qFileStaticText', parent=self.splitterWindow1,
              pos=wx.Point(55, 100), size= wx.Size(100, 20), style=0)
        self.qFileStaticText.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.BOLD,True,u'Sans'))
  
 

    def OnWritePacketBtnButton(self,event):
        #get the file names from the file name editors in the GUI
        self.i_file_name = self.iFileNameEditor.GetLineText(0)
        self.q_file_name = self.qFileNameEditor.GetLineText(0)

        #write the data out
        open_file = open(self.i_file_name, 'w')   #open the file for writing
        open_file.write(str(self.I_data))
        open_file.close()

        open_file = open(self.q_file_name, 'w')   #open the file for writing
        open_file.write(str(self.Q_data))
        open_file.close()

    def OnWriteBufferBtnButton(self,event):
        #get the file names from the file name editors in the GUI
        self.i_file_name = self.iFileNameEditor.GetLineText(0)
        self.q_file_name = self.qFileNameEditor.GetLineText(0)

        #write the data out
        open_file = open(self.i_file_name, 'w')   #open the file for writing
        open_file.write(str(self.I_data))
        open_file.close()

        open_file = open(self.q_file_name, 'w')   #open the file for writing
        open_file.write(str(self.Q_data))
        open_file.close()

    def OnFileExit(self, event):
        '''This is what will happen when you select File -> Exit 
           in the menu bar'''
        self.Close()      #close the frame
  
    def OnHelpAbout(self, event):
        '''Stuff that gets displayed when you select Help -> About in 
           the menu bar'''
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, "Write to file tool.\nA product of Wireless@VT.", "About...")
        about.ShowModal()

    def setup_graphics(self):
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
     
         ResourceHandle = ResourceRef._narrow(CF.Resource)
         PortReference = ResourceHandle.getPort(self.port_name)
         if PortReference is None:
             print "Failed to get Port reference"
         self.PortHandle = PortReference._narrow(CF.Port)
         
        
         #create the class instance of the write_to_file class 
         self.my_file_writer = write_to_file_short(self.orb, self)

         obj_poa = self.orb.resolve_initial_references("RootPOA")
         poaManager = obj_poa._get_the_POAManager()
         poaManager.activate()
         obj_poa.activate_object(self.my_file_writer)
         self.PortHandle.connectPort(self.my_file_writer._this(), 
                                     "thisismyconnectionid_w2file")
         #orb.run()

    def OnCloseWindow(self,event):
        if hasattr(self.parent, 'removeToolFrame'):
            self.parent.removeToolFrame(self)
        self = None
        event.Skip()

    def __del__(self):
        if self.CORBA_being_used:
            self.PortHandle.disconnectPort("thisismyconnectionid_w2file")
            while (_time.time() - self.my_local_plot.end_time) < 1.5:
                #print (time.time() - self.my_local_plot.end_time)
                pass
                #_time.sleep(1)



