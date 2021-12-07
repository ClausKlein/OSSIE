#Boa:Dialog:PortDialog

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
import ComponentClass
import copy
from errorMsg import *
import importIDL

def create(parent):
    return PortDialog(parent)

[wxID_PORTDIALOG, wxID_PORTDIALOGCANCELBTN, wxID_PORTDIALOGIMPORTBTN, 
 wxID_PORTDIALOGINTBOX, wxID_PORTDIALOGOKBTN, wxID_PORTDIALOGPORTNAMEBOX, 
 wxID_PORTDIALOGSTATICTEXT1, wxID_PORTDIALOGSTATICTEXT2, 
 wxID_PORTDIALOGSTATICTEXT3, wxID_PORTDIALOGTYPECHOICE, 
] = [wx.NewId() for _init_ctrls in range(10)]

class PortDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_PORTDIALOG, name='PortDialog',
              parent=prnt, pos=wx.Point(797, 377), size=wx.Size(498, 342),
              style=wx.DEFAULT_DIALOG_STYLE, title='Add Port')
        self.SetClientSize(wx.Size(498, 342))
        self.Center(wx.BOTH)

        self.portNameBox = wx.TextCtrl(id=wxID_PORTDIALOGPORTNAMEBOX,
              name='portNameBox', parent=self, pos=wx.Point(275, 80),
              size=wx.Size(200, 25), style=0, value='')
        self.portNameBox.Enable(True)

        self.OkBtn = wx.Button(id=wxID_PORTDIALOGOKBTN, label='Ok',
              name='OkBtn', parent=self, pos=wx.Point(275, 291),
              size=wx.Size(85, 30), style=0)
        self.OkBtn.SetToolTipString(u'Ok')
        self.OkBtn.Bind(wx.EVT_BUTTON, self.OnOkBtnButton,
              id=wxID_PORTDIALOGOKBTN)

        self.staticText1 = wx.StaticText(id=wxID_PORTDIALOGSTATICTEXT1,
              label=u'Interface', name='staticText1', parent=self,
              pos=wx.Point(107, 23), size=wx.Size(81, 17), style=0)

        self.ImportBtn = wx.Button(id=wxID_PORTDIALOGIMPORTBTN, label=u'Import',
              name=u'ImportBtn', parent=self, pos=wx.Point(90, 291),
              size=wx.Size(85, 30), style=0)
        self.ImportBtn.SetToolTipString(u'Import an Interface')
        self.ImportBtn.Enable(True)
        self.ImportBtn.Bind(wx.EVT_BUTTON, self.OnImportBtnButton,
              id=wxID_PORTDIALOGIMPORTBTN)

        self.staticText2 = wx.StaticText(id=wxID_PORTDIALOGSTATICTEXT2,
              label=u'Port Name', name='staticText2', parent=self,
              pos=wx.Point(295, 56), size=wx.Size(100, 17), style=0)

        self.CancelBtn = wx.Button(id=wxID_PORTDIALOGCANCELBTN, label=u'Cancel',
              name=u'CancelBtn', parent=self, pos=wx.Point(394, 291),
              size=wx.Size(85, 30), style=0)
        self.CancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelBtnButton,
              id=wxID_PORTDIALOGCANCELBTN)

        self.typeChoice = wx.Choice(choices=["Uses", "Provides"],
              id=wxID_PORTDIALOGTYPECHOICE, name=u'typeChoice', parent=self,
              pos=wx.Point(275, 161), size=wx.Size(120, 27), style=0)
        self.typeChoice.Show(True)
        self.typeChoice.SetSelection(0)
        self.typeChoice.Bind(wx.EVT_CHOICE, self.OnChoice1Choice,
              id=wxID_PORTDIALOGTYPECHOICE)

        self.staticText3 = wx.StaticText(id=wxID_PORTDIALOGSTATICTEXT3,
              label=u'Port Type', name='staticText3', parent=self,
              pos=wx.Point(295, 136), size=wx.Size(100, 17), style=0)

        self.intBox = wx.TreeCtrl(id=wxID_PORTDIALOGINTBOX, name=u'intBox',
              parent=self, pos=wx.Point(16, 43), size=wx.Size(248, 229),
              style=wx.SIMPLE_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.active_comp = parent.active_comp
        self.Available_Ints = parent.Available_Ints
        self.display_ints()

    def OnOkBtnButton(self, event):
        tempLn = self.portNameBox.GetLineText(0)
                            
        if tempLn == '':
            errorMsg(self,'Please enter a port name!')
            return
            
        sn = self.intBox.GetSelection()
        if sn == self.intBox.GetRootItem() or self.intBox.GetItemParent(sn) == self.intBox.GetRootItem():
            errorMsg(self,'Please select an Interface!')
            return   
            
        tempType = self.typeChoice.GetSelection()
        if tempType == wx.NOT_FOUND:
            errorMsg(self,'Please select a Type!')
            return 
        if tempType == 0:
            typeS = "Uses"
        else:
            typeS = "Provides"
            
        for p in self.active_comp.ports:
            if tempLn == p.name and typeS == p.type:
                errorMsg(self,"Port name <" + tempLn + "> already in use as a '"+typeS+"' port.")
                return
        
        selectedInt = self.intBox.GetPyData(sn)
        
        tempP = ComponentClass.Port(tempLn,copy.deepcopy(selectedInt),typeS)
        self.active_comp.ports.append(tempP)
        self.Close()
        event.Skip()

    def display_ints(self):
        if len(self.Available_Ints)==0:
            dlg = wx.MessageDialog(self, 'There are no interfaces available.',
              'Error', wx.OK | wx.ICON_INFORMATION)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
            return
        self.intBox.DeleteAllItems()
        ns_list = {}
        troot = self.intBox.AddRoot("the_root")
        for i in self.Available_Ints:
            if i.nameSpace in ns_list:
                t1 = ns_list[i.nameSpace]
            else:
                t1 = self.intBox.AppendItem(troot,i.nameSpace)
                ns_list[i.nameSpace] = t1
                
            t2 = self.intBox.AppendItem(t1,i.name)
            self.intBox.SetPyData(t2,i)
            
        if self.intBox.GetChildrenCount(troot,recursively=False) > 0:
            cid1,cookie1 = self.intBox.GetFirstChild(troot)
            self.intBox.SortChildren(cid1)
            for x in range(self.intBox.GetChildrenCount(troot,recursively=False)-1):
                cid1,cookie1 = self.intBox.GetNextChild(troot,cookie1)
                self.intBox.SortChildren(cid1)

    def OnCancelBtnButton(self, event):
        self.Close()
        event.Skip()

    def OnChoice1Choice(self, event):
        event.Skip()

    def OnImportBtnButton(self, event):
        dlg = wx.FileDialog(self, "Choose an idl file to import", "/home", "", "*.idl", wx.OPEN)
        tmpPath = ''
        try:
            returnCode = dlg.ShowModal()
            if returnCode == wx.ID_OK:
                tmpPath = dlg.GetPath()
            elif returnCode == wx.ID_CANCEL:
                dlg.Destroy()
                return
        finally:
            dlg.Destroy()
        print dlg.GetMessage()
        
        newInts = importIDL.getInterfaces(tmpPath)
        tmpMsg = 'You will need to copy <' + tmpPath[(tmpPath.rfind('/')+1):]
        tmpMsg += '> to /usr/local/include/standardinterfaces in order to '
        tmpMsg += 'use the generated code.'
        dlg = wx.MessageDialog(self, tmpMsg,
          'Note', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
        try:
            returnCode = dlg.ShowModal()
            if returnCode == wx.ID_CANCEL:
                dlg.Destroy()
                return
        finally:
            dlg.Destroy()
        
        
        self.Available_Ints.extend(newInts)
        self.display_ints()
        
        event.Skip()
