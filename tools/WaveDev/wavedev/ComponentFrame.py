#Boa:Frame:CompFrame

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
import wx.gizmos
from wx.lib.anchors import LayoutAnchors
import wx.grid
import PortDialog
import os, shutil, commands
import importIDL
import ComponentClass as CC
from errorMsg import *
import XML_gen.component_gen as component_gen
import cPickle
import PropertiesDialog
import MainFrame
import string

def create(parent):
    return CompFrame(parent)

[wxID_COMPFRAME, wxID_COMPFRAMEACECHECKBOX, wxID_COMPFRAMETIMINGCHECKBOX, wxID_COMPFRAMEADDPORTBTN,
 wxID_COMPFRAMEADDPROP, wxID_COMPFRAMEASSEMBLYCCHECKBOX,
 wxID_COMPFRAMECLOSEBTN, wxID_COMPFRAMECOMPNAMEBOX, wxID_COMPFRAMECOMPDESCRBOX,
 wxID_COMPFRAMEDEVICECHOICE, wxID_COMPFRAMENODECHOICE, wxID_COMPFRAMEPORTBOX,
 wxID_COMPFRAMEPROPLIST, wxID_COMPFRAMEREMOVEBTN, wxID_COMPFRAMEREMOVEPROP,
 wxID_COMPFRAMESTATICTEXT1, wxID_COMPFRAMESTATICTEXT2,
 wxID_COMPFRAMESTATICTEXT3, wxID_COMPFRAMESTATICTEXT4,
 wxID_COMPFRAMESTATICTEXT5, wxID_COMPFRAMESTATICTEXT6,
 wxID_COMPFRAMESTATICTEXT7, wxID_COMPFRAMESTATICTEXT8, wxID_COMPFRAMESTATUSBARCOMPONENT,
 wxID_COMPFRAMESTATICLINE1, wxID_COMPFRAMETEMPLATECHOICE,
] = [wx.NewId() for _init_ctrls in range(26)]

[wxID_COMPFRAMEMENUFILENEW, wxID_COMPFRAMEMENUFILEOPEN,
 wxID_COMPFRAMEMENUFILESAVE, wxID_COMPFRAMEMENUFILESAVEAS,
] = [wx.NewId() for _init_coll_menuFile_Items in range(4)]

[wxID_COMPFRAMEPORTBOXPOPUPADD, wxID_COMPFRAMEPORTBOXPOPUPEXPAND,
 wxID_COMPFRAMEPORTBOXPOPUPREMOVE,
] = [wx.NewId() for _init_coll_portBoxPopup_Items in range(3)]

[wxID_COMPFRAMEPROPLISTPOPUPADD, wxID_COMPFRAMEPROPLISTPOPUPEDIT,
 wxID_COMPFRAMEPROPLISTPOPUPREMOVE,
] = [wx.NewId() for _init_coll_propListPopup_Items in range(3)]

[wxID_COMPFRAMEMENUCOMPONENTGENERATE] = [wx.NewId() for _init_coll_menuComponent_Items in range(1)]

