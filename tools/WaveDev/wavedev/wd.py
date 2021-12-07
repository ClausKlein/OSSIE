#!/usr/bin/env python
#Boa:App:BoaApp

## Copyright 2005, 2006 Virginia Polytechnic Institute and State University
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

import wx

import MainFrame

modules ={'AboutDialog': [0, '', 'AboutDialog.py'],
 'ComponentClass': [0, '', 'ComponentClass.py'],
 'ComponentFrame': [0, '', 'ComponentFrame.py'],
 'ConnectDialog': [0, '', 'ConnectDialog.py'],
 'MainFrame': [1, 'Main frame of Application', 'MainFrame.py'],
 u'NodeDialog': [0, '', u'NodeDialog.py'],
 'PortDialog': [0, '', 'PortDialog.py'],
 u'PropertiesDialog': [0, '', u'PropertiesDialog.py'],
 'WaveformClass': [0, '', 'WaveformClass.py'],
 u'application_gen': [0, '', u'XML_gen/application_gen.py'],
 u'component_gen': [0, '', u'XML_gen/component_gen.py'],
 'genStructure': [0, '', 'generate/genStructure.py']}

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = MainFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
