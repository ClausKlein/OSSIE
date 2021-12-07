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

import wx

def errorMsg(self,msg):
    dlg = wx.MessageDialog(self,msg,'Error', wx.OK | wx.ICON_INFORMATION)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    return

def owdMsg(self,msg):
    dlg = wx.MessageDialog(self, msg,
          'OSSIE Waveform Developer', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
    try:
        if dlg.ShowModal() == wx.ID_NO:
            return False
    finally:
        dlg.Destroy()
        
    return True