class CompFrame(wx.Frame):
    def _init_coll_menuComponent_Items(self, parent):
        # generated method, don't edit

        parent.Append(help=u'', id=wxID_COMPFRAMEMENUCOMPONENTGENERATE,
              kind=wx.ITEM_NORMAL, text=u'Generate Component')
        self.Bind(wx.EVT_MENU, self.OnMenuComponentGenerateMenu,
              id=wxID_COMPFRAMEMENUCOMPONENTGENERATE)

    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menuFile, title='File')
        parent.Append(menu=self.menuComponent, title=u'Component')

    def _init_coll_imageListPorts_Images(self, parent):
        # generated method, don't edit

        root = __file__
        if os.path.islink (root):
              root = os.path.realpath (root)
        root = os.path.dirname (os.path.abspath (root))
        parent.Add(bitmap=wx.Bitmap(root + '/images/uses.bmp', wx.BITMAP_TYPE_BMP),
              mask=wx.NullBitmap)
        parent.Add(bitmap=wx.Bitmap(root+ '/images/provides.bmp', wx.BITMAP_TYPE_BMP),
              mask=wx.NullBitmap)

    def _init_coll_menuFile_Items(self, parent):
        # generated method, don't edit
        parent.Append(help='', id=wxID_COMPFRAMEMENUFILENEW,
              kind=wx.ITEM_NORMAL, text='New')
        parent.Append(help='', id=wxID_COMPFRAMEMENUFILEOPEN,
              kind=wx.ITEM_NORMAL, text=u'Open')
        parent.Append(help='', id=wxID_COMPFRAMEMENUFILESAVE,
              kind=wx.ITEM_NORMAL, text='Save')
        parent.Append(help='', id=wxID_COMPFRAMEMENUFILESAVEAS,
              kind=wx.ITEM_NORMAL, text='Save As')
        self.Bind(wx.EVT_MENU, self.OnMenuFileSaveasMenu,
              id=wxID_COMPFRAMEMENUFILESAVEAS)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSaveMenu,
              id=wxID_COMPFRAMEMENUFILESAVE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileNewMenu,
              id=wxID_COMPFRAMEMENUFILENEW)
        self.Bind(wx.EVT_MENU, self.OnMenuFileOpenMenu,
              id=wxID_COMPFRAMEMENUFILEOPEN)

    def _init_coll_portBoxPopup_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_COMPFRAMEPORTBOXPOPUPADD,
              kind=wx.ITEM_NORMAL, text=u'Add')
        parent.Append(help='', id=wxID_COMPFRAMEPORTBOXPOPUPREMOVE,
              kind=wx.ITEM_NORMAL, text=u'Remove')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_COMPFRAMEPORTBOXPOPUPEXPAND,
              kind=wx.ITEM_NORMAL, text=u'Expand All')
        self.Bind(wx.EVT_MENU, self.OnPortBoxPopupRemoveMenu,
              id=wxID_COMPFRAMEPORTBOXPOPUPREMOVE)
        self.Bind(wx.EVT_MENU, self.OnPortBoxPopupExpandMenu,
              id=wxID_COMPFRAMEPORTBOXPOPUPEXPAND)
        self.Bind(wx.EVT_MENU, self.OnPortBoxPopupAddMenu,
              id=wxID_COMPFRAMEPORTBOXPOPUPADD)

    def _init_coll_propListPopup_Items(self, parent):

        parent.Append(help='', id=wxID_COMPFRAMEPROPLISTPOPUPADD,
              kind=wx.ITEM_NORMAL, text=u'Add')
        parent.Append(help='', id=wxID_COMPFRAMEPROPLISTPOPUPREMOVE,
              kind=wx.ITEM_NORMAL, text=u'Remove')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_COMPFRAMEPROPLISTPOPUPEDIT,
              kind=wx.ITEM_NORMAL, text=u'Edit')
        self.Bind(wx.EVT_MENU, self.OnPropsListPopupRemoveMenu,
              id=wxID_COMPFRAMEPROPLISTPOPUPREMOVE)
        self.Bind(wx.EVT_MENU, self.OnPropsListPopupEditMenu,
              id=wxID_COMPFRAMEPROPLISTPOPUPEDIT)
        self.Bind(wx.EVT_MENU, self.OnPropsListPopupAddMenu,
              id=wxID_COMPFRAMEPROPLISTPOPUPADD)

    def _init_coll_propList_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Properties', width=155)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Values', width=155)

    def _init_utils(self):
        # generated method, don't edit
        self.menuFile = wx.Menu(title='')

        self.menuComponent = wx.Menu(title='')

        self.menuBar1 = wx.MenuBar()

        self.portBoxPopup = wx.Menu(title='')

        self.propListPopup = wx.Menu(title='')

        self.imageListPorts = wx.ImageList(height=16, width=16)
        self._init_coll_imageListPorts_Images(self.imageListPorts)

        self._init_coll_menuFile_Items(self.menuFile)
        self._init_coll_menuComponent_Items(self.menuComponent)
        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_portBoxPopup_Items(self.portBoxPopup)
        self._init_coll_propListPopup_Items(self.propListPopup)

    def _init_ctrls(self, prnt, _availableTemplates):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_COMPFRAME, name='CompFrame',
              parent=prnt, pos=wx.Point(553, 276), size=wx.Size(656, 544),
              style=wx.DEFAULT_FRAME_STYLE, title=u'OSSIE Component Editor')
        self._init_utils()
        self.SetClientSize(wx.Size(856, 544))
        self.SetMenuBar(self.menuBar1)
