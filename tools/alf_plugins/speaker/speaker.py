#!/usr/bin/env python

## Copyright 2007 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE ALF speaker tool.
##
## OSSIE ALF speaker is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## OSSIE ALF speaker is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE ALF speaker; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
from omniORB import CORBA
import CosNaming
from ossie.cf import CF, CF__POA
from ossie.standardinterfaces import standardInterfaces
from ossie.standardinterfaces import standardInterfaces__POA
import time, threading
import ossaudiodev
import struct
import wx
import time

class my_sound_structure(standardInterfaces__POA.complexShort):
    def __init__(self, orb, gui):
        #print "Initializing consumer..."
        self.orb = orb
        self.gui = gui
        self.end_time = time.time()
        self.begin_time = time.time()

    def pushPacket(self, Left_channel, Right_channel):
        if self.gui.sound_state:
            my_string = ''
            if Right_channel[0]==0:	# using the left channel
                for y in range(0,len(Left_channel)):
                    upper_val = Left_channel[y]/256
                    lower_val = Left_channel[y] - (upper_val * 256)
                    my_string += struct.pack('h', Left_channel[y])
                    #my_string += struct.pack('B',lower_val)
                    #my_string += struct.pack('b',upper_val)
                    if self.gui.channels == 2:
                        my_string += '\0'
                        my_string += '\0'
                    else:
                        my_string += struct.pack('h', Left_channel[y])
                        #my_string += struct.pack('B',lower_val)
                        #my_string += struct.pack('b',upper_val)
            else:     # using the right channel
                for y in range(0,len(Right_channel)):
                    upper_val = Right_channel[y]/256
                    lower_val = Right_channel[y] - (upper_val * 256)
                    my_string += struct.pack('h', Right_channel[y])
                    #my_string += struct.pack('B',lower_val)
                    #my_string += struct.pack('b',upper_val)
                    if self.gui.channels == 2:
                        my_string += '\0'
                        my_string += '\0'
                    else:
                        my_string += struct.pack('h', Right_channel[y])
                        #my_string += struct.pack('B',lower_val)
                        #my_string += struct.pack('b',upper_val)
            self.gui.sound_driver.writeall(my_string)
            self.end_time = time.time()

