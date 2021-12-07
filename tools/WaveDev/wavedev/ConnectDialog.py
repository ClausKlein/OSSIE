#Boa:Dialog:ConnectDialog

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
import sys
import os
from errorMsg import *
import ComponentClass

def create(parent):
    return ConnectDialog(parent)

[wxID_CONNECTDIALOG, wxID_CONNECTDIALOGCONLABEL, wxID_CONNECTDIALOGCONNECTBOX, 
 wxID_CONNECTDIALOGCONNECTBTN, wxID_CONNECTDIALOGDSTBOX, 
 wxID_CONNECTDIALOGINTLABELDST, wxID_CONNECTDIALOGINTLABELSRC, 
 wxID_CONNECTDIALOGOKBTN, wxID_CONNECTDIALOGSRCBOX, 
 wxID_CONNECTDIALOGSTATICBITMAP1, wxID_CONNECTDIALOGSTATICBITMAP2, 
 wxID_CONNECTDIALOGSTATICBOX1, wxID_CONNECTDIALOGSTATICTEXT1, 
 wxID_CONNECTDIALOGSTATICTEXT2, wxID_CONNECTDIALOGSTATICTEXT3, 
 wxID_CONNECTDIALOGSTATICTEXT4, wxID_CONNECTDIALOGSTATICTEXT5, 
 wxID_CONNECTDIALOGSTATICTEXT6, 
] = [wx.NewId() for _init_ctrls in range(18)]