#        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnCompFrameClose)
        self.Bind(wx.EVT_ACTIVATE, self.OnCompFrameActivate)

        self.statusBarComponent = wx.StatusBar(id=wxID_COMPFRAMESTATUSBARCOMPONENT,
              name='statusBarComponent', parent=self, style=0)
        self.SetStatusBar(self.statusBarComponent)

        self.AddPortBtn = wx.Button(id=wxID_COMPFRAMEADDPORTBTN, label='Add Port',
              name='AddPortBtn', parent=self, pos=wx.Point(387, 216),
              size=wx.Size(100, 30), style=0)
        self.AddPortBtn.Bind(wx.EVT_BUTTON, self.OnAddPortBtnButton,
              id=wxID_COMPFRAMEADDPORTBTN)

        self.RemoveBtn = wx.Button(id=wxID_COMPFRAMEREMOVEBTN, label='Remove Port',
              name='RemoveBtn', parent=self, pos=wx.Point(387, 259),
              size=wx.Size(100, 30), style=0)
        self.RemoveBtn.Bind(wx.EVT_BUTTON, self.OnRemoveBtnButton,
              id=wxID_COMPFRAMEREMOVEBTN)

        self.addProp = wx.Button(id=wxID_COMPFRAMEADDPROP, label=u'Add Property',
              name=u'addProp', parent=self, pos=wx.Point(384, 356),
              size=wx.Size(100, 30), style=0)
        self.addProp.Enable(True)
        self.addProp.Bind(wx.EVT_BUTTON, self.OnaddPropButton,
              id=wxID_COMPFRAMEADDPROP)

        self.removeProp = wx.Button(id=wxID_COMPFRAMEREMOVEPROP,
              label=u'Remove Property', name=u'removeProp', parent=self,
              pos=wx.Point(384, 404), size=wx.Size(140, 32), style=0)
        self.removeProp.Enable(True)
        self.removeProp.Bind(wx.EVT_BUTTON, self.OnRemovePropButton,
              id=wxID_COMPFRAMEREMOVEPROP)

        self.staticText2 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT2,
              label='Ports', name='staticText2', parent=self, pos=wx.Point(167,
              89), size=wx.Size(65, 17), style=0)

        self.CloseBtn = wx.Button(id=wxID_COMPFRAMECLOSEBTN, label='Close',
              name='CloseBtn', parent=self, pos=wx.Point(530, 424),
              size=wx.Size(85, 32), style=0)
        self.CloseBtn.Bind(wx.EVT_BUTTON, self.OnCloseBtnButton,
              id=wxID_COMPFRAMECLOSEBTN)

        self.TimingcheckBox = wx.CheckBox(id=wxID_COMPFRAMETIMINGCHECKBOX,
              label=u'Timing Port Support', name=u'TimingcheckBox', parent=self,
              pos=wx.Point(634, 126), size=wx.Size(185, 21), style=0)
        self.TimingcheckBox.SetValue(False)
        self.TimingcheckBox.Bind(wx.EVT_CHECKBOX, self.OnTimingcheckBoxCheckbox,
              id=wxID_COMPFRAMETIMINGCHECKBOX)

        self.ACEcheckBox = wx.CheckBox(id=wxID_COMPFRAMEACECHECKBOX,
              label=u'ACE Support', name=u'ACEcheckBox', parent=self,
              pos=wx.Point(634, 157), size=wx.Size(125, 21), style=0)
        self.ACEcheckBox.SetValue(False)
        self.ACEcheckBox.Bind(wx.EVT_CHECKBOX, self.OnACEcheckBoxCheckbox,
              id=wxID_COMPFRAMEACECHECKBOX)

        self.PortBox = wx.TreeCtrl(id=wxID_COMPFRAMEPORTBOX, name=u'PortBox',
              parent=self, pos=wx.Point(40, 112), size=wx.Size(312, 185),
              style=wx.SIMPLE_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.PortBox.SetImageList(self.imageListPorts)
        self.PortBox.SetBestFittingSize(wx.Size(312, 185))
        self.PortBox.Bind(wx.EVT_RIGHT_UP, self.OnPortBoxRightUp)

        self.AssemblyCcheckBox = wx.CheckBox(id=wxID_COMPFRAMEASSEMBLYCCHECKBOX,
              label=u'Assembly Controller', name=u'AssemblyCcheckBox',
              parent=self, pos=wx.Point(384, 126), size=wx.Size(165, 21),
              style=0)
        self.AssemblyCcheckBox.SetValue(False)
        self.AssemblyCcheckBox.Bind(wx.EVT_CHECKBOX,
              self.OnAssemblyCcheckBoxCheckbox,
              id=wxID_COMPFRAMEASSEMBLYCCHECKBOX)

        self.compNameBox = wx.TextCtrl(id=wxID_COMPFRAMECOMPNAMEBOX,
              name=u'compNameBox', parent=self, pos=wx.Point(138, 10),
              size=wx.Size(215, 25), style=0, value=u'')

        self.staticText1 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT1,
              label=u'Component Name:', name='staticText1', parent=self,
              pos=wx.Point(24, 13), size=wx.Size(110, 17), style=0)

        self.compDescrBox = wx.TextCtrl(id=wxID_COMPFRAMECOMPDESCRBOX,
              name=u'compDescrBox', parent=self, pos=wx.Point(110, 40),
              size=wx.Size(243, 50), style=wx.TE_BESTWRAP | wx.TE_MULTILINE, value=u'')

        self.staticText1_1 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT8,
              label=u'Description:', name='staticText8', parent=self,
              pos=wx.Point(24, 43), size=wx.Size(110, 17), style=0)

        self.deviceChoice = wx.Choice(choices=[], id=wxID_COMPFRAMEDEVICECHOICE,
              name=u'deviceChoice', parent=self, pos=wx.Point(453, 93),
              size=wx.Size(136, 28), style=0)
        self.deviceChoice.SetBestFittingSize(wx.Size(136, 28))
        self.deviceChoice.Bind(wx.EVT_CHOICE, self.OnDeviceChoiceChoice,
              id=wxID_COMPFRAMEDEVICECHOICE)

        self.staticText3 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT3,
              label=u'Waveform Deployment Settings', name='staticText3', parent=self,
              pos=wx.Point(384, 24), size=wx.Size(100, 35), style=wx.TE_BESTWRAP | wx.TE_MULTILINE)

        self.staticText3.SetFont(wx.Font(8,wx.SWISS,wx.NORMAL,wx.BOLD,True,u'Sans'))

        self.nodeChoice = wx.Choice(choices=[], id=wxID_COMPFRAMENODECHOICE,
              name=u'nodeChoice', parent=self, pos=wx.Point(453, 60),
              size=wx.Size(136, 28), style=0)
        self.nodeChoice.Bind(wx.EVT_CHOICE, self.OnNodeChoiceChoice,
              id=wxID_COMPFRAMENODECHOICE)

        self.staticText4 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT4,
              label=u'Node', name='staticText4', parent=self, pos=wx.Point(384,
              65), size=wx.Size(41, 17), style=0)

        self.staticText5 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT5,
              label=u'Device', name='staticText5', parent=self,
              pos=wx.Point(384, 98), size=wx.Size(51, 17), style=0)

        self.staticText6 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT6,
              label=u'Component Generation Options', name='staticText6', parent=self,
              pos=wx.Point(634, 24), size=wx.Size(100, 35), style=wx.TE_BESTWRAP | wx.TE_MULTILINE)
        self.staticText6.SetFont(wx.Font(8,wx.SWISS,wx.NORMAL,wx.BOLD,True,u'Sans'))

        self.staticText7 = wx.StaticText(id=wxID_COMPFRAMESTATICTEXT7,
              label=u'Template', name='staticText7', parent=self,
              pos=wx.Point(634, 65), size=wx.Size(222, 17), style=0)

        self.propList = wx.ListView(id=wxID_COMPFRAMEPROPLIST, name=u'propList',
              parent=self, pos=wx.Point(40, 320), size=wx.Size(312, 160),
              style=wx.LC_SINGLE_SEL | wx.VSCROLL | wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.SIMPLE_BORDER)
        self.propList.SetBestFittingSize(wx.Size(312, 160))
        self._init_coll_propList_Columns(self.propList)
        #self.propList.Bind(wx.EVT_RIGHT_UP, self.OnPropListRightUp)
        self.propList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnPropListListItemRightClick)
        self.propList.Bind(wx.EVT_LEFT_DCLICK,self.OnPropListLeftDclick)

        self.staticLine1 = wx.StaticLine(id=wxID_COMPFRAMESTATICLINE1,
              name='staticLine1', parent=self, pos=wx.Point(610, 17),
              size=wx.Size(1, 200), style=wx.LI_VERTICAL)

        self.templateChoice = wx.Choice(choices=_availableTemplates,
              id=wxID_COMPFRAMETEMPLATECHOICE,
              name=u'templateChoice', parent=self, pos=wx.Point(703, 60),
              size=wx.Size(136, 28), style=0)
        self.templateChoice.SetBestFittingSize(wx.Size(136, 28))
        self.templateChoice.Bind(wx.EVT_CHOICE, self.OnTemplateChoiceChoice,
              id=wxID_COMPFRAMETEMPLATECHOICE)

    def __init__(self, parent):
        # Constructor for ComponentFrame
        self.wavedevPath = os.getcwd() + os.sep

        self.wavedevPath = __file__
        if os.path.islink (self.wavedevPath):
            self.wavedevPath = os.path.realpath (self.wavedevPath)
        self.wavedevPath = os.path.dirname (os.path.abspath (self.wavedevPath)) 

        #NOTE: There still may be a better way to do this,
        # assuming generate/templates always exists below this file, this will work
        path = self.wavedevPath + '/generate/templates'
        availableTemplates = commands.getoutput("ls -I __init__.py* " + path)
        availableTemplates = availableTemplates.split()
        self._init_ctrls(parent,availableTemplates)

        self.templateChoice.SetSelection(0)
        self.template = self.templateChoice.GetStringSelection()

        self.parent = parent

        self.saveComponentPath = None
        self.calledByParent = False

        if parent == None:  #OSSIE Component Editor being run in stand-alone mode
            self.menuComponent.Enable(wxID_COMPFRAMEMENUCOMPONENTGENERATE,True)
            self.compDescrBox.Enable(True)
            MainFrame.LoadConfiguration(self)
        else:
            self.menuComponent.Enable(wxID_COMPFRAMEMENUCOMPONENTGENERATE,False)
            self.compDescrBox.Enable(False)

        self.Available_Ints = []
        self.importStandardIdl()


    def OnCompFrameActivate(self, event):
        if self.calledByParent == True:
            self.active_comp = self.parent.active_comp
            self.displayPorts()
            self.displayProps()

            if self.active_comp.ace == True:
                self.ACEcheckBox.SetValue(True)
            else:
                self.ACEcheckBox.SetValue(False)

            if self.active_comp.timing == True:
                self.TimingcheckBox.SetValue(True)
            else:
                self.TimingcheckBox.SetValue(False)

            if self.active_comp.AssemblyController == True:
                self.AssemblyCcheckBox.SetValue(True)
            else:
                self.AssemblyCcheckBox.SetValue(False)

            if self.active_comp.generate == False:
                self.AddPortBtn.Enable(False)
                self.RemoveBtn.Enable(False)
                self.addProp.Enable(False)
                self.removeProp.Enable(False)
                self.ACEcheckBox.Enable(False)
                self.TimingcheckBox.Enable(False)
            else:
                self.AddPortBtn.Enable(True)
                self.RemoveBtn.Enable(True)
                self.addProp.Enable(True)
                self.removeProp.Enable(True)
                self.ACEcheckBox.Enable(True)
                self.TimingcheckBox.Enable(True)

            self.compNameBox.Clear()
            self.compNameBox.WriteText(self.active_comp.name)

            self.compDescrBox.Clear()
            self.compDescrBox.WriteText(self.active_comp.description)

            if self.active_comp.type != 'resource':
                self.deviceChoice.Clear()
                self.deviceChoice.Enable(False)
                self.nodeChoice.Enable(False)
            else:
                self.deviceChoice.Enable(True)
                self.nodeChoice.Enable(True)
                self.displayPlatformInfo()

            self.menuFile.Enable(wxID_COMPFRAMEMENUFILENEW,False)
            self.menuFile.Enable(wxID_COMPFRAMEMENUFILEOPEN,False)

            self.calledByParent = False


