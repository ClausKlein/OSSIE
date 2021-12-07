#Boa:Dialog:Dialog1

## Copyright 2005, 2006, 2007 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE Waveform Developer.
##
## OSSIE Waveform Developer is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## OSSIE Waveform Developer is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE Waveform Developer; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import wx

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1STATICBITMAP1, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, wxID_DIALOG1STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(6)]

class Dialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(893, 355), size=wx.Size(306, 385),
              style=wx.DEFAULT_DIALOG_STYLE, title='About')
        self.SetClientSize(wx.Size(306, 385))
        self.Center(wx.BOTH)

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label='OSSIE Waveform Developer', name='staticText1', parent=self,
              pos=wx.Point(21, 16), size=wx.Size(252, 24),
              style=wx.ALIGN_CENTRE)
        self.staticText1.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Microsoft Sans Serif'))

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label='MPRG at Virginia Tech', name='staticText2', parent=self,
              pos=wx.Point(80, 42), size=wx.Size(135, 17), style=0)
        self.staticText2.SetBackgroundColour(wx.Colour(128, 128, 255))
        self.staticText2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Microsoft Sans Serif'))
        self.staticText2.SetMinSize(wx.Size(-1, -1))

        root = __file__
        if os.path.islink (root):
              root = os.path.realpath (root)
        root = os.path.dirname (os.path.abspath (root))
        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(root + '/images/ossieLogo.bmp',
              wx.BITMAP_TYPE_BMP), id=wxID_DIALOG1STATICBITMAP1,
              name='staticBitmap1', parent=self, pos=wx.Point(48, 93),
              size=wx.Size(199, 227), style=0)
        self.staticBitmap1.SetMinSize(wx.Size(199, 227))

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label='Close',
              name='button1', parent=self, pos=wx.Point(172, 339),
              size=wx.Size(75, 26), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_DIALOG1BUTTON1)

        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3, label='',
              name='staticText3', parent=self, pos=wx.Point(87, 63),
              size=wx.Size(120, 19), style=0)
        self.staticText3.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Arial'))

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.staticText3.SetLabel(parent.version)

    def OnButton1Button(self, event):
        self.Close()