class ConnectDialog(wx.Dialog):
    def _init_coll_imageList1_Images(self, parent):
        # generated method, don't edit

        root = __file__
        if os.path.islink (root):
              root = os.path.realpath (root)
        root = os.path.dirname (os.path.abspath (root))
        parent.Add(bitmap=wx.Bitmap( root + '/images/uses.bmp', wx.BITMAP_TYPE_BMP),
              mask=wx.NullBitmap)
        parent.Add(bitmap=wx.Bitmap( root + '/images/provides.bmp', wx.BITMAP_TYPE_BMP),
              mask=wx.NullBitmap)

    def _init_utils(self):
        # generated method, don't edit
        self.imageList1 = wx.ImageList(height=16, width=16)
        self._init_coll_imageList1_Images(self.imageList1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CONNECTDIALOG, name='ConnectDialog',
              parent=prnt, pos=wx.Point(727, 264), size=wx.Size(638, 567),
              style=wx.DEFAULT_DIALOG_STYLE, title='Connections')
        self._init_utils()
        self.SetClientSize(wx.Size(638, 567))
        self.Center(wx.BOTH)

        self.ConnectBtn = wx.Button(id=wxID_CONNECTDIALOGCONNECTBTN,
              label='Connect', name='ConnectBtn', parent=self, pos=wx.Point(239,
              182), size=wx.Size(85, 30), style=0)
        self.ConnectBtn.Bind(wx.EVT_BUTTON, self.OnConnectBtnButton,
              id=wxID_CONNECTDIALOGCONNECTBTN)

        self.ConLabel = wx.StaticText(id=wxID_CONNECTDIALOGCONLABEL,
              label='None', name='ConLabel', parent=self, pos=wx.Point(29, 21),
              size=wx.Size(31, 17), style=0)

        self.OkBtn = wx.Button(id=wxID_CONNECTDIALOGOKBTN, label=u'Ok',
              name=u'OkBtn', parent=self, pos=wx.Point(488, 496),
              size=wx.Size(85, 30), style=0)
        self.OkBtn.Bind(wx.EVT_BUTTON, self.OnOkBtnButton,
              id=wxID_CONNECTDIALOGOKBTN)

        self.srcBox = wx.TreeCtrl(id=wxID_CONNECTDIALOGSRCBOX, name=u'srcBox',
              parent=self, pos=wx.Point(24, 48), size=wx.Size(199, 296),
              style=wx.SIMPLE_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.srcBox.SetImageList(self.imageList1)
        self.srcBox.SetBestFittingSize(wx.Size(199, 296))
        self.srcBox.Bind(wx.EVT_LEFT_UP, self.OnSrcBoxLeftUp)

        self.dstBox = wx.TreeCtrl(id=wxID_CONNECTDIALOGDSTBOX, name=u'dstBox',
              parent=self, pos=wx.Point(340, 48), size=wx.Size(278, 296),
              style=wx.SIMPLE_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.dstBox.SetImageList(self.imageList1)
        self.dstBox.SetBestFittingSize(wx.Size(278, 296))
        self.dstBox.Bind(wx.EVT_LEFT_UP, self.OnDstBoxLeftUp)

        self.connectBox = wx.ListBox(choices=[],
              id=wxID_CONNECTDIALOGCONNECTBOX, name=u'connectBox', parent=self,
              pos=wx.Point(52, 429), size=wx.Size(401, 118), style=0)
        self.connectBox.SetBestFittingSize(wx.Size(401, 118))

        self.staticText1 = wx.StaticText(id=wxID_CONNECTDIALOGSTATICTEXT1,
              label=u'Connections', name='staticText1', parent=self,
              pos=wx.Point(214, 405), size=wx.Size(105, 17), style=0)

        self.staticText2 = wx.StaticText(id=wxID_CONNECTDIALOGSTATICTEXT2,
              label=u'Available ports to connect to:', name='staticText2',
              parent=self, pos=wx.Point(394, 21), size=wx.Size(235, 17),
              style=0)

        self.intLabelSrc = wx.StaticText(id=wxID_CONNECTDIALOGINTLABELSRC,
              label=u'intLabelSrc', name=u'intLabelSrc', parent=self,
              pos=wx.Point(120, 352), size=wx.Size(65, 17), style=0)

        self.intLabelDst = wx.StaticText(id=wxID_CONNECTDIALOGINTLABELDST,
              label=u'intLabelDst', name=u'intLabelDst', parent=self,
              pos=wx.Point(466, 352), size=wx.Size(66, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_CONNECTDIALOGSTATICTEXT3,
              label=u'Interface:', name='staticText3', parent=self,
              pos=wx.Point(30, 352), size=wx.Size(67, 17), style=0)
        self.staticText3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Sans'))

        self.staticText4 = wx.StaticText(id=wxID_CONNECTDIALOGSTATICTEXT4,
              label=u'Interface:', name='staticText4', parent=self,
              pos=wx.Point(386, 352), size=wx.Size(67, 17), style=0)
        self.staticText4.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Sans'))

        self.staticBox1 = wx.StaticBox(id=wxID_CONNECTDIALOGSTATICBOX1,
              label=u'Legend', name='staticBox1', parent=self, pos=wx.Point(233,
              264), size=wx.Size(96, 68), style=0)
        self.staticBox1.SetBestFittingSize(wx.Size(96, 68))

        root = __file__
        if os.path.islink (root):
              root = os.path.realpath (root)
        root = os.path.dirname (os.path.abspath (root))
        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap( root+ '/images/uses.bmp',
              wx.BITMAP_TYPE_BMP), id=wxID_CONNECTDIALOGSTATICBITMAP1,
              name='staticBitmap1', parent=self, pos=wx.Point(245, 286),
              size=wx.Size(16, 16), style=0)

        self.staticBitmap2 = wx.StaticBitmap(bitmap=wx.Bitmap( root + '/images/provides.bmp',
              wx.BITMAP_TYPE_BMP), id=wxID_CONNECTDIALOGSTATICBITMAP2,
              name='staticBitmap2', parent=self, pos=wx.Point(245, 306),
              size=wx.Size(16, 16), style=0)

        self.staticText5 = wx.StaticText(id=wxID_CONNECTDIALOGSTATICTEXT5,
              label=u'Uses', name='staticText5', parent=self, pos=wx.Point(269,
              284), size=wx.Size(55, 17), style=0)

        self.staticText6 = wx.StaticText(id=wxID_CONNECTDIALOGSTATICTEXT6,
              label=u'Provides', name='staticText6', parent=self,
              pos=wx.Point(269, 304), size=wx.Size(60, 17), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.parent = parent
        self.active_comp = parent.active_comp
        
        # Set the label for the Component box
        t = self.active_comp.name +" ports:"
        self.ConLabel.SetLabel(t)
        
        # Set the interface labels to nothing
        self.intLabelSrc.SetLabel('')
        self.intLabelDst.SetLabel('')
        
        # Add the available ports on the Component
        srcRoot= self.srcBox.AddRoot("src_root")
        for p in self.active_comp.ports:
            if p.type == 'Uses':
                t1 = self.srcBox.AppendItem(srcRoot,p.name,image=0)
            else:
                t1 = self.srcBox.AppendItem(srcRoot,p.name,image=1)
            self.srcBox.SetPyData(t1,p)
        
        # Add the available ports from all the other Components
        dstRoot = self.dstBox.AddRoot("dst_root")
        compRoot = self.dstBox.AppendItem(dstRoot,"Components")
        devRoot = self.dstBox.AppendItem(dstRoot,"Devices")
        for c in parent.active_wave:
            t1 = self.dstBox.AppendItem(compRoot,c.name)
            self.dstBox.SetPyData(t1,c)
            for p in c.ports:
                if p.type == 'Uses':
                    t2 = self.dstBox.AppendItem(t1,p.name,image=0)
                else:
                    t2 = self.dstBox.AppendItem(t1,p.name,image=1)
                self.dstBox.SetPyData(t2,p)
            self.dstBox.Expand(t1)
        
        for n in self.parent.active_plat.nodes:
            t1 = self.dstBox.AppendItem(devRoot,n.name)
            self.dstBox.SetPyData(t1,n)    
            for d in n.Devices:
                t2 = self.dstBox.AppendItem(t1,unicode(d.name))
                self.dstBox.SetPyData(t2,d)
                for p in d.ports:
                    if p.type == 'Uses':
                        t3 = self.dstBox.AppendItem(t2,p.name,image=0)
                    else:
                        t3 = self.dstBox.AppendItem(t2,p.name,image=1)
                    self.dstBox.SetPyData(t3,p)
                        
                self.dstBox.Expand(t2)
            self.dstBox.Expand(t1)
        
        self.displayConnections()

    def OnConnectBtnButton(self, event):
        srcOK = self.checkSrcBox()
        dstOK = self.checkDstBox()
        
        if not srcOK or not dstOK:
            return        
        else:
            srcSel = self.srcBox.GetSelection()
            dstSel = self.dstBox.GetSelection()        
            # both the source and destination boxes have ports selected
            srcP = self.srcBox.GetPyData(srcSel)
            dstP = self.dstBox.GetPyData(dstSel)
            dstC = self.dstBox.GetPyData(self.dstBox.GetItemParent(dstSel))
            
            if (srcP.type == 'Uses' and dstP.type == 'Uses') or \
                (srcP.type == 'Provides' and dstP.type == 'Provides'):
                errorMsg(self,"Ports cannot be of same type")
                return
            newCon = ComponentClass.Connection(srcP,dstP,dstC)
            tmpflag,tmpcomp = self.checkConnection(newCon)
            if tmpflag == True:
                self.active_comp.connections.append(newCon)
                self.displayConnections()
            else:
                errorMsg(self,"A duplicate connection exists on <"+tmpcomp+">.")
            
        event.Skip()
        
    def displayConnections(self):
        self.connectBox.Clear()
        cnames = []
        for x in self.active_comp.connections:
            tmpS = x.localPort.name + " ==> " + x.remoteComp.name + "::" + x.remotePort.name
            cnames.append(tmpS)
        if len(cnames) != 0:
            self.connectBox.InsertItems(cnames,0)
 

    def OnOkBtnButton(self, event):
        self.Close()
        event.Skip()

    def checkConnection(self,newCon):
        """This function checks for duplicate connections on both components"""
        for c in self.active_comp.connections:
            if c.remoteComp.uuid == newCon.remoteComp.uuid and \
                c.localPort.name == newCon.localPort.name and \
                c.remotePort.name == newCon.remotePort.name and \
                c.localPort.type == newCon.localPort.type:
                    
                return False,self.active_comp.name
                
        for c in newCon.remoteComp.connections:
            if c.remoteComp.uuid == self.active_comp.uuid and \
                c.localPort.name == newCon.remotePort.name and \
                c.remotePort.name == newCon.localPort.name and \
                c.localPort.type == newCon.remotePort.type:
                    
                return False,newCon.remoteComp.name
            
        return True,''

    def OnSrcBoxLeftUp(self, event):
        sn = self.srcBox.GetSelection()
        if self.srcBox.GetItemParent(sn) == self.srcBox.GetRootItem():
            tempInt = self.srcBox.GetPyData(sn)
            self.intLabelSrc.SetLabel(tempInt.interface.name)
        else:
            self.intLabelSrc.SetLabel('')
            return
        event.Skip()

    def OnDstBoxLeftUp(self, event):
        sn = self.dstBox.GetSelection()
        if sn == self.dstBox.GetRootItem():
            self.intLabelDst.SetLabel('')
            #return
        elif self.dstBox.GetItemParent(sn) == self.dstBox.GetRootItem():
            self.intLabelDst.SetLabel('')
            #return
        else:
            tempP = self.dstBox.GetPyData(sn)
            if isinstance(tempP,ComponentClass.Port):
                self.intLabelDst.SetLabel(tempP.interface.name)
            #return
        event.Skip()
            
            
    def checkSrcBox(self):
        srcSel = self.srcBox.GetSelection()
        
        if srcSel == self.srcBox.GetRootItem():
            # nothing is selected in the source box
            errorMsg(self,"Please select a source Port")
            return False
        else:
            return True
        
    def checkDstBox(self):
        dstSel = self.dstBox.GetSelection()
        
        if dstSel == self.dstBox.GetRootItem():
            # nothing is selected in the source box
            errorMsg(self,"Please select a destination Port")
            return False
        elif self.dstBox.GetItemParent(dstSel) == self.dstBox.GetRootItem():
            # a main level component was selected for the destination
            errorMsg(self,"Invalid destination selection.")
            return False
        else:
            tmpP = self.dstBox.GetPyData(dstSel)
            if isinstance(tmpP,ComponentClass.Port):
                return True
            else:
                errorMsg(self,"Invalid destination selection.")
                return False
                
            
            
            
            