################################################################################
## File Menu / Frame Functionality
################################################################################
    def OnMenuFileSaveasMenu(self, event):
        self.ComponentSave(True)
        event.Skip()

    def OnMenuFileSaveMenu(self, event):
        self.ComponentSave(False)
        event.Skip()

    def OnMenuFileNewMenu(self, event):
        self.active_comp = CC.Component("component1")
        self.ACEcheckBox.SetValue(False)
        self.TimingcheckBox.SetValue(False)
        self.AssemblyCcheckBox.SetValue(False)
        self.AddPortBtn.Enable(True)
        self.RemoveBtn.Enable(True)
        self.displayPorts()
        self.compNameBox.Clear()
        self.compNameBox.WriteText(self.active_comp.name)
        self.compDescrBox.Clear()
        self.compDescrBox.WriteText("Enter brief description of component")
        event.Skip()

    def OnMenuFileOpenMenu(self, event):
        if len(self.homeDir) > 0:
            tmpdir = self.homeDir
        else:
            tmpdir = os.path.expanduser("~")
            if tmpdir == "~":
                tmpdir = "/home"

        tmpwildcard = "Component Files (*.cmp)|*.cmp"
        dlg = wx.FileDialog(self, "Choose a file", tmpdir, "", tmpwildcard, wx.OPEN)
        try:
            returnCode = dlg.ShowModal()
            if returnCode == wx.ID_OK:
                tmpPath = dlg.GetPath()
            elif returnCode == wx.ID_CANCEL:
                dlg.Destroy()
                return
        finally:
            dlg.Destroy()

        f = open(tmpPath,'r')
        tmpObject = cPickle.load(f)
        if tmpObject[0] == 'component':
            self.ComponentOpen(tmpPath,tmpObject[1])

        event.Skip()

    def ComponentSave(self,saveasFlag):
        if saveasFlag == True or self.saveComponentPath == None:
            tempLn = self.compNameBox.GetLineText(0)
            if tempLn == '':
                errorMsg(self,'Please enter a component name first')
                return
            self.active_comp.name = tempLn

            tempDescr = self.compDescrBox.GetLineText(0)
            if tempDescr == '':
                errorMsg(self,'Please enter a component description first')
                return
            self.active_comp.description = tempDescr

            if len(self.homeDir) > 0:
                tmpdir = self.homeDir
            else:
                tmpdir = os.path.expanduser("~")
                if tmpdir == "~":
                    tmpdir = "/home"

            dlg = wx.FileDialog(self, "Choose a file", tmpdir, tempLn + '.cmp', "Component File (*.cmp)|*.cmp", wx.SAVE)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_OK:
                    self.saveComponentPath = dlg.GetPath()
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    return
            finally:
                dlg.Destroy()

        f = open(self.saveComponentPath,'w')
        cPickle.dump(('component',self.active_comp),f)

    def ComponentOpen(self,newPath,newComp):
        if newPath != None:
            if self.saveComponentPath != None:
                dlg = wx.MessageDialog(self, 'Do you want to save your changes to the active component first?',
                      'Error', wx.YES_NO | wx.ICON_INFORMATION)
                try:
                    returnCode = dlg.ShowModal()
                    if returnCode == wx.ID_YES:
                        self.ComponentSave(False)
                    elif returnCode == wx.ID_CANCEL:
                        dlg.Destroy()
                        return
                finally:
                    dlg.Destroy()

            self.saveComponentPath = newPath

        self.active_comp = newComp
        self.displayPorts()
        self.displayProps()

        if self.active_comp.ace == True:
            self.ACEcheckBox.SetValue(True)
        else:
            self.ACEcheckBox.SetValue(False)

        if not hasattr(self.active_comp,'timing'):
            self.active_comp.timing = False
        if self.active_comp.timing == True:
            self.TimingcheckBox.SetValue(True)
        else:
            self.TimingcheckBox.SetValue(False)

        if self.active_comp.AssemblyController == True:
            self.AssemblyCcheckBox.SetValue(True)
        else:
            self.AssemblyCcheckBox.SetValue(False)

        if self.active_comp.generate == False:
            self.AddPortBtn.Enable(False)
            self.RemoveBtn.Enable(False)
        else:
            self.AddPortBtn.Enable(True)
            self.RemoveBtn.Enable(True)

        self.compNameBox.Clear()
        self.compNameBox.WriteText(self.active_comp.name)

        self.compDescrBox.Clear()
        self.compDescrBox.WriteText(self.active_comp.description)

    def OnCloseBtnButton(self, event):
        if self.parent == None:
            self.Show(False)
            self.Close()
            return
        tempLn = self.compNameBox.GetLineText(0)
        if tempLn == '':
            errorMsg(self,'Please enter a component name first')
            return

        for c in self.parent.active_wave.components:
            if c != self.active_comp and c.name == tempLn:
                errorMsg(self,'Invalid name - a component by that name already exists')
                return

        #Component names with spaces do not work
        if tempLn.find(' ') != -1:
            errorMsg(self,'Resource names can not have spaces in them.\nReplacing spaces with "_".')
            tempLn = tempLn.replace(' ','_')


        self.active_comp.changeName(tempLn)

        self.MakeModal(False)
        self.parent.displayComps()
        self.parent.displayNodes()
        self.Show(False)
        event.Skip()

    def OnCompFrameClose(self, event):
        self.MakeModal(False)
        if self.parent != None:
            self.parent.displayComps()
        self.Show(False)
        event.Skip()