class SpeakerFrame(wx.Frame):

    def __init__(self,parent, namespace, interface, ns_name, port_name):
        self.namespace = namespace
        self.interface = interface
        self.ns_name = ns_name
        self.port_name = port_name
        self.parent = parent
        self.setup_sound()
        self.XLEFT = 25
        self.YTOP = 65
        self.VSPACE = 70
        self._init_ctrls(parent)
        self.sound_state = True
        self.channels = self.osschannels
        self.sampleRateBox.SetValue(str(self.ossspeed))
        self.sampleTypeChoice.SetSelection(1)

    def _init_ctrls(self,prnt):
        # Initialize the frame
        wx.Frame.__init__(self, id=-1, name='irFrame',
        parent=prnt, pos=wx.Point(-1, -1), size=wx.Size(600, 100),
        style=wx.DEFAULT_FRAME_STYLE, title=u'Sound Out Control')

        self.panel = wx.Panel(parent=self, pos=wx.Point(1,1), size=wx.Size(450,450))
		
        self.sampleRateBox = wx.TextCtrl(id=-1,
            name=u'sampleRateBox', parent=self.panel, pos=wx.Point(self.XLEFT+320, self.YTOP-20),
            size=wx.Size(100, 25),value=u'')
        self.staticText1 = wx.StaticText(id=-1,
            label=u'Sample Rate:', name='staticText1', parent=self.panel,
            pos=wx.Point(self.XLEFT+325, self.YTOP-40), size=wx.Size(120, 17), style=0)
        self.UpdateRateBtn = wx.Button(id=-1, label='update rate',
            name='ExitBtn', parent=self.panel, pos=wx.Point(self.XLEFT+320, self.YTOP+2),
            size=wx.Size(100, 25), style=0)
        self.UpdateRateBtn.Bind(wx.EVT_BUTTON, self.OnUpdateRateBtn, id=-1)
		
        #self.bitChoice = wx.Choice(choices=["U8","U16","S16"], id=-1, name=u'bitChoice',
        self.bitChoice = wx.Choice(choices=["U8"], id=-1, name=u'bitChoice',
            parent=self.panel,pos=wx.Point(self.XLEFT+70,self.YTOP-20), size=wx.Size(75,27), style=0);
        self.staticText5 = wx.StaticText(id=-1,
            label=u'Bits Per Sample:', name='staticText5', parent=self.panel,
            pos=wx.Point(self.XLEFT+75, self.YTOP-40), size=wx.Size(145, 17), style=0)
        self.bitChoice.Bind(wx.EVT_BUTTON, self.OnSoundBtn, id=-1)

        self.sampleTypeChoice = wx.Choice(choices=["stereo","mono"], id=-1, name=u'sampleTypeChoice',
            parent=self.panel,pos=wx.Point(self.XLEFT+195,self.YTOP-20), size=wx.Size(90,27), style=0);
        self.staticText6 = wx.StaticText(id=-1,
            label=u'Sample Type:', name='staticText5', parent=self.panel,
            pos=wx.Point(self.XLEFT+200, self.YTOP-40), size=wx.Size(120, 17), style=0)
        self.sampleTypeChoice.Bind(wx.EVT_CHOICE, self.OnsampleTypeChoice, id=-1)
		
        self.ExitBtn = wx.Button(id=-1, label='Exit',
            name='ExitBtn', parent=self.panel, pos=wx.Point(self.XLEFT+460, self.YTOP-23),
            size=wx.Size(80, 30), style=0)
        self.ExitBtn.Bind(wx.EVT_BUTTON, self.OnExitBtn, id=-1)

        self.SoundBitmap = wx.Bitmap("/sdr/sca/tools/speaker/audio-on.xpm", wx.BITMAP_TYPE_XPM)
        self.SoundBtn = wx.BitmapButton(id=-1, name='initBtn', parent=self.panel, pos=wx.Point(self.XLEFT, self.YTOP-40),
            size=wx.Size(55, 55), style=0, bitmap=self.SoundBitmap)
        self.SoundBtn.Bind(wx.EVT_BUTTON, self.OnSoundBtn, id=-1)

        # Bind the close event so we can disconnect the ports
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def setup_sound(self):
        self.timing_diff = 1000
        self.ossspeed = 100000
        self.osschannels = 1
        self.ossfmt = ossaudiodev.AFMT_S16_LE
        self.CORBA_being_used = False

        self.sound_driver = ossaudiodev.open('w')
        self.osschannels = self.sound_driver.channels(2)
        #ossfmt = sound_driver.setfmt(ossaudiodev.AFMT_U8)
        self.ossfmt = self.sound_driver.setfmt(ossaudiodev.AFMT_S16_LE)
        self.ossspeed = self.sound_driver.speed(50000)
        self.sound_driver.nonblock()

        if not ((self.ns_name==None) or (self.port_name==None)):		
         self.CORBA_being_used = True
         self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
         obj = self.orb.resolve_initial_references("NameService")
         rootContext = obj._narrow(CosNaming.NamingContext)
         if rootContext is None:
             print "Failed to narrow the root naming context"
             sys.exit(1)
         name = [CosNaming.NameComponent(self.ns_name[0],""),
             CosNaming.NameComponent(self.ns_name[1],""),
             CosNaming.NameComponent(self.ns_name[2],"")]
     
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
 
         self.my_local_speaker = my_sound_structure(self.orb, self)
         obj_poa = self.orb.resolve_initial_references("RootPOA")
         poaManager = obj_poa._get_the_POAManager()
         poaManager.activate()
         obj_poa.activate_object(self.my_local_speaker)
         self.PortHandle.connectPort(self.my_local_speaker._this(), "thisismyconnectionid_speaker")
         self.connected_state = True
         #orb.run()

    def OnCloseWindow(self,event):
        if hasattr(self.parent, 'removeToolFrame'):
            self.parent.removeToolFrame(self)
        self = None
        event.Skip()

    def __del__(self):
        if self.CORBA_being_used:
            if self.connected_state == True:
                self.PortHandle.disconnectPort("thisismyconnectionid_speaker")
            while (time.time() - self.my_local_speaker.end_time) < 1.0:
                #print (time.time() - my_local_speaker.end_time)
                time.sleep(1)
            #sys.exit(0)

    def OnUpdateRateBtn(self, event):
        inspeed = self.sampleRateBox.GetValue()
        self.ossspeed = self.sound_driver.speed(int(inspeed))
        #print "This is my new speed: " + str(ossspeed) + " from this speed: " + inspeed
        self.sampleRateBox.SetValue(str(self.ossspeed))
        pass

    def OnsampleTypeChoice(self, event):
        sel = self.sampleTypeChoice.GetSelection()
        #print "The selection is: " + str(sel)
        if self.sampleTypeChoice.GetSelection()==1:
            self.channels = 1
        else:
            self.channels = 2

    def OnExitBtn(self,event):
        if self.CORBA_being_used:
            self.PortHandle.disconnectPort("thisismyconnectionid_speaker")
            self.connected_state = False
            while (time.time() - self.my_local_speaker.end_time) < 1.0:
                #print (time.time() - my_local_speaker.end_time)
                time.sleep(1)
            #sys.exit(0)
            self.Close()
        else:
            self.Close()

    def OnSoundBtn(self,event):
        if self.sound_state:
            self.SoundBitmap = wx.Bitmap("/sdr/sca/tools/speaker/audio-off.xpm", wx.BITMAP_TYPE_XPM)
            self.SoundBtn = wx.BitmapButton(id=-1, name='initBtn', parent=self.panel, pos=wx.Point(self.XLEFT, self.YTOP-40),
                size=wx.Size(55, 55), style=0, bitmap=self.SoundBitmap)
            self.SoundBtn.Bind(wx.EVT_BUTTON, self.OnSoundBtn, id=-1)
            self.sound_state = False
        else:
            self.SoundBitmap = wx.Bitmap("/sdr/sca/tools/speaker/audio-on.xpm", wx.BITMAP_TYPE_XPM)
            self.SoundBtn = wx.BitmapButton(id=-1, name='initBtn', parent=self.panel, pos=wx.Point(self.XLEFT, self.YTOP-40),
                size=wx.Size(55, 55), style=0, bitmap=self.SoundBitmap)
            self.SoundBtn.Bind(wx.EVT_BUTTON, self.OnSoundBtn, id=-1)
            self.sound_state = True

def create(parent, namespace, interface, ns_name, port_name):
    return SpeakerFrame(parent, namespace, interface, ns_name, port_name)

if __name__=="__main__":
 if not (len(sys.argv)==5):
  print "usage: plot.py <Domain_name> <Waveform_name> <Component_name> <port_name>"
  sys.exit(1)

 wx.InitAllImageHandlers()
 application = wx.App(0)
 application.main = create(None, "standardInterfaces", "complexShort", [sys.argv[1], sys.argv[2], sys.argv[3]], sys.argv[4])
 application.main.Show()
 application.SetTopWindow(application.main)
 application.MainLoop()
