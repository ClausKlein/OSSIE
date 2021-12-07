#Boa:Dialog:Dialog1

import wx
from errorMsg import *

def create(parent,nodes,name):
    return Dialog1(parent,nodes,name)

[wxID_DIALOG1, wxID_DIALOG1CANCEL, wxID_DIALOG1NAMEBOX, 
 wxID_DIALOG1NODECHOICE, wxID_DIALOG1OK, wxID_DIALOG1STATICTEXT1, 
 wxID_DIALOG1STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(7)]

class Dialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(891, 437), size=wx.Size(310, 222),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Set Node Info')
        self.SetClientSize(wx.Size(310, 222))
        self.SetMaxSize(wx.Size(310, 222))
        self.SetMinSize(wx.Size(310, 222))
        self.Center(wx.BOTH)

        self.nameBox = wx.TextCtrl(id=wxID_DIALOG1NAMEBOX, name=u'nameBox',
              parent=self, pos=wx.Point(25, 48), size=wx.Size(260, 25), style=0,
              value=u'')

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=u'Please enter an instance name for this device.',
              name='staticText1', parent=self, pos=wx.Point(20, 23),
              size=wx.Size(270, 17), style=0)

        self.nodeChoice = wx.Choice(choices=[], id=wxID_DIALOG1NODECHOICE,
              name=u'nodeChoice', parent=self, pos=wx.Point(75, 121),
              size=wx.Size(160, 27), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=u'Please choose a deployment node.', name='staticText2',
              parent=self, pos=wx.Point(53, 96), size=wx.Size(204, 17),
              style=0)

        self.ok = wx.Button(id=wx.ID_OK, label=u'OK', name=u'ok', parent=self,
              pos=wx.Point(200, 176), size=wx.Size(85, 30), style=0)
        self.ok.Bind(wx.EVT_BUTTON, self.OnOkButton, id=wx.ID_OK)

        self.cancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'cancel', parent=self, pos=wx.Point(100, 176),
              size=wx.Size(85, 30), style=0)

    def __init__(self, parent,nodes,name):
        self._init_ctrls(parent)
        self.nameBox.WriteText(name)
        self.nodeChoice.Clear()
        for x in nodes:
            self.nodeChoice.Append(x.name,x)
        
        if self.nodeChoice.GetCount() > 0:
            self.nodeChoice.SetSelection(0)

    def OnOkButton(self, event):
        pos = self.nodeChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            errorMsg(self,"You must select a deployment node.")
            return 
        tempLn = self.nameBox.GetLineText(0)
        if tempLn == '':
            errorMsg(self,'Invalid instance name.')
            return
        
        self.DeploymentNode = self.nodeChoice.GetClientData(pos)
        self.InstanceName = tempLn
        
        event.Skip()
        