################################################################################
## Miscellaneous Functionality
################################################################################

    def importStandardIdl(self):
        '''Imports IDL from cf, standardinterfaces, and custominterfaces'''
        #temporarily change self.parent to self so this works
        #normally this function looks at the MainFrame - but not in standalone
        changedParent = False
        if self.parent == None:
            self.parent = self
            changedParent = True

        if os.path.isfile(self.parent.ossieIncludePath + "cf.idl"):
            cfIdl_file = self.parent.ossieIncludePath + "cf.idl"
        else:
            tmpstr = "Cannot find cf.idl in the OSSIE installation location:\n"
            tmpstr += self.parent.ossieIncludePath
            errorMsg(self.parent,tmpstr)

        # for each file in the standardinterfaces directory, import all available
        # interfaces (skip standardIdl files)

        standard_idl_list = os.listdir(self.parent.stdIdlPath)

        try:
            custom_idl_list = os.listdir(self.parent.customIdlPath)
        except OSError: # this will occur if customIdlPath was never set
                        # as a result of customInterfaces not being found
            custom_idl_list = []

        if len(standard_idl_list) <= 0:
            tmpstr = "Can't find any files in: " + self.parent.stdIdlPath
            errorMsg(self.parent,tmpstr)
            return

        # Add the CF interfaces first - in case another file includes them, we
        # don't want them asscociated with anything other than cf.idl
        self.Available_Ints.extend(importIDL.getInterfaces(cfIdl_file))

        # import standard interfaces
        for standard_idl_file in standard_idl_list:
            # standardIdl files are not included because they are aggregates of the other interfaces
            if 'standardIdl' in standard_idl_file:
                continue

            if string.lower(os.path.splitext(standard_idl_file)[1]) != ".idl":
                # ignore non idl files
                continue

            tempInts = importIDL.getInterfaces(self.parent.stdIdlPath+standard_idl_file)
            for t in tempInts:
                if t not in self.Available_Ints:
                    self.Available_Ints.append(t)

        # import custom interfaces
        for custom_idl_file in custom_idl_list:
            # ignore aggregate 'customInterfaces.idl' file
            if 'customInterfaces' in custom_idl_file:
                continue

            if string.lower(os.path.splitext(custom_idl_file)[1]) != ".idl":
                # ignore non idl files
                continue

            tempInts = importIDL.getInterfaces(self.parent.customIdlPath+custom_idl_file)
            for t in tempInts:
                if t not in self.Available_Ints:
                   # print "Testing: " + t.name + " " + idl_file + " " + str(len(self.Available_Ints))
                    self.Available_Ints.append(t)
                    if t.name == 'timingStatus':
                        self.timing_interface = CC.Interface(t.name, t.nameSpace, t.operations, t.filename, t.fullpath)
                        self.timing_port = CC.Port('send_timing_report', self.timing_interface, "Uses", "data")
#                    print "CF.py: " + t.name + "  " + str(len(t.operations))

        if changedParent == True:
            self.parent = None



    def OnACEcheckBoxCheckbox(self, event):
        if self.ACEcheckBox.GetValue() == True:
            self.active_comp.ace = True
        else:
            self.active_comp.ace = False
        event.Skip()

    def OnTimingcheckBoxCheckbox(self, event):
        if self.TimingcheckBox.GetValue() == True:
            self.active_comp.timing = True
        else:
            self.active_comp.timing = False
        event.Skip()

    def OnAssemblyCcheckBoxCheckbox(self, event):
        if self.AssemblyCcheckBox.GetValue() == True:
            if self.parent != None:
                for x in self.parent.active_wave.components:
                    x.AssemblyController = False
            self.active_comp.AssemblyController = True
        else:
            self.active_comp.AssemblyController = False
        event.Skip()

################################################################################
## Port Functionality
################################################################################

    def displayPorts(self):
        self.PortBox.DeleteAllItems()
        troot = self.PortBox.AddRoot("the_root")
        usesRoot = self.PortBox.AppendItem(troot,'Uses',image=0)
        provRoot = self.PortBox.AppendItem(troot,'Provides',image=1)

        for p in self.active_comp.ports:
            if p.type == 'Uses':
                tnm = p.name + "::" + p.interface.name
                t1 = self.PortBox.AppendItem(usesRoot,tnm)
                self.PortBox.SetPyData(t1,p)

            if p.type == 'Provides':
                tnm = p.name + "::" + p.interface.name
                t2 = self.PortBox.AppendItem(provRoot,tnm)
                self.PortBox.SetPyData(t2,p)
        self.PortBox.Expand(usesRoot)
        self.PortBox.Expand(provRoot)

    def AddPort(self):
        if self.active_comp.generate == False:
            return
        dlg = PortDialog.create(self)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

        self.displayPorts()

    def RemovePort(self):
        if self.active_comp.generate == False:
            return
        dlg = wx.MessageDialog(self, '("Are you sure you want to remove this port?")',
          'Error', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        try:
            if dlg.ShowModal() == wx.ID_NO:
                return
        finally:
            dlg.Destroy()

        sn = self.PortBox.GetSelection()
        if sn == self.PortBox.GetRootItem():
            return
        elif self.PortBox.GetItemParent(sn) == self.PortBox.GetRootItem():
            # a main level component
            return
        else:
            # a child component (port)
            tc = self.PortBox.GetPyData(sn)
            ti = self.active_comp.ports.index(tc)
            del self.active_comp.ports[ti]

        self.displayPorts()


    def OnAddPortBtnButton(self, event):
        self.AddPort()
        event.Skip()

    def OnRemoveBtnButton(self, event):
        self.RemovePort()
        event.Skip()

    def OnPortBoxPopupExpandMenu(self, event):
        troot = self.PortBox.GetRootItem()
        cid1,cookie1 = self.PortBox.GetFirstChild(troot)
        cid2,cookie2 = self.PortBox.GetNextChild(troot,cookie1)
        self.PortBox.Expand(cid1)
        self.PortBox.Expand(cid2)
        event.Skip()

    def OnPortBoxRightUp(self, event):
        sn = self.PortBox.GetSelection()

        if sn == self.PortBox.GetRootItem():
            self.portBoxPopup.Enable(wxID_COMPFRAMEPORTBOXPOPUPREMOVE,False)
        elif self.PortBox.GetItemParent(sn) == self.PortBox.GetRootItem():
            # a main level item
            self.portBoxPopup.Enable(wxID_COMPFRAMEPORTBOXPOPUPREMOVE,False)
        else:
            # a child component (ports in our case)
            for x in self.portBoxPopup.GetMenuItems():
                x.Enable(True)

        if self.active_comp.generate == False:
            self.portBoxPopup.Enable(wxID_COMPFRAMEPORTBOXPOPUPADD,False)
            self.portBoxPopup.Enable(wxID_COMPFRAMEPORTBOXPOPUPREMOVE,False)
        else:
            self.portBoxPopup.Enable(wxID_COMPFRAMEPORTBOXPOPUPADD,True)

        self.PortBox.PopupMenu(self.portBoxPopup)
        event.Skip()

    def OnPortBoxPopupRemoveMenu(self, event):
        self.RemovePort()
        event.Skip()

    def OnPortBoxPopupAddMenu(self, event):
        self.AddPort()
        event.Skip()



################################################################################
## Deployment Functionality
################################################################################

    def displayDevices(self):
        if self.parent == None:
            return

        pos = self.nodeChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            return

        tmpNode = self.nodeChoice.GetClientData(pos)


        self.deviceChoice.Clear()
        for x in tmpNode.Devices:
            if x.type == 'executabledevice' or x.type == 'loadabledevice':
                self.deviceChoice.Append(unicode(x.name),x)

    def displayPlatformInfo(self):
        if self.parent == None:
            return

        self.deviceChoice.Clear()
        self.nodeChoice.Clear()

        for x in self.parent.active_plat.nodes:
            self.nodeChoice.Append(x.name,x)

        tmpNode = None
        if self.active_comp.device != None:
            for x in self.parent.active_plat.nodes:
                for d in x.Devices:
                    if d == self.active_comp.device:
                        tmpNode = x
            if tmpNode != None:
                pos = self.nodeChoice.FindString(tmpNode.name)
                self.nodeChoice.SetSelection(pos)
                for d in tmpNode.Devices:
                    self.deviceChoice.Append(d.name,d)
                pos = self.deviceChoice.FindString(self.active_comp.device.name)
                self.deviceChoice.SetSelection(pos)

            else:
                tmpstr = 'ERROR! Cannot find the ' + self.active_comp.device.name
                tmpstr += ' device in current Platform configuration.'
                tmpstr += '\nSetting device assignment to None.'
                errorMsg(self,tmpstr)
                self.active_comp.device = None

    def OnNodeChoiceChoice(self, event):
        pos = self.nodeChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            return
        self.displayDevices()

    def OnDeviceChoiceChoice(self, event):
        pos = self.deviceChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            return

        tmpDev = self.deviceChoice.GetClientData(pos)
        self.active_comp.device = tmpDev

    def OnTemplateChoiceChoice(self, event):
        pos = self.templateChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            return

        tmpTmpl = self.templateChoice.GetStringSelection()
        self.template = tmpTmpl


    ############################################################################
    ## Properties Functionality
    ############################################################################
    def OnaddPropButton(self, event):
        self.AddProperty()
        event.Skip()

    def OnRemovePropButton(self, event):
        #sel = self.propList.GetFirstSelected()
        self.RemoveProperty()
        event.Skip()

    def displayProps(self):
        self.propList.DeleteAllItems()
        pCount = 0
        for p in self.active_comp.properties:
            if p.elementType == "Simple":
                self.propList.InsertStringItem(pCount,p.name)
                self.propList.SetStringItem(pCount,1,str(p.value))
            if p.elementType == "SimpleSequence":
                self.propList.InsertStringItem(pCount,p.name)
                ts = "["
                for x in p.values:
                    ts += x + ","
                ts = ts[:-1] + "]"
                self.propList.SetStringItem(pCount,1,ts)
            self.propList.SetItemData(pCount,self.active_comp.properties.index(p))

    def OnPropListListItemRightClick(self, event):
        self.propList.PopupMenu(self.propListPopup)
        event.Skip()

    def EditProperty(self):
        sel = self.propList.GetFocusedItem()
        if self < 0:
            return
        item = self.propList.GetItem(sel)
        tmpind = item.GetData()                # the index of the property is stored with the item
        dlg = PropertiesDialog.create(self)
        dlg.active_prop = self.active_comp.properties[tmpind]
        dlg.editable = self.active_comp.generate
        dlg.calledByParent = True
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

        self.displayProps()

    def AddProperty(self):
        dlg = PropertiesDialog.create(self)
        dlg.active_prop = None
        dlg.editable = self.active_comp.generate
        dlg.calledByParent = True
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

        self.displayProps()

    def RemoveProperty(self):
        sel = self.propList.GetFocusedItem()
        if sel >= 0:
            tmpstr = "Are you sure you want to remove this property?"
            if owdMsg(self,tmpstr):
                for p in self.active_comp.properties:
                    if p.name == self.propList.GetItemText(sel):
                        ti = self.active_comp.properties.index(p)
                        del self.active_comp.properties[ti]
                        self.propList.DeleteItem(sel)
                        break
            self.displayProps()

    def OnPropsListPopupEditMenu(self, event):
        self.EditProperty()
        event.Skip()

    def OnPropsListPopupRemoveMenu(self, event):
        self.RemoveProperty()
        event.Skip()

    def OnPropsListPopupAddMenu(self, event):
        self.AddProperty()
        event.Skip()

    def OnPropListLeftDclick(self,event):
        self.EditProperty()
        event.Skip()

    ############################################################################
    ## Generate the Component XML and C++
    ############################################################################
    def OnMenuComponentGenerateMenu(self, event):

        #select which template to use
        if self.template == "basic_ports":
            import WaveDev.wavedev.generate.templates.basic_ports.genStructure as genStruct
        elif self.template == "custom_ports":
            import WaveDev.wavedev.generate.templates.custom_ports.genStructure as genStruct
        elif self.template == "py_comp":
            import WaveDev.wavedev.generate.templates.py_comp.genStructure as genStruct
        else:
            errorMsg(self.parent, self.template + " is not supported in OnMenuComponentGenerateMenu within the componentFrame")
            return

        tempLn = self.compNameBox.GetLineText(0)
        if tempLn == '':
            errorMsg(self,'Please enter a component name first')
            return

        self.active_comp.name = tempLn

        tempDescr = self.compDescrBox.GetLineText(0)
        if tempDescr == '':
            errorMsg(self,'Please enter a component description first')
            return

        self.active_comp.description = tempDescr

        dlg = wx.DirDialog(self)
        dlg.SetMessage("Please select the place to generate the code")
        dlg.SetPath(os.path.expanduser('~'))
        try:
            if dlg.ShowModal() == wx.ID_OK:
                savepath = dlg.GetPath()
            else:
                return
        finally:
            dlg.Destroy()

        if savepath[len(savepath)-1] != '/':
            savepath = savepath + '/'

        self.path = savepath
        self.path = self.path + self.active_comp.name

        if os.path.exists(self.path) == False:
                os.mkdir(self.path)

                #if os.path.exists(self.path + '/aclocal.d') == False:
                #    os.mkdir(self.path + '/aclocal.d')
                #for f in os.listdir('generate/aclocal.d/'):
                #    if not os.path.isdir(f):
                #        shutil.copy('generate/aclocal.d/' + f,self.path + '/aclocal.d')
                if self.template != "py_comp":
                    shutil.copy(self.wavedevPath + '/generate/reconf',self.path)
                    os.chmod(self.path + '/reconf', 0755)
                shutil.copy(self.wavedevPath + '/generate/LICENSE',self.path)

        if self.active_comp.timing:
                found_timing = False
                for p in self.active_comp.ports:
                        if p.interface.name == 'timingStatus':
                                found_timing = True
                if not found_timing:
                        self.active_comp.ports.append(self.timing_port)

        gen = genStruct.genAll(savepath, self.wavedevPath, None)
        gen.writeCompMakefile(self.active_comp,self.path)
        gen.writeConfAC(self.path, self.active_comp.name, self.active_comp.ace, False, self.installPath)
        gen.genCompFiles(self.active_comp)

        component_gen.gen_scd(self.active_comp, savepath, self.wavedevPath)
        component_gen.gen_spd(self.active_comp, savepath, self.wavedevPath)
        component_gen.gen_prf(self.active_comp, savepath, self.wavedevPath)

class App(wx.App):
    def OnInit(self):
        self.name = 'comp_frame_app'
        self.main = create(None)
        self.main.Show()

        #self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        self.ExitMainLoop()    # inherited from wx.App

def newComponentFrame():
    wx.InitAllImageHandlers()
    application = App()

    application.main.active_comp = CC.Component("component1")
    application.main.calledByParent = False
    application.main.displayPorts()
    application.main.compNameBox.WriteText("component1")
    application.main.compDescrBox.WriteText("Enter component description here")
    if application.main.active_comp.ace == True:
        application.main.ACEcheckBox.SetValue(True)
    else:
        application.main.ACEcheckBox.SetValue(False)

    if application.main.active_comp.timing == True:
        application.main.TimingcheckBox.SetValue(True)
    else:
        application.main.TimingcheckBox.SetValue(False)

    application.main.deviceChoice.Enable(False)
    application.main.nodeChoice.Enable(False)
    application.MainLoop()



################################################################################
## If Component Developer is run as a seperate application
################################################################################

if __name__ == "__main__":
    newComponentFrame()
