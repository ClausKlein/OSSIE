#Boa:Frame:Frame1

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
import ComponentFrame, ConnectDialog, AboutDialog
from wx.lib.anchors import LayoutAnchors
import ComponentClass, WaveformClass, PlatformClass
import sys, os, copy
import WaveDev.wavedev.generate.templates.custom_ports.genStructure as genStruct
import WaveDev.wavedev.XML_gen.application_gen as xml_gen
from errorMsg import *
import cPickle
import importResource
import importNode
import NodeDialog
import xml.dom.minidom
from xml.dom.minidom import Node
import generate.genNode as genNode
import webbrowser
#import WaveDev.wavedev.uuidgen
from WaveDev.wavedev.uuidgen import uuidgen
def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1COMPBOX, wxID_FRAME1NODEBOX, wxID_FRAME1RESOURCEBOX,
 wxID_FRAME1SASHWINDOW1, wxID_FRAME1SASHWINDOW2, wxID_FRAME1SASHWINDOW3,
 wxID_FRAME1SASHWINDOW4, wxID_FRAME1SPLITTERWINDOW1,
 wxID_FRAME1SPLITTERWINDOW2, wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2,
 wxID_FRAME1STATICTEXT3, wxID_FRAME1STATUSBAR1, wxID_FRAME1WAVENAMEBOX,
 wxID_REFRESHRESOURCEBTN, wxID_FRAME1COMPDESCRBOX, wxID_FRAME1STATICTEXT4
] = [wx.NewId() for _init_ctrls in range(18)]

[wxID_FRAME1MENUFILEEXIT, wxID_FRAME1MENUFILENEW, wxID_FRAME1MENUFILEOPEN,
 wxID_FRAME1MENUFILESAVE, wxID_FRAME1MENUFILESAVEPLATFORM,
 wxID_FRAME1MENUFILESAVEPLATFORMAS, wxID_FRAME1MENUFILESAVEWAVEFORM,
 wxID_FRAME1MENUFILESAVEWAVEFORMAS, wxID_FRAME1MENUFILESAVE_AS,
] = [wx.NewId() for _init_coll_menuFile_Items in range(9)]

[wxID_FRAME1COMPBOXPOPUPCONNECT, wxID_FRAME1COMPBOXPOPUPEDIT,
 wxID_FRAME1COMPBOXPOPUPEXPAND, wxID_FRAME1COMPBOXPOPUPREFRESH,
 wxID_FRAME1COMPBOXPOPUPREMOVE, wxID_FRAME1COMPBOXPOPUPRENAME,
 wxID_FRAME1COMPBOXPOPUPSET_AC,
] = [wx.NewId() for _init_coll_compBoxPopup_Items in range(7)]

[wxID_FRAME1MENUWAVEFORMACESUPPORT, wxID_FRAME1MENUWAVEFORMADDCOMP,
 wxID_FRAME1MENUWAVEFORMCONNECTCOMP, wxID_FRAME1MENUWAVEFORMEDITCOMP,
 wxID_FRAME1MENUWAVEFORMGENWAV, wxID_FRAME1MENUWAVEFORMREMOVECOMP,
] = [wx.NewId() for _init_coll_menuWaveform_Items in range(6)]

[wxID_FRAME1MENUHELPABOUT, wxID_FRAME1MENUHELPSAMPLEWAVEFORM,
] = [wx.NewId() for _init_coll_menuHelp_Items in range(2)]

[wxID_FRAME1RESOURCEBOXPOPUPDEVADD] = [wx.NewId() for _init_coll_resourceBoxPopupDev_Items in range(1)]

[wxID_FRAME1RESOURCEBOXPOPUPADD, wxID_FRAME1RESOURCEBOXPOPUPADDDEV, wxID_FRAME1RESOURCEBOXPOPUPADDNODE,
 wxID_FRAME1RESOURCEBOXPOPUPGETDESCR, wxID_FRAME1RESOURCEBOXPOPUPGETDOXYGENREFMAN,
] = [wx.NewId() for _init_coll_resourceBoxPopup_Items in range(5)]

[wxID_FRAME1NODEBOXPOPUPADDNODE, wxID_FRAME1NODEBOXPOPUPLOADNODE, wxID_FRAME1NODEBOXPOPUPEXPAND,
 wxID_FRAME1NODEBOXPOPUPREFRESH, wxID_FRAME1NODEBOXPOPUPREMOVE, wxID_FRAME1NODEBOXPOPUPGENERATE,
 wxID_FRAME1NODEBOXPOPUPCONNECT, wxID_FRAME1NODEBOXPOPUPRENAME,
] = [wx.NewId() for _init_coll_nodeBoxPopup_Items in range(8)]

[wxID_FRAME1NEWMENUNEWPLATFORM, wxID_FRAME1NEWMENUNEWPROJECT,
 wxID_FRAME1NEWMENUNEWWAVEFORM,
] = [wx.NewId() for _init_coll_newMenu_Items in range(3)]

[wxID_FRAME1MENUPLATFORMADDNODE, wxID_FRAME1MENUPLATFORMGENERATENODE] = [wx.NewId() for _init_coll_menuPlatform_Items in range(2)]

class Frame1(wx.Frame):
    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menuFile, title='File')
        parent.Append(menu=self.menuWaveform, title=u'Waveform')
        parent.Append(menu=self.menuPlatform, title=u'Platform')
        parent.Append(menu=self.menuHelp, title='Help')

    def _init_coll_newMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1NEWMENUNEWPROJECT,
              kind=wx.ITEM_NORMAL, text=u'Project')
        parent.Append(help='', id=wxID_FRAME1NEWMENUNEWWAVEFORM,
              kind=wx.ITEM_NORMAL, text=u'Waveform')
        parent.Append(help='', id=wxID_FRAME1NEWMENUNEWPLATFORM,
              kind=wx.ITEM_NORMAL, text=u'Platform')
        self.Bind(wx.EVT_MENU, self.OnNewMenuNewprojectMenu,
              id=wxID_FRAME1NEWMENUNEWPROJECT)
        self.Bind(wx.EVT_MENU, self.OnNewMenuNewwaveformMenu,
              id=wxID_FRAME1NEWMENUNEWWAVEFORM)
        self.Bind(wx.EVT_MENU, self.OnNewMenuNewplatformMenu,
              id=wxID_FRAME1NEWMENUNEWPLATFORM)

    def _init_coll_menuFile_Items(self, parent):
        # generated method, don't edit

        parent.AppendMenu(help='', id=wxID_FRAME1MENUFILENEW,
              submenu=self.newMenu, text=u'New')
        parent.Append(help='Open an existing design',
              id=wxID_FRAME1MENUFILEOPEN, kind=wx.ITEM_NORMAL, text=u'Open')
        parent.Append(help='Save current project', id=wxID_FRAME1MENUFILESAVE,
              kind=wx.ITEM_NORMAL, text=u'Save Project')
        parent.Append(help=u'Save current project to a new file',
              id=wxID_FRAME1MENUFILESAVE_AS, kind=wx.ITEM_NORMAL,
              text=u'Save Project As...')
        parent.AppendSeparator()
#        parent.Append(help='', id=wxID_FRAME1MENUFILESAVEWAVEFORM,
#              kind=wx.ITEM_NORMAL, text=u'Save Waveform')
#        parent.Append(help='', id=wxID_FRAME1MENUFILESAVEWAVEFORMAS,
#              kind=wx.ITEM_NORMAL, text=u'Save Waveform As...')
#        parent.AppendSeparator()
#        parent.Append(help='', id=wxID_FRAME1MENUFILESAVEPLATFORM,
#              kind=wx.ITEM_NORMAL, text=u'Save Platform')
#        parent.Append(help='', id=wxID_FRAME1MENUFILESAVEPLATFORMAS,
#              kind=wx.ITEM_NORMAL, text=u'Save Platform As...')
#        parent.AppendSeparator()
        parent.Append(help='Close the waveform developer',
              id=wxID_FRAME1MENUFILEEXIT, kind=wx.ITEM_NORMAL, text='Exit')
        self.Bind(wx.EVT_MENU, self.OnMenuFileOpenMenu,
              id=wxID_FRAME1MENUFILEOPEN)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSaveMenu,
              id=wxID_FRAME1MENUFILESAVE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSave_asMenu,
              id=wxID_FRAME1MENUFILESAVE_AS)
        self.Bind(wx.EVT_MENU, self.OnMenuFileExitMenu,
              id=wxID_FRAME1MENUFILEEXIT)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSavewaveformMenu,
              id=wxID_FRAME1MENUFILESAVEWAVEFORM)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSavewaveformasMenu,
              id=wxID_FRAME1MENUFILESAVEWAVEFORMAS)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSaveplatformMenu,
              id=wxID_FRAME1MENUFILESAVEPLATFORM)
        self.Bind(wx.EVT_MENU, self.OnMenuFileSaveplatformasMenu,
              id=wxID_FRAME1MENUFILESAVEPLATFORMAS)

    def _init_coll_menuPlatform_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENUPLATFORMADDNODE,
              kind=wx.ITEM_NORMAL, text=u'Add Deployment Node')
        self.Bind(wx.EVT_MENU, self.OnMenuPlatformAddnodeMenu,
              id=wxID_FRAME1MENUPLATFORMADDNODE)

    def _init_coll_compBoxPopup_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1COMPBOXPOPUPEDIT,
              kind=wx.ITEM_NORMAL, text=u'Edit')
        parent.Append(help='', id=wxID_FRAME1COMPBOXPOPUPCONNECT,
              kind=wx.ITEM_NORMAL, text=u'Connect')
        parent.Append(help='', id=wxID_FRAME1COMPBOXPOPUPREMOVE,
              kind=wx.ITEM_NORMAL, text=u'Remove')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1COMPBOXPOPUPREFRESH,
              kind=wx.ITEM_NORMAL, text=u'Refresh')
        parent.Append(help=u'', id=wxID_FRAME1COMPBOXPOPUPRENAME,
              kind=wx.ITEM_NORMAL, text=u'Rename')
        parent.Append(help=u'', id=wxID_FRAME1COMPBOXPOPUPEXPAND,
              kind=wx.ITEM_NORMAL, text=u'Expand All')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1COMPBOXPOPUPSET_AC,
              kind=wx.ITEM_NORMAL, text=u'Set Assembly Controller')
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupSet_acMenu,
              id=wxID_FRAME1COMPBOXPOPUPSET_AC)
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupEditMenu,
              id=wxID_FRAME1COMPBOXPOPUPEDIT)
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupConnectMenu,
              id=wxID_FRAME1COMPBOXPOPUPCONNECT)
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupRemoveMenu,
              id=wxID_FRAME1COMPBOXPOPUPREMOVE)
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupExpandMenu,
              id=wxID_FRAME1COMPBOXPOPUPEXPAND)
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupRenameMenu,
              id=wxID_FRAME1COMPBOXPOPUPRENAME)
        self.Bind(wx.EVT_MENU, self.OnCompBoxPopupRefreshMenu,
              id=wxID_FRAME1COMPBOXPOPUPREFRESH)

    def _init_coll_menuWaveform_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENUWAVEFORMADDCOMP,
              kind=wx.ITEM_NORMAL, text=u'New or Saved Component')
        parent.Append(help='', id=wxID_FRAME1MENUWAVEFORMREMOVECOMP,
              kind=wx.ITEM_NORMAL, text=u'Remove Component')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1MENUWAVEFORMEDITCOMP,
              kind=wx.ITEM_NORMAL, text=u'Edit Component')
        parent.Append(help='', id=wxID_FRAME1MENUWAVEFORMCONNECTCOMP,
              kind=wx.ITEM_NORMAL, text=u'Connect Component')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1MENUWAVEFORMACESUPPORT,
              kind=wx.ITEM_CHECK, text=u'ACE Support')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1MENUWAVEFORMGENWAV,
              kind=wx.ITEM_NORMAL, text=u'Generate')
        self.Bind(wx.EVT_MENU, self.OnMenuWaveformAddcompMenu,
              id=wxID_FRAME1MENUWAVEFORMADDCOMP)
        self.Bind(wx.EVT_MENU, self.OnMenuWaveformRemovecompMenu,
              id=wxID_FRAME1MENUWAVEFORMREMOVECOMP)
        self.Bind(wx.EVT_MENU, self.OnMenuWaveformConnectcompMenu,
              id=wxID_FRAME1MENUWAVEFORMCONNECTCOMP)
        self.Bind(wx.EVT_MENU, self.OnMenuWaveformEditcompMenu,
              id=wxID_FRAME1MENUWAVEFORMEDITCOMP)
        self.Bind(wx.EVT_MENU, self.OnMenuWaveformGenwavMenu,
              id=wxID_FRAME1MENUWAVEFORMGENWAV)
        self.Bind(wx.EVT_MENU, self.OnMenuWaveformAcesupportMenu,
              id=wxID_FRAME1MENUWAVEFORMACESUPPORT)

    def _init_coll_nodeBoxPopup_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPADDNODE,
              kind=wx.ITEM_NORMAL, text=u'Add Node')
        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPREMOVE,
              kind=wx.ITEM_NORMAL, text=u'Remove')
        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPGENERATE,
              kind=wx.ITEM_NORMAL, text=u'Generate')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPCONNECT,
              kind=wx.ITEM_NORMAL, text=u'Connect')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPREFRESH,
              kind=wx.ITEM_NORMAL, text=u'Refresh')
        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPRENAME,
              kind=wx.ITEM_NORMAL, text=u'Rename')
        parent.Append(help='', id=wxID_FRAME1NODEBOXPOPUPEXPAND,
              kind=wx.ITEM_NORMAL, text=u'Expand All')
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupAddnodeMenu,
              id=wxID_FRAME1NODEBOXPOPUPADDNODE)
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupRemoveMenu,
              id=wxID_FRAME1NODEBOXPOPUPREMOVE)
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupGenerateMenu,
              id=wxID_FRAME1NODEBOXPOPUPGENERATE)
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupConnectMenu,
              id=wxID_FRAME1NODEBOXPOPUPCONNECT)
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupExpandMenu,
              id=wxID_FRAME1NODEBOXPOPUPEXPAND)
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupRefreshMenu,
              id=wxID_FRAME1NODEBOXPOPUPREFRESH)
        self.Bind(wx.EVT_MENU, self.OnNodeBoxPopupRenameMenu,
              id=wxID_FRAME1NODEBOXPOPUPRENAME)

    def _init_coll_resourceBoxPopup_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1RESOURCEBOXPOPUPADD,
              kind=wx.ITEM_NORMAL, text=u'Add to Waveform')
        parent.Append(help='', id=wxID_FRAME1RESOURCEBOXPOPUPADDDEV,
              kind=wx.ITEM_NORMAL, text=u'Add to Node')
        parent.Append(help='', id=wxID_FRAME1RESOURCEBOXPOPUPADDNODE,
              kind=wx.ITEM_NORMAL, text=u'Add to Platform')
        #parent.Append(help='', id=wxID_FRAME1RESOURCEBOXPOPUPGETDESCR,
        #      kind=wx.ITEM_NORMAL, text=u'Display Description Below')
        parent.Append(help='', id=wxID_FRAME1RESOURCEBOXPOPUPGETDOXYGENREFMAN,
              kind=wx.ITEM_NORMAL, text=u'View Manual from Doxygen')
        self.Bind(wx.EVT_MENU, self.OnResourceBoxPopupAddMenu,
              id=wxID_FRAME1RESOURCEBOXPOPUPADD)
        #self.Bind(wx.EVT_MENU, self.OnResourceBoxPopupGetDescr,
        #      id=wxID_FRAME1RESOURCEBOXPOPUPGETDESCR)
        self.Bind(wx.EVT_MENU, self.OnResourceBoxPopupGetDoxygenRefMan,
              id=wxID_FRAME1RESOURCEBOXPOPUPGETDOXYGENREFMAN)
        self.Bind(wx.EVT_MENU, self.OnResourceBoxPopupAdddevMenu,
              id=wxID_FRAME1RESOURCEBOXPOPUPADDDEV)
        self.Bind(wx.EVT_MENU, self.OnResourceBoxPopupAddnodeMenu,
              id=wxID_FRAME1RESOURCEBOXPOPUPADDNODE)

    def _init_coll_menuHelp_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENUHELPSAMPLEWAVEFORM,
              kind=wx.ITEM_NORMAL, text=u'Sample Waveform')
        parent.AppendSeparator()
        parent.Append(help='Display general information about OSSIE Waveform Developer',
              id=wxID_FRAME1MENUHELPABOUT, kind=wx.ITEM_NORMAL, text='About')
        self.Bind(wx.EVT_MENU, self.OnMenuHelpAboutMenu,
              id=wxID_FRAME1MENUHELPABOUT)
        self.Bind(wx.EVT_MENU, self.OnMenuHelpSamplewaveformMenu,
              id=wxID_FRAME1MENUHELPSAMPLEWAVEFORM)

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(number=0, text='status')

        parent.SetStatusWidths([-1])

    def _init_utils(self):
        # generated method, don't edit
        self.menuFile = wx.Menu(title='')

        self.menuHelp = wx.Menu(title='')

        self.menuBar1 = wx.MenuBar()

        self.compBoxPopup = wx.Menu(title='')

        self.menuWaveform = wx.Menu(title='')

        self.resourceBoxPopup = wx.Menu(title=u'')

        self.menuPlatform = wx.Menu(title='')

        self.nodeBoxPopup = wx.Menu(title='')

        self.newMenu = wx.Menu(title=u'')

        self._init_coll_menuFile_Items(self.menuFile)
        self._init_coll_menuHelp_Items(self.menuHelp)
        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_compBoxPopup_Items(self.compBoxPopup)
        self._init_coll_menuWaveform_Items(self.menuWaveform)
        self._init_coll_resourceBoxPopup_Items(self.resourceBoxPopup)
        self._init_coll_menuPlatform_Items(self.menuPlatform)
        self._init_coll_nodeBoxPopup_Items(self.nodeBoxPopup)
        self._init_coll_newMenu_Items(self.newMenu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(574, 283), size=wx.Size(594, 560),
              style=wx.DEFAULT_FRAME_STYLE, title='OSSIE Waveform Developer')
        self._init_utils()
        self.SetClientSize(wx.Size(594, 560))
        self.SetMenuBar(self.menuBar1)
        self.SetAutoLayout(True)
        self.Center(wx.BOTH)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=wx.VSCROLL)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.waveNameBox = wx.TextCtrl(id=wxID_FRAME1WAVENAMEBOX,
              name='waveNameBox', parent=self, pos=wx.Point(7, 9),
              size=wx.Size(175, 25), style=0, value='')

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='Waveform Name', name='staticText2', parent=self,
              pos=wx.Point(190, 13), size=wx.Size(99, 17), style=0)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAME1SPLITTERWINDOW1,
              name='splitterWindow1', parent=self, point=wx.Point(7, 75),
              size=wx.Size(580, 365), style=wx.SP_3D)
        self.splitterWindow1.SetConstraints(LayoutAnchors(self.splitterWindow1,
              True, True, True, True))
  #      self.splitterWindow1.SetBestFittingSize(wx.Size(580, 366))

        self.sashWindow1 = wx.SashWindow(id=wxID_FRAME1SASHWINDOW1,
              name='sashWindow1', parent=self.splitterWindow1, pos=wx.Point(0,
              0), size=wx.Size(175, 365),
              style=wx.SIMPLE_BORDER | wx.CLIP_CHILDREN | wx.SW_3D)

        self.sashWindow2 = wx.SashWindow(id=wxID_FRAME1SASHWINDOW2,
              name='sashWindow2', parent=self.splitterWindow1, pos=wx.Point(180,
              0), size=wx.Size(400, 365), style=wx.CLIP_CHILDREN | wx.SW_3D)
        self.splitterWindow1.SplitVertically(self.sashWindow1, self.sashWindow2,
              175)

        self.resourceBox = wx.TreeCtrl(id=wxID_FRAME1RESOURCEBOX,
              name=u'resourceBox', parent=self.sashWindow1, pos=wx.Point(0, 0),
              size=wx.Size(175, 365),
              style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.resourceBox.SetMinSize(wx.Size(-1, -1))
        self.resourceBox.SetBestFittingSize(wx.Size(175, 365))
        self.resourceBox.Bind(wx.EVT_RIGHT_UP, self.OnResourceBoxRightUp)
        self.resourceBox.Bind(wx.EVT_LEFT_UP, self.OnResourceBoxLeftUp)
        self.resourceBox.Bind(wx.EVT_LEFT_DCLICK, self.OnResourceBoxLeftDoubleClick)
        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Available Resources', name='staticText1', parent=self,
              pos=wx.Point(7, 46), size=wx.Size(120, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Waveform Layout', name='staticText3', parent=self,
              pos=wx.Point(327, 46), size=wx.Size(103, 17), style=0)

        self.splitterWindow2 = wx.SplitterWindow(id=wxID_FRAME1SPLITTERWINDOW2,
              name='splitterWindow2', parent=self.sashWindow2, point=wx.Point(0,
              -32), size=wx.Size(200, 100), style=wx.SP_3D)
        self.splitterWindow2.SetSashSize(5)

        self.sashWindow3 = wx.SashWindow(id=wxID_FRAME1SASHWINDOW3,
              name='sashWindow3', parent=self.splitterWindow2, pos=wx.Point(0,
              0), size=wx.Size(400, 200),
              style=wx.SIMPLE_BORDER | wx.CLIP_CHILDREN | wx.SW_3D)

        self.sashWindow4 = wx.SashWindow(id=wxID_FRAME1SASHWINDOW4,
              name='sashWindow4', parent=self.splitterWindow2, pos=wx.Point(0,
              205), size=wx.Size(400, 191),
              style=wx.SIMPLE_BORDER | wx.CLIP_CHILDREN | wx.SW_3D)
        self.sashWindow4.SetSashVisible(wx.SASH_TOP, False)
        self.sashWindow4.SetMinSize(wx.Size(-1, -1))
        self.splitterWindow2.SplitHorizontally(self.sashWindow3,
              self.sashWindow4, 200)

        self.compBox = wx.TreeCtrl(id=wxID_FRAME1COMPBOX, name=u'compBox',
              parent=self.sashWindow3, pos=wx.Point(0, 0), size=wx.Size(399,
              200),
              style=wx.TR_EDIT_LABELS | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.compBox.SetBestFittingSize(wx.Size(399, 200))
        self.compBox.Bind(wx.EVT_RIGHT_UP, self.OnCompBoxRightUp)
        self.compBox.Bind(wx.EVT_TREE_END_LABEL_EDIT,
              self.OnCompBoxTreeEndLabelEdit, id=wxID_FRAME1COMPBOX)
        self.compBox.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT,
              self.OnCompBoxTreeBeginLabelEdit, id=wxID_FRAME1COMPBOX)
        self.compBox.Bind(wx.EVT_LEFT_DCLICK, self.OnCompBoxLeftDclick)

        self.nodeBox = wx.TreeCtrl(id=wxID_FRAME1NODEBOX, name=u'nodeBox',
              parent=self.sashWindow4, pos=wx.Point(0, 0), size=wx.Size(400,
              191),
              style=wx.TR_EDIT_LABELS | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.nodeBox.Bind(wx.EVT_RIGHT_UP, self.OnNodeBoxRightUp)
        self.nodeBox.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT,
              self.OnNodeBoxTreeBeginLabelEdit, id=wxID_FRAME1NODEBOX)
        self.nodeBox.Bind(wx.EVT_TREE_END_LABEL_EDIT,
              self.OnNodeBoxTreeEndLabelEdit, id=wxID_FRAME1NODEBOX)

        self.RefreshResourceBtn = wx.Button(id=wxID_REFRESHRESOURCEBTN, label='Refresh',
              name='RefreshResourceBtn', parent=self, pos=wx.Point(170, 40),
              size=wx.Size(70, 27), style=0)
        self.RefreshResourceBtn.Bind(wx.EVT_BUTTON, self.OnRefreshResourceBtnButton,
              id=wxID_REFRESHRESOURCEBTN)

        self.resDescrBox = wx.TextCtrl(id=wxID_FRAME1COMPDESCRBOX,
              name='resDescrBox', parent=self, pos=wx.Point(90, 445),
              size=wx.Size(497, 55), style= wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.resDescrBox.SetConstraints(LayoutAnchors(self.resDescrBox,
              True, False, True, True))
        self.resDescrBox.SetMinSize(wx.Size(-1,-1))
        self.resDescrBox.SetBackgroundColour("lightgray")

        self.staticText4 = wx.StaticText (id=wxID_FRAME1STATICTEXT4,
              label='Resource Description', name='staticText4', parent=self,
              pos=wx.Point(7, 445), size=wx.Size (80, 40), style= wx.TE_BESTWRAP | wx.TE_MULTILINE)
        self.staticText4.SetConstraints(LayoutAnchors(self.staticText4,
              True, False, False, True))



    def __init__(self, parent):
        self.name = "owd"   # in case anybody asks

        # Constructor for MainFrame
        self._init_ctrls(parent)

        #read in the configuration information
        LoadConfiguration(self)

        #setup the environment
        self.active_comp = None
        self.CompFrame = ComponentFrame.create(self)
        self.active_wave = WaveformClass.Waveform()
        self.active_plat = PlatformClass.Platform()
        self.displayComps()
        self.loadResources()
        self.saveWaveformPath = None
        self.savePlatformPath = None
        self.saveProjectPath = None
        self.description = None
#        self.wavedevPath = os.getcwd() + "/"
# NOTE The wavedevPath string should be constructed, not hard-coded
#        self.wavedevPath = "/usr/lib/python2.5/site-packages/WaveDev/wavedev/"
        self.wavedevPath = __file__
        if os.path.islink (self.wavedevPath):
            self.wavedevPath = os.path.realpath (self.wavedevPath)
        self.wavedevPath = os.path.dirname (os.path.abspath (self.wavedevPath)) + '/'

################################################################################
## File/Help Menu Functionality
################################################################################
    def OnMenuFileNewMenu(self, event):
        self.active_comp = None
        self.active_wave = WaveformClass.Waveform()
        self.displayComps()
        event.Skip()

    def OnNewMenuNewprojectMenu(self, event):
        if len(self.active_wave.components)>0 or len(self.active_plat.nodes)>0 or self.saveProjectPath != None:
            tmpstr = 'Do you want to save the current project first?\n'
            dlg = wx.MessageDialog(self, tmpstr,
                  'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_YES:
                    sflag = True
                if returnCode == wx.ID_NO:
                    sflag = False
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    event.Skip()
                    return
            finally:
                dlg.Destroy()

            if sflag == True:
                tempLn = self.waveNameBox.GetLineText(0)
                if tempLn != self.active_wave.name and self.saveProjectPath != None:
                    tmpstr = 'The waveform name has changed.\n'
                    tmpstr += 'Do you want to overwrite the existing project file?\n'
                    tmpstr += self.saveProjectPath
                    dlg = wx.MessageDialog(self, tmpstr,
                          'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
                    try:
                        returnCode = dlg.ShowModal()
                        if returnCode == wx.ID_YES:
                            self.active_wave.name = tempLn
                            if self.ProjectSave(False) == False:
                                return
                        if returnCode == wx.ID_NO:
                            if self.ProjectSave(True) == False:
                                return
                        elif returnCode == wx.ID_CANCEL:
                            dlg.Destroy()
                            event.Skip()
                            return
                    finally:
                        dlg.Destroy()

                else:
                    if self.saveProjectPath != None:
                        if self.ProjectSave(False) == False:
                            return
                    else:
                        if self.ProjectSave(True) == False:
                            return

        self.active_wave = WaveformClass.Waveform()
        self.active_plat = PlatformClass.Platform()
        self.saveProjectPath = None
        self.waveNameBox.Clear()
        self.displayComps()
        self.displayNodes()


        event.Skip()

    def OnNewMenuNewwaveformMenu(self, event):
        if len(self.active_wave.components)>0 or self.saveWaveformPath != None:
            tmpstr = 'Do you want to save the current waveform first?\n'
            dlg = wx.MessageDialog(self, tmpstr,
                  'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_YES:
                    sflag = True
                if returnCode == wx.ID_NO:
                    sflag = False
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    event.Skip()
                    return
            finally:
                dlg.Destroy()

            if sflag == True:
                tempLn = self.waveNameBox.GetLineText(0)
                if tempLn != self.active_wave.name and self.saveWaveformPath != None:
                    tmpstr = 'The waveform name has changed.\n'
                    tmpstr += 'Do you want to overwrite the existing waveform file?\n'
                    tmpstr += self.saveWaveformPath
                    dlg = wx.MessageDialog(self, tmpstr,
                          'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
                    try:
                        returnCode = dlg.ShowModal()
                        if returnCode == wx.ID_YES:
                            self.active_wave.name = tempLn
                            if self.WaveformSave(False) == False:
                                return
                        if returnCode == wx.ID_NO:
                            if self.WaveformSave(True) == False:
                                return
                        elif returnCode == wx.ID_CANCEL:
                            dlg.Destroy()
                            event.Skip()
                            return
                    finally:
                        dlg.Destroy()

                else:
                    if self.saveWaveformPath != None:
                        if self.WaveformSave(False) == False:
                            return
                    else:
                        if self.WaveformSave(True) == False:
                            return

        self.active_wave = WaveformClass.Waveform()
        self.saveWaveformPath = None
        self.waveNameBox.Clear()
        self.displayComps()

        event.Skip()

    def OnNewMenuNewplatformMenu(self, event):
        if len(self.active_plat.nodes)>0 or self.savePlatformPath != None:
            tmpstr = 'Do you want to save the current platform first?\n'
            dlg = wx.MessageDialog(self, tmpstr,
                  'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_YES:
                    sflag = True
                if returnCode == wx.ID_NO:
                    sflag = False
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    event.Skip()
                    return
            finally:
                dlg.Destroy()

            if sflag == True:
                if self.savePlatformPath != None:
                    tmpstr = 'Do you want to overwrite the existing platform file?\n'
                    tmpstr += self.savePlatformPath
                    dlg = wx.MessageDialog(self, tmpstr,
                          'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
                    try:
                        returnCode = dlg.ShowModal()
                        if returnCode == wx.ID_YES:
                            if self.PlatformSave(False) == False:
                                return
                        if returnCode == wx.ID_NO:
                            if self.PlatformSave(True) == False:
                                return
                        elif returnCode == wx.ID_CANCEL:
                            dlg.Destroy()
                            event.Skip()
                            return
                    finally:
                        dlg.Destroy()

                else:
                    if self.PlatformSave(True) == False:
                        return

        self.active_plat = PlatformClass.Platform()
        self.savePlatformPath = None
        self.displayNodes()

        event.Skip()

    def OnMenuFileOpenMenu(self, event):
        if len(self.homeDir) > 0:
            tmpdir = self.homeDir
        else:
            tmpdir = os.path.expanduser("~")
            if tmpdir == "~":
                tmpdir = "/home"

        tmpwildcard = "Project Files (*.owd)|*.owd|Waveform Designs (*.sca)|*.sca|Platform Layouts (*.plt)|*.plt"
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
        if tmpObject[0] == 'waveform':
            self.WaveformOpen(tmpPath,tmpObject[1])
        elif tmpObject[0] == 'platform':
            self.PlatformOpen(tmpPath,tmpObject[1])
        elif tmpObject[0] == 'project':
            self.ProjectOpen(tmpPath,tmpObject[1],tmpObject[2])

        event.Skip()

    def OnMenuFileSaveMenu(self, event):
        if self.saveProjectPath != None:
            tempLn = self.waveNameBox.GetLineText(0)
            if tempLn != self.active_wave.name:
                tmpstr = 'The waveform name has changed.\n'
                tmpstr += 'Do you want to overwrite the existing project file?\n'
                tmpstr += self.saveProjectPath
                dlg = wx.MessageDialog(self, tmpstr,
                      'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
                try:
                    returnCode = dlg.ShowModal()
                    if returnCode == wx.ID_YES:
                        self.active_wave.name = tempLn
                        self.ProjectSave(False)
                    if returnCode == wx.ID_NO:
                        self.ProjectSave(True)
                    elif returnCode == wx.ID_CANCEL:
                        dlg.Destroy()
                        event.Skip()
                        return
                finally:
                    dlg.Destroy()

            else:
                self.ProjectSave(False)
        else:
            self.ProjectSave(False)

        event.Skip()

    def OnMenuFileSave_asMenu(self, event):
        self.ProjectSave(True)
        event.Skip()

    def OnMenuFileSavewaveformMenu(self, event):
        if self.saveWaveformPath != None:
            tempLn = self.waveNameBox.GetLineText(0)
            if tempLn != self.active_wave.name:
                tmpstr = 'The waveform name has changed.\n'
                tmpstr += 'Do you want to overwrite the existing waveform file?\n'
                tmpstr += self.saveWaveformPath
                dlg = wx.MessageDialog(self, tmpstr,
                      'OSSIE Waveform Developer', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
                try:
                    returnCode = dlg.ShowModal()
                    if returnCode == wx.ID_YES:
                        self.active_wave.name = tempLn
                        self.WaveformSave(False)
                    if returnCode == wx.ID_NO:
                        self.WaveformSave(True)
                    elif returnCode == wx.ID_CANCEL:
                        dlg.Destroy()
                        event.Skip()
                        return
                finally:
                    dlg.Destroy()

            else:
                self.WaveformSave(False)
        else:
            self.WaveformSave(False)

        event.Skip()

    def OnMenuFileSavewaveformasMenu(self, event):
        self.WaveformSave(True)
        event.Skip()

    def OnMenuFileSaveplatformMenu(self, event):
        self.PlatformSave(False)
        event.Skip()

    def OnMenuFileSaveplatformasMenu(self, event):
        self.PlatformSave(True)
        event.Skip()

    def OnMenuFileExitMenu(self, event):
        self.Close()
        event.Skip()

    def ProjectSave(self,saveasFlag):
        if saveasFlag == True or self.saveProjectPath == None:
            tempLn = self.waveNameBox.GetLineText(0)
            if tempLn == '':
                errorMsg(self,'Please enter a waveform name first')
                return False
            self.active_wave.name = tempLn

            if len(self.homeDir) > 0:
                tmpdir = self.homeDir
            else:
                tmpdir = os.path.expanduser("~")

            dlg = wx.FileDialog(self, "Save As", tmpdir, tempLn + '.owd', "Project File (*.owd)|*.owd", wx.SAVE)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_OK:
                    self.saveProjectPath = dlg.GetPath()
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    return False
            finally:
                dlg.Destroy()

        f = open(self.saveProjectPath,'w')
        cPickle.dump(('project',self.active_wave,self.active_plat),f)

        return True

    def WaveformSave(self,saveasFlag):
        if saveasFlag == True or self.saveWaveformPath == None:
            tempLn = self.waveNameBox.GetLineText(0)
            if tempLn == '':
                errorMsg(self,'Please enter a waveform name first')
                return False
            self.active_wave.name = tempLn

            if len(self.homeDir) > 0:
                tmpdir = self.homeDir
            else:
                tmpdir = os.path.expanduser("~")

            dlg = wx.FileDialog(self, "Save As", tmpdir, tempLn + '.sca', "*.sca", wx.SAVE)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_OK:
                    self.saveWaveformPath = dlg.GetPath()
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    return False
            finally:
                dlg.Destroy()

        f = open(self.saveWaveformPath,'w')
        cPickle.dump(('waveform',self.active_wave),f)

        return True

    def PlatformSave(self,saveasFlag):
        if saveasFlag == True or self.savePlatformPath == None:
            if self.active_plat.name != "":
                tmpname = self.active_plat.name
            else:
                tmpname = 'Platform1'

            if len(self.homeDir) > 0:
                tmpdir = self.homeDir
            else:
                tmpdir = os.path.expanduser("~")

            dlg = wx.FileDialog(self, "Save As", tmpdir, tmpname + '.plt', "Platform File (*.plt)|*.plt", wx.SAVE)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_OK:
                    self.savePlatformPath = dlg.GetPath()
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    return False
            finally:
                dlg.Destroy()

        f = open(self.savePlatformPath,'w')
        cPickle.dump(('platform',self.active_plat),f)

        return True

    def WaveformOpen(self,newPath,newWav):
        if newPath != None:
            if self.saveWaveformPath != None:
                dlg = wx.MessageDialog(self, 'Do you want to save your changes to the active waveform first?',
                      'Error', wx.YES_NO | wx.ICON_INFORMATION)
                try:
                    returnCode = dlg.ShowModal()
                    if returnCode == wx.ID_YES:
                        self.WaveformSave(False)
                    elif returnCode == wx.ID_CANCEL:
                        dlg.Destroy()
                        return
                finally:
                    dlg.Destroy()

            self.saveWaveformPath = newPath

        self.active_wave = newWav

        # We must create new UUIDs for each instance and copy the file uuid from
        # the base component to the instance
        for c in self.active_wave.components:
            found = False
            for x in self.Available_Components:
                c.setUUID()
                if c.baseName == x.baseName:
                    c.file_uuid = x.file_uuid
                    found = True
            if c.generate == False and found == False:
                errorMsg(self,"Could not find " + c.baseName + " which " + c.name + " is an instance of.")


        #Because device assignments are stored as python objects in each component
        #we must refresh the assignment with the available platform devices

        for c in self.active_wave.components:
            if c.device == None:
                continue
            found = False
            for n in self.active_plat.nodes:
                for d in n.Devices:
                    if c.device.name == d.name and c.device.node == d.node:
                        c.device = d
                        found = True
                        break
            if found == False:
                tmpstr = 'ERROR! Cannot find the ' + c.device.name + ' device'
                tmpstr += ' in this platform layout.\nThe ' + c.name + ' component was assigned to this device.\n'
                tmpstr += 'Setting device assignment to None.'
                errorMsg(self,tmpstr)
                c.device = None

        self.waveNameBox.Clear()
        self.waveNameBox.WriteText(self.active_wave.name)
        self.displayComps()

        if self.active_wave.ace == True:
            self.menuWaveform.Check(wxID_FRAME1MENUWAVEFORMACESUPPORT,True)
            #self.ACEcheckBox.SetValue(True)
        else:
            self.menuWaveform.Check(wxID_FRAME1MENUWAVEFORMACESUPPORT,False)
            #self.ACEcheckBox.SetValue(False)

    def PlatformOpen(self,newPath,newPlat):
        if newPath != None:
            if self.savePlatformPath != None:
                dlg = wx.MessageDialog(self, 'Do you want to save your changes to the active platform layout first?',
                      'Error', wx.YES_NO | wx.ICON_INFORMATION)
                try:
                    returnCode = dlg.ShowModal()
                    if returnCode == wx.ID_YES:
                        self.PlatformSave(False)
                    elif returnCode == wx.ID_CANCEL:
                        dlg.Destroy()
                        return
                finally:
                    dlg.Destroy()

            self.savePlatformPath = newPath

        self.active_plat = newPlat


        # NOTE: The following comment does not hold true now that the nodes are installed
        # once for the whole system -> hence, the d.setUUID() is also commented out

        # We must create new UUIDs for each instance and copy the file uuid from
        # the base component to the instance
        for n in self.active_plat.nodes:
            for d in n.Devices:
                found = False
                for ad in self.Available_Devices:
                    if d.baseName == ad.baseName:
                       # print d.baseName
                        d.file_uuid = ad.file_uuid
        #                d.setUUID()
                        found = True
                if found == False:
                    errorMsg(self,"Could not find " + d.baseName + " which " + d.name + " is an instance of.")

        self.displayNodes()


    def ProjectOpen(self,newPath,newWav,newPlat):
        if self.saveProjectPath != None:
            dlg = wx.MessageDialog(self, 'Do you want to save your changes to the active project first?',
                  'Error', wx.YES_NO | wx.ICON_INFORMATION)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_YES:
                    self.ProjectSave(False)
                elif returnCode == wx.ID_CANCEL:
                    dlg.Destroy()
                    return
            finally:
                dlg.Destroy()

        self.saveProjectPath = newPath

        self.PlatformOpen(None,newPlat)
        self.WaveformOpen(None,newWav)
        self.displayNodes()


    #################################################################
    ## Help Menu Stuff
    #################################################################

    def OnMenuHelpAboutMenu(self, event):
        dlg = AboutDialog.Dialog1(self)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        event.Skip()

    def OnMenuHelpSamplewaveformMenu(self, event):
        self.generateTestWF()
        event.Skip()

    def generateTestWF(self):
        self.active_wave = WaveformClass.Waveform()
        int1 = ComponentClass.Interface('complexShort')
        op1 = ComponentClass.Operation('pushPacket','void')
        param1 = ComponentClass.Param('I','PortTypes::ShortSequence','in')
        param2 = ComponentClass.Param('Q','PortTypes::ShortSequence','in')
        op1.params.extend([param1,param2])
        int1.operations.append(op1)

        t2 = ComponentClass.Component("Transmitter",AC=True)
        p1 = ComponentClass.Port('inPortTx1',copy.deepcopy(int1),'Provides')
        p2 = ComponentClass.Port('outPortTx1',copy.deepcopy(int1),'Uses')
        t2.ports.append(p1); t2.ports.append(p2)
        self.active_wave.components.append(t2)

        t3 = ComponentClass.Component("Channel")
        p1 = ComponentClass.Port('inPortCh1',copy.deepcopy(int1),'Provides')
        p2 = ComponentClass.Port('inPortCh2',copy.deepcopy(int1),'Provides')
        p3 = ComponentClass.Port('inPortCh3',copy.deepcopy(int1),'Provides')
        p4 = ComponentClass.Port('outPortCh1',copy.deepcopy(int1),'Uses')
        p5 = ComponentClass.Port('outPortCh2',copy.deepcopy(int1),'Uses')
        p6 = ComponentClass.Port('outPortCh3',copy.deepcopy(int1),'Uses')
        t3.ports.extend([p1,p2,p3,p4,p5,p6])
        self.active_wave.components.append(t3)

        t4 = ComponentClass.Component("Receiver")
        p1 = ComponentClass.Port('inPortRx1',copy.deepcopy(int1),'Provides')
        p2 = ComponentClass.Port('outPortRx1',copy.deepcopy(int1),'Uses')
        t4.ports.append(p1); t4.ports.append(p2)
        self.active_wave.components.append(t4)

        temp_dev = ComponentClass.Component("GPP")
        self.active_wave.devices.append(temp_dev)

        self.displayComps()


################################################################################
## Waveform Layout Functionality
################################################################################

    def displayComps(self):
        self.compBox.DeleteAllItems()
        troot = self.compBox.AddRoot("the_root")
        for c in self.active_wave:
            t1 = self.compBox.AppendItem(troot,c.name)
            self.compBox.SetPyData(t1,c)
            if c.AssemblyController == True:
                self.compBox.SetItemBold(t1,True)
            else:
                self.compBox.SetItemBold(t1,False)
            for p in c.connections:
                tnm = p.localPort.name + "::" + p.remoteComp.name + "(" + p.remotePort.name + ")"
                t2 = self.compBox.AppendItem(t1,tnm)
                self.compBox.SetPyData(t2,p)

    def EditComponent(self):
        self.CompFrame.calledByParent = True
        self.CompFrame.MakeModal(True)
        self.CompFrame.Show(True)

    def ConnectComponent(self):
        ## Assume active_comp is set to the appropriate component
        dlg = ConnectDialog.create(self)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
            self.displayComps()

    def RemoveCompBoxSelection(self):
        dlg = wx.MessageDialog(self, '"Are you sure you want to remove this item?"',
          'Error', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        try:
            if dlg.ShowModal() == wx.ID_NO:
                return
        finally:
            dlg.Destroy()

        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            return
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
            ti = self.active_wave.components.index(self.active_comp)
            # If any other component is connected to this component - connection must be removed
            for c in self.active_wave.components:
                for con in c.connections:
                    if con.remoteComp == self.active_comp:
                        ci = c.connections.index(con)
                        del c.connections[ci]
            del self.active_wave.components[ti]
        else:
            # a child component (connection)
            tc = self.compBox.GetPyData(sn)
            self.active_comp = self.compBox.GetPyData(self.compBox.GetItemParent(sn))
            ti = self.active_comp.connections.index(tc)
            del self.active_comp.connections[ti]

        self.displayComps()
        self.displayNodes()


    #################################################################
    ## Waveform Event Stuff
    #################################################################

    def OnCompBoxRightUp(self, event):
        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            for x in self.compBoxPopup.GetMenuItems():
                if x.GetLabel() == 'Expand All' or x.GetLabel() == 'Refresh':
                    x.Enable(True)
                else:
                    x.Enable(False)
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
            for x in self.compBoxPopup.GetMenuItems():
                x.Enable(True)
        else:
            # a child component (connections in our case)
            for x in self.compBoxPopup.GetMenuItems():
                if x.GetLabel() != 'Remove':
                    x.Enable(False)

        self.compBox.PopupMenu(self.compBoxPopup)
        event.Skip()

    def OnCompBoxPopupSet_acMenu(self, event):
        for c in self.active_wave.components:
            c.AssemblyController = False
        self.active_comp.AssemblyController = True
        self.displayComps()
        event.Skip()

    def OnCompBoxPopupEditMenu(self, event):
        self.EditComponent()
        event.Skip()

    def OnCompBoxPopupConnectMenu(self, event):
        self.ConnectComponent()
        event.Skip()

    def OnNodeBoxPopupConnectMenu(self, event):
        errorMsg(self, "Connection between two devices is not yet supported.  Please connect via the component.")

        # what to do when the connections are supported :
        #sn = self.nodeBox.GetSelection()
        #self.active_comp = self.nodeBox.GetPyData(sn)  #active component is actually and active resource
        #self.ConnectComponent()

    def OnCompBoxPopupRemoveMenu(self, event):
        self.RemoveCompBoxSelection()
        event.Skip()

    def OnCompBoxPopupExpandMenu(self, event):
        troot = self.compBox.GetRootItem()
        if self.compBox.GetChildrenCount(troot) > 0:
            cid1,cookie1 = self.compBox.GetFirstChild(troot)
            self.compBox.Expand(cid1)
            for x in range(self.compBox.GetChildrenCount(troot,recursively=False)-1):
                    cid2,cookie2 = self.compBox.GetNextChild(troot,cookie1)
                    self.compBox.Expand(cid2)
                    cid1 = cid2
                    cookie1 = cookie2
        event.Skip()

    def OnCompBoxTreeEndLabelEdit(self, event):
        if event.IsEditCancelled():
            event.Veto()
            return
        sn = event.GetItem()
        if sn == self.compBox.GetRootItem():
            errorMsg(self,'You can not rename this element - root!')
            even.Veto()
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
            newname = event.GetLabel()

        if len(newname) > 0:
            for c in self.active_wave.components:
                if c != self.active_comp and c.name == newname:
                    errorMsg(self,'Invalid name - a component by that name already exists')
                    event.Veto()
                    return

            #Component names with spaces do not work
            if newname.find(' ') != -1:
                errorMsg(self,'Resource names can not have spaces in them.')
                event.Veto()
                return
                #newname = newname.replace(' ','_')
                #self.compBox.SetItemText(sn,newname)

            self.active_comp.changeName(newname)
            #self.active_comp.name = newname
            #if self.active_comp.generate == True:
            #    self.active_comp.baseName = newname
        else:
            errorMsg(self,'Invalid name - must have at least one character!')
            event.Veto()
            return
        event.Skip()

    def OnCompBoxTreeBeginLabelEdit(self, event):
        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            errorMsg(self,'You can not rename this element!')
            event.Veto()
            return
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
        else:
            # a child component (connection)
            event.Veto()
            return
        event.Skip()

    def OnCompBoxPopupRenameMenu(self, event):
        sn = self.compBox.GetSelection()
        self.compBox.EditLabel(sn)
        event.Skip()

    def OnCompBoxLeftDclick(self, event):
        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            return
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
            self.EditComponent()
        else:
            # a child component (connections in our case)
            return

        event.Skip()

    def OnCompBoxPopupRefreshMenu(self, event):
        self.displayComps()
        event.Skip()

    #################################################################
    ## Waveform Menu Stuff
    #################################################################

    def OnMenuWaveformAddcompMenu(self, event):
        ComponentFrame.newComponentFrame()

    def OnMenuWaveformRemovecompMenu(self, event):
        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            return
        self.RemoveCompBoxSelection()
        event.Skip()

    def OnMenuWaveformConnectcompMenu(self, event):
        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            errorMsg(self,'Please select a component first!')
            return
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
        else:
            # a child component (connections in our case)
            errorMsg(self,'Only top level components can be connected!')
            return

        self.ConnectComponent()
        event.Skip()

    def OnMenuWaveformEditcompMenu(self, event):
        sn = self.compBox.GetSelection()
        if sn == self.compBox.GetRootItem():
            return
        elif self.compBox.GetItemParent(sn) == self.compBox.GetRootItem():
            # a main level component
            self.active_comp = self.compBox.GetPyData(sn)
            ti = self.active_wave.components.index(self.active_comp)
        else:
            # a child component (connection)
            errorMsg(self,'Only top level components can be edited!')
            return

        self.EditComponent()
        event.Skip()

    def OnMenuWaveformGenwavMenu(self, event):
        tempLn = self.waveNameBox.GetLineText(0)
        if tempLn == '':
            errorMsg(self,'Please enter a waveform name first')
            return

        nFlag = False
        for c in self.active_wave.components:
            if c.name == tempLn:
                nFlag = True

        if nFlag == True:
            tmpstr = "One of the waveform components has the same name as the waveform.\n"
            tmpstr += "This is not allowed."
            errorMsg(self,tmpstr)
            return

        #check for duplicate node names
        #get all the device instance ids and node names
        device_ids = []
        node_names = []
        for n in self.active_plat.nodes:
            node_names.append(n.name)
            for d in n.Devices:
                device_ids.append(d.uuid)

        ##check for duplicate node names
        #tmp = list(set(node_names))   #removes duplicates from the list
        #if len(tmp) != len(node_names):
        #    errorMsg(self,"Duplicate node names detected.  This is not allowed.")
        #    return

        #check for duplicates in the device uuids
        tmp = list(set(device_ids))  #removes duplicates from the list
        if len(tmp) != len(device_ids):  #if there were duplicates (multiple copies of same device instances)
            errorMsg(self,"Duplicate nodes or device instantiation UUIDs have been detected.  This is not allowed.")
            return

        acFlag = False
        noDevs = []
        for c in self.active_wave.components:
            if c.AssemblyController == True:
                acFlag = True
            if c.device == None:
                noDevs.append(c.name)
        if not acFlag:
            #errorMsg(self,'Please set one component to be the Assebly Controller.')
            dlg = wx.MessageDialog(self, 'Are you sure you want to generate this waveform without an Assembly Controller?',
              'Caption', wx.YES_NO | wx.ICON_INFORMATION)
            try:
                returnCode = dlg.ShowModal()
                if returnCode == wx.ID_YES:
                    pass
                else:
                    dlg.Destroy()
                    return
            finally:
                dlg.Destroy()
            #return

        if len(noDevs) > 0:
            tmpstr = 'The following components are not assigned to a device. '
            tmpstr += 'This will cause the DAS file to generated incorrectly.\n\n'
            for x in noDevs:
                tmpstr += x + '\n'
            errorMsg(self,tmpstr)

        self.waveName = tempLn
        self.active_wave.name = tempLn

        dlg = wx.DirDialog(self,"Please select the place to generate the code",style=wx.DD_NEW_DIR_BUTTON)
        dlg.SetPath(os.path.expanduser('~'))
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.path = dlg.GetPath()
            else:
                return
        finally:
            dlg.Destroy()

        gen = genStruct.genAll(self.path, self.wavedevPath, copy.deepcopy(self.active_wave))
        gen.genDirs()
        # Only include the device manager files if there is just one node
        if len(self.active_plat.nodes) == 1:
            gen.writeMakefiles(True)
        else:
            gen.writeMakefiles(False)
        # TODO: use different configure.ac file for application -JDG
        gen.genConfigureACFiles(self.installPath)
        for c in self.active_wave.components:
            if c.generate:
                gen.genCompFiles(c)

        xml_gen.genxml(copy.deepcopy(self.active_wave.components), self.path, self.wavedevPath, self.active_wave.name)
        xml_gen.genDAS(copy.deepcopy(self.active_wave.components), self.path, self.wavedevPath, self.active_wave.name)
        xml_gen.writeWaveSetuppy(self.path, self.wavedevPath, self.active_wave.name)

        #save the .owd file
        f = open(self.path + "/" + self.waveName +  "/" + self.waveName + ".owd",'w')
        cPickle.dump(('project',self.active_wave,self.active_plat),f)

        #generate the dcd file for each node
        #for n in self.active_plat.nodes:
            #if len(self.active_plat.nodes) == 1:
            #    tmpname = 'DeviceManager'
            #    folderFlag = False
            #else:
            #    tmpname = 'DeviceManager' + n.name
            #    folderFlag = True
            #xml_gen.genDeviceManager(n, self.path, self.wavedevPath, self.active_wave.name, tmpname,folderFlag)

        gen.cleanUp()

    def OnMenuWaveformAcesupportMenu(self, event):
        if self.menuWaveform.IsChecked(wxID_FRAME1MENUWAVEFORMACESUPPORT):
            self.active_wave.ace = True
            for x in self.active_wave.components:
                if x.generate == True:
                    x.ace = True
        else:
            self.active_wave.ace = False
            for x in self.active_wave.components:
                if x.generate == True:
                    x.ace = False

        event.Skip()


################################################################################
## Resource Functionality
################################################################################

    def displayResources(self):
        self.resourceBox.DeleteAllItems()
        troot = self.resourceBox.AddRoot("the_root")
        compRoot = self.resourceBox.AppendItem(troot,'Components',image=0)
        devRoot = self.resourceBox.AppendItem(troot,'Devices',image=1)
        nodeRoot = self.resourceBox.AppendItem(troot,'Nodes',image=1)

        for c in self.Available_Components:
            t1 = self.resourceBox.AppendItem(compRoot,c.name)
            self.resourceBox.SetPyData(t1,c)

        for c in self.Available_Devices:
            t1 = self.resourceBox.AppendItem(devRoot,c.name)
            self.resourceBox.SetPyData(t1,c)

        for n in self.Available_Nodes:
            t1 = self.resourceBox.AppendItem(nodeRoot,n.name)
            self.resourceBox.SetPyData(t1,n)


        if self.resourceBox.GetChildrenCount(troot,recursively=False) > 0:
            cid1,cookie1 = self.resourceBox.GetFirstChild(troot)
            self.resourceBox.SortChildren(cid1)
            for x in range(self.resourceBox.GetChildrenCount(troot,recursively=False)-1):
                cid1,cookie1 = self.resourceBox.GetNextChild(troot,cookie1)
                self.resourceBox.SortChildren(cid1)

    def loadResources(self):
        self.Available_Components = []
        self.Available_Devices = []
        self.Available_Nodes = []

        resList = []

        # List possible resource directories (components and device)
        baseComponentPath = self.installPath + 'xml/'
        if os.path.isdir(baseComponentPath):
            for r in os.listdir(baseComponentPath):
                if r != 'dtd':  # ignore dtd directory
                    resList.append( (baseComponentPath,r) )
        else:
            errorMsg(self,"No component resources could be found in: " + self.installPath)
            return

        # find the .scd.xml files for each resource
        for r in resList:
            tmpResName = r[1]
            tmpResPath = r[0] + r[1]
            tmpComp = importResource.getResource(tmpResPath,tmpResName,self)

            if tmpComp == None:
                continue
            if tmpComp.type == 'resource':
                self.Available_Components.append(tmpComp)
            elif tmpComp.type == 'executabledevice':
                self.Available_Devices.append(tmpComp)
            elif tmpComp.type == 'loadabledevice':
                self.Available_Devices.append(tmpComp)
            elif tmpComp.type == 'device':
                self.Available_Devices.append(tmpComp)

        nodeList = []
        if os.path.isdir(self.installPath + 'nodes'):
            nodeList = os.listdir(self.installPath + 'nodes')
        else:
            errorMsg(self, "No nodes could be found in: " + self.installPath)

        # find the scd files for each node
        for node_name in nodeList:

            # check for existence of DomainManager XML files
            nodes_root_path = self.installPath + os.path.sep + 'nodes' + os.path.sep + node_name + os.path.sep
            if not os.path.exists(nodes_root_path + 'DeviceManager.dcd.xml'):
                errorMsg(self, "Could not find DeviceManager.dcd.xml in: " + nodes_root_path)
                continue
            elif not os.path.exists(nodes_root_path + 'DeviceManager.prf.xml'):
                errorMsg(self, "Could not find DeviceManager.prf.xml in: " + nodes_root_path)
                continue
            elif not os.path.exists(nodes_root_path + 'DeviceManager.scd.xml'):
                errorMsg(self, "Could not find DeviceManager.scd.xml in: " + nodes_root_path)
                continue
            elif not os.path.exists(nodes_root_path + 'DeviceManager.spd.xml'):
                errorMsg(self, "Could not find DeviceManager.spd.xml in: " + nodes_root_path)
                continue

            nodeName = node_name
            nodePath = self.installPath + 'nodes/' + nodeName + '/'

            tmpNode = importNode.getNode(nodePath,nodeName,self)
            if tmpNode == None:
                print "WARNING: possibly an error reading node " + nodePath + "/" + nodeName
                continue
            self.Available_Nodes.append(tmpNode)

        self.displayResources()

    def OnRefreshResourceBtnButton(self, event):
        self.loadResources()


    #################################################################
    ## Resource Event Stuff
    #################################################################

    def OnResourceBoxPopupAddMenu(self, event):
        sn = self.resourceBox.GetSelection()
        tmpRes = None
        if (sn != self.resourceBox.GetRootItem() and self.resourceBox.GetItemParent(sn) != self.resourceBox.GetRootItem()):
            # a child component (Component or Device)
            tmpRes =  self.resourceBox.GetPyData(sn)
            if tmpRes.type == 'resource':
#            errorMsg(self,'You cannot add this type of resource to a waveform.  Right click to add to platform or node')
 #           return
                tmpBaseName = tmpRes.name
                tmpCount = 1
                for c in self.active_wave.components:
                    if c.baseName == tmpBaseName:
                        tmpCount += 1

                dlg = wx.TextEntryDialog(self, 'Please enter an instance name for this '\
                + tmpRes.name + ' component.', 'Enter Name', tmpRes.name + str(tmpCount))
                try:
                    returnCode = dlg.ShowModal()
                    if returnCode == wx.ID_OK:
                        newname = dlg.GetValue()
                        if len(newname) <= 0:
                            errorMsg(self,'Invalid instance name.')
                            dlg.Destroy()
                            return

                        for c in self.active_wave.components:
                            if newname == c.name:
                                errorMsg(self,'A component instance with this name already exists in your waveform.')
                                dlg.Destroy()
                                return
                    elif returnCode == wx.ID_CANCEL:
                        dlg.Destroy()
                        return
                finally:
                    dlg.Destroy()


                newRes = copy.deepcopy(tmpRes)
                newRes.name = newname
                newRes.baseName = tmpBaseName
                newRes.setUUID()    # this gives the component instance a unique id
        # we do not set the newRes.file_uuid because it is the same for all components of this type

                self.active_wave.components.append(newRes)
                self.displayComps()
                self.resourceBox.Unselect()
                event.Skip()

    def OnResourceBoxRightUp(self, event):
        self.OnResourceBoxPopupGetDescr(event)
        sn = self.resourceBox.GetSelection()
        tmpRes = None
        if sn == self.resourceBox.GetRootItem():
            for x in self.resourceBoxPopup.GetMenuItems():
                x.Enable(False)
        elif self.resourceBox.GetItemParent(sn) == self.resourceBox.GetRootItem():
            for x in self.resourceBoxPopup.GetMenuItems():
                x.Enable(False)
        else:
            # a child component (Component or Device)
            for x in self.resourceBoxPopup.GetMenuItems():
                    x.Enable(True)
            tmpRes =  self.resourceBox.GetPyData(sn)
            if tmpRes.type == 'resource':
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPADDDEV)
                x.Enable(False)
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPADDNODE)
                x.Enable(False)

                #x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPGETDESCR)
                #x.Enable(False)

                #disable Doxygen docs display if no docs directory found
                docsPath = self.installPath + 'docs/' + tmpRes.name
                if os.path.isdir(docsPath) != 1:
                    x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPGETDOXYGENREFMAN)
                    x.Enable(False)
            elif tmpRes.type == 'node':
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPADDDEV)
                x.Enable(False)
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPADD)
                x.Enable(False)
                #x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPGETDESCR)
                #x.Enable(False)
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPGETDOXYGENREFMAN)
                x.Enable(False)
            else:
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPADDNODE)
                x.Enable(False)
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPADD)
                x.Enable(False)
                #x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPGETDESCR)
                #x.Enable(False)
                x = self.resourceBoxPopup.FindItemById(wxID_FRAME1RESOURCEBOXPOPUPGETDOXYGENREFMAN)
                x.Enable(False)

        #if tmpRes != None:
        self.resourceBox.PopupMenu(self.resourceBoxPopup)
        event.Skip()

    def OnResourceBoxLeftUp(self, event):
        self.OnResourceBoxPopupGetDescr(event)

    def OnResourceBoxLeftDoubleClick(self, event):
        sn = self.resourceBox.GetSelection()
        if (sn != self.resourceBox.GetRootItem() and self.resourceBox.GetItemParent(sn) != self.resourceBox.GetRootItem()):
            # a child component (Component or Device)
            tmpRes =  self.resourceBox.GetPyData(sn)
            if tmpRes.type == 'resource':
                self.OnResourceBoxPopupAddMenu(event)
            elif tmpRes.type == 'node':
                self.OnResourceBoxPopupAddnodeMenu(event)
            elif (tmpRes.type == 'device' or tmpRes.type == 'loadabledevice' or tmpRes.type == 'executabledevice'):
                self.OnResourceBoxPopupAdddevMenu(event)

    def OnResourceBoxPopupAdddevMenu(self, event):
        sn = self.resourceBox.GetSelection()
        tmpRes =  self.resourceBox.GetPyData(sn)

        if len(self.active_plat.nodes) == 0:
            tmpstr = "There are no available nodes to add a device instance to.\n"
            tmpstr += "Please add a node to your design.  Platform->Add Deployment Node"
            errorMsg(self,tmpstr)
            return

        tmpBaseName = tmpRes.name
        #tmpCount = 1
        #for c in self.active_plat.nodes:
        #    for x in c.Devices:
        #        if x.baseName == tmpBaseName:
        #            tmpCount += 1

        #dlg = NodeDialog.create(self,self.active_plat.nodes,tmpBaseName + str(tmpCount))
        dlg = NodeDialog.create(self,self.active_plat.nodes,tmpBaseName)

        try:
            returnCode = dlg.ShowModal()
            if returnCode == wx.ID_OK:
                tmpnode = dlg.DeploymentNode
                newname = dlg.InstanceName
                tmpCount = 1
                iterator = 0
                basename = newname
                newname = newname+str(tmpCount)

                while iterator < len(tmpnode.Devices):
                    for c in tmpnode.Devices:
                        if newname == c.name:
                            tmpCount = tmpCount + 1
                            newname = basename+str(tmpCount)
                            iterator = 0
                            break
                        else:
                            iterator = iterator + 1

                        #errorMsg(self,'A device instance with this name already exists on ' + tmpnode.name + '.')
                        #dlg.Destroy()
                        #return
                #for c in tmpnode.Devices:
                #    if newname == c.name:
                #        tmpCount = tmpCount + 1
                        #errorMsg(self,'A device instance with this name already exists on ' + tmpnode.name + '.')
                        #dlg.Destroy()
                        #return
            else:
                dlg.Destroy()
                return
        finally:
            dlg.Destroy()


        newDev = copy.deepcopy(tmpRes)
        newDev.name = newname
        newDev.baseName = tmpBaseName
        newDev.generate = False
        newDev.node = tmpnode.name
        newDev.setUUID()    # this gives the device instance a unique id
        # we do not set the newDev.file_uuid because it is the same for all devices of this type

        tmpnode.Devices.append(newDev)
        self.displayNodes()
        self.resourceBox.Unselect()
        event.Skip()

    def OnResourceBoxPopupGetDescr(self, event):
        sn = self.resourceBox.GetSelection()
        tmpRes = None
        if (sn != self.resourceBox.GetRootItem() and self.resourceBox.GetItemParent(sn) != self.resourceBox.GetRootItem()):
            # a child component (Component or Device)
            tmpRes =  self.resourceBox.GetPyData(sn)
            self.resDescrBox.Clear()
            self.resDescrBox.WriteText(tmpRes.name + " (" + tmpRes.type + "):  " \
                + tmpRes.description)
        event.Skip()

    def OnResourceBoxPopupGetDoxygenRefMan(self, event):
        defaultHtml = 'index.html'
        defaultPdf = 'refman.pdf'
        docList = None
        sn = self.resourceBox.GetSelection()
        tmpRes = self.resourceBox.GetPyData(sn)
        docsPath = self.installPath + 'docs/' + tmpRes.name
        if os.path.isdir(docsPath):
            docList = os.listdir(docsPath)
            if os.path.isfile(docsPath + '/' + defaultHtml):
                webbrowser.open_new('file://' + docsPath + '/' + defaultHtml)
            elif os.path.isfile(docsPath + '/' + defaultPdf):
                #find more portable way to view pdf?
                try:
                    os.system('evince ' + docsPath + '/' + defaultPdf + ' &')
                finally:
                    errorMsg(self,'evince pdf viewer threw exception or not found')
                #webbrowser.open('file://' + docsPath + '/' + defaultPdf, 1)
            else:
                errorMsg(self,'Neither index.html nor refman.pdf found in ' + docsPath + ': directory listing: ' + str(docList))
        else:
            errorMsg(self,'No directory for ' + tmpRes.name + ' could be found in: ' + self.installPath + 'docs')
            return

    def OnResourceBoxPopupAddnodeMenu(self, event):
        sn = self.resourceBox.GetSelection()
        tmpNode =  self.resourceBox.GetPyData(sn)
        self.active_plat.nodes.append(tmpNode)
        self.displayNodes()
        event.Skip()

################################################################################
## Platform Layout Functionality
################################################################################

    def displayNodes(self):
        self.nodeBox.DeleteAllItems()
        troot = self.nodeBox.AddRoot("the_root")

        for n in self.active_plat.nodes:
            t1 = self.nodeBox.AppendItem(troot,n.name)
            self.nodeBox.SetPyData(t1,n)

            for d in n.Devices:
                t2 = self.nodeBox.AppendItem(t1,unicode(d.name))
                self.nodeBox.SetPyData(t2,d)

                for c in self.active_wave.components:
                    if c.device == d:
                        t3 = self.nodeBox.AppendItem(t2,c.name)
                        self.nodeBox.SetPyData(t3,c)

    def AddNode(self):
        tmpCount = len(self.active_plat.nodes) + 1

        dlg = wx.TextEntryDialog(self, 'Please enter a name for this node ',\
         'Enter Name', 'Node' + str(tmpCount))
        try:
            returnCode = dlg.ShowModal()
            if returnCode == wx.ID_OK:
                newname = dlg.GetValue()
                if len(newname) <= 0:
                    errorMsg(self,'Invalid instance name.')
                    dlg.Destroy()
                    return

                for c in self.active_plat.nodes:
                    if newname == c.name:
                        errorMsg(self,'A node with this name already exists in your design.')
                        dlg.Destroy()
                        return
            elif returnCode == wx.ID_CANCEL:
                dlg.Destroy()
                return
        finally:
            dlg.Destroy()

        #tmpNode = PlatformClass.Node(newname)
        tmpNode = ComponentClass.Node(name=newname)
        self.active_plat.nodes.append(tmpNode)
        self.displayNodes()

    def GenerateNodeBoxSelection(self):
        errorMsg(self, 'WARNING: You will have to regenerate your waveform if you continue')
        sn = self.nodeBox.GetSelection()

        #generate the dcd file for the selected node
        dlg = wx.DirDialog(self,"Please select the place to generate the code",style=wx.DD_NEW_DIR_BUTTON)
        dlg.SetPath(os.path.expanduser('~'))
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.path = dlg.GetPath()
            else:
                return
        finally:
            dlg.Destroy()
        active_node = None

        tmp_count = 0
        duplicate_name_flag = False
        for n in self.active_plat.nodes:
            if n==self.nodeBox.GetPyData(sn):
                dev_count = 0
                while dev_count < len(self.active_plat.nodes[tmp_count].Devices):
                    tmp_uuid = unicode(uuidgen())
                    n.Devices[dev_count].uuid = tmp_uuid
                    self.active_plat.nodes[tmp_count].Devices[dev_count].uuid = tmp_uuid
                    dev_count = dev_count + 1
                active_node = n
                break
            tmp_count = tmp_count + 1
        if active_node == None:
            print "This should never happen - the node names don't match"
            return


        gen = genNode.genAll(self.path, self.wavedevPath, copy.deepcopy(active_node))
        gen.genDirs()
        gen.writeMakefile()
        # TODO: use different configure.ac file for node -JDG
        gen.genConfigureACFiles(self.installPath)
        xml_gen.genDeviceManager(n, self.path, self.wavedevPath, n.name, "DeviceManager", False)


    def RemoveNodeBoxSelection(self):
        sn = self.nodeBox.GetSelection()
        snParent = self.nodeBox.GetItemParent(sn)
        if snParent == self.nodeBox.GetRootItem():
            # a platform node
            tmpMsg = "        Are you sure you want to remove this Node?\n\n"
            tmpMsg += "All device instances assigned to this node will be removed,\n"
            tmpMsg += "and all components assignments to these devices will voided."
            if owdMsg(self,tmpMsg) == False:
                return
            tmpNode = self.nodeBox.GetPyData(sn)
            for n in self.active_plat.nodes:
                if tmpNode == n:
                    for d in n.Devices:
                        # If any other component is connected to this device - connection must be removed
                        for c in self.active_wave.components:
                            for con in c.connections:
                                if con.remoteComp == d:
                                    ci = c.connections.index(con)
                                    del c.connections[ci]
                        for c in self.active_wave.components:
                            if c.device == d:
                                c.device = None
                    dIndex = self.active_plat.nodes.index(tmpNode)
                    del self.active_plat.nodes[dIndex]

        elif self.nodeBox.GetItemParent(snParent) == self.nodeBox.GetRootItem():
            # a device instance
            tmpMsg = "Are you sure you want to remove this Device Instance?\n\n"
            tmpMsg += "All component assignments to this devices will voided."
            if owdMsg(self,tmpMsg) == False:
                return
            tmpDev = self.nodeBox.GetPyData(sn)
            # If any other component is connected to this device - connection must be removed
            for c in self.active_wave.components:
                for con in c.connections:
                    if con.remoteComp == tmpDev:
                        ci = c.connections.index(con)
                        del c.connections[ci]

            for n in self.active_plat.nodes:
                for d in n.Devices:
                    if tmpDev == d:
                        for c in self.active_wave.components:
                            if c.device == d:
                                c.device = None
                        dIndex = n.Devices.index(tmpDev)
                        del n.Devices[dIndex]
        else:
            # a component assignment
            tmpMsg = "Are you sure you want to void this component assignment?\n\n"
            if owdMsg(self,tmpMsg) == False:
                return
            tmpComp = self.nodeBox.GetPyData(sn)
            tmpComp.device = None

        self.displayNodes()
        self.displayComps()


    #################################################################
    ## Platform Event Stuff
    #################################################################

    def OnNodeBoxRightUp(self, event):
        sn = self.nodeBox.GetSelection()
        if sn != self.nodeBox.GetRootItem():
            snParent = self.nodeBox.GetItemParent(sn)
        if sn == self.nodeBox.GetRootItem():
            self.nodeBoxPopup.Enable(wxID_FRAME1NODEBOXPOPUPREMOVE,False)
            self.nodeBoxPopup.Enable(wxID_FRAME1NODEBOXPOPUPRENAME,False)
        elif snParent == self.nodeBox.GetRootItem():
            # a platform node
            for x in self.nodeBoxPopup.GetMenuItems():
                x.Enable(True)
            self.nodeBoxPopup.Enable(wxID_FRAME1NODEBOXPOPUPGENERATE,True)
        elif self.nodeBox.GetItemParent(snParent) == self.nodeBox.GetRootItem():
            # a device instance
            for x in self.nodeBoxPopup.GetMenuItems():
                x.Enable(True)
            self.nodeBoxPopup.Enable(wxID_FRAME1NODEBOXPOPUPGENERATE,False)
        else:
            # a component assignment
            for x in self.nodeBoxPopup.GetMenuItems():
                x.Enable(True)
            self.nodeBoxPopup.Enable(wxID_FRAME1NODEBOXPOPUPGENERATE,False)
            self.nodeBoxPopup.Enable(wxID_FRAME1NODEBOXPOPUPRENAME,False)

        self.nodeBox.PopupMenu(self.nodeBoxPopup)
        event.Skip()

    def OnNodeBoxPopupAddnodeMenu(self, event):
        self.AddNode()
        event.Skip()

    def OnNodeBoxPopupRemoveMenu(self, event):
        self.RemoveNodeBoxSelection()
        event.Skip()

    def OnNodeBoxPopupGenerateMenu(self, event):
        self.GenerateNodeBoxSelection()
        event.Skip()

    def OnNodeBoxPopupExpandMenu(self, event):
        troot = self.nodeBox.GetRootItem()
        if self.nodeBox.ItemHasChildren(troot):
            cid1,cookie1 = self.nodeBox.GetFirstChild(troot)
            self.ExpandTreeNode(self.nodeBox,cid1)
            cid1 = self.nodeBox.GetNextSibling(cid1)
            while cid1.IsOk():
                self.ExpandTreeNode(self.nodeBox,cid1)
                cid1 = self.nodeBox.GetNextSibling(cid1)

        event.Skip()

    def OnNodeBoxPopupRefreshMenu(self, event):
        self.displayNodes()
        event.Skip()

    def OnNodeBoxPopupRenameMenu(self, event):
        sn = self.nodeBox.GetSelection()
        self.nodeBox.EditLabel(sn)
        event.Skip()

    def OnNodeBoxTreeBeginLabelEdit(self, event):
        sn = self.nodeBox.GetSelection()
        snParent = self.nodeBox.GetItemParent(sn)
        if snParent == self.nodeBox.GetRootItem():
            # a platform node
            pass
        elif self.nodeBox.GetItemParent(snParent) == self.nodeBox.GetRootItem():
            # a device instance
            pass
        else:
            # a child component (connection)
            event.Veto()
            return
        event.Skip()

    def OnNodeBoxTreeEndLabelEdit(self, event):
        if event.IsEditCancelled():
            event.Veto()
            return
        sn = event.GetItem()
        snParent = self.nodeBox.GetItemParent(sn)
        if snParent == self.nodeBox.GetRootItem():
            # a platform node
            tempNode = self.nodeBox.GetPyData(sn)
            newname = event.GetLabel()
            if len(newname) > 0:
                for n in self.active_plat.nodes:
                    if n != tempNode and n.name == newname:
                        errorMsg(self,'Invalid name - a node by that name already exists')
                        event.Veto()
                        return

                #Node names with spaces do not work
                if newname.find(' ') != -1:
                    errorMsg(self,'Node names can not have spaces in them.')
                    event.Veto()
                    return

                tempNode.name = newname
            else:
                errorMsg(self,'Invalid name - must have at least one character!')
                event.Veto()
                return
        elif self.nodeBox.GetItemParent(snParent) == self.nodeBox.GetRootItem():
            # a device instance
            tempDev = self.nodeBox.GetPyData(sn)
            snNode = self.nodeBox.GetItemParent(sn)
            tempNode = self.nodeBox.GetPyData(snNode)
            newname = event.GetLabel()
            if len(newname) > 0:
                for d in tempNode.Devices:
                    if d != tempDev and d.name == newname:
                        errorMsg(self,'Invalid name - a device instance with that name already exists')
                        event.Veto()
                        return

                #Device names with spaces do not work
                if newname.find(' ') != -1:
                    errorMsg(self,'Device names can not have spaces in them.')
                    event.Veto()
                    return

                tempDev.changeName(newname)

        else:
            # a child component (connection)
            event.Veto()
            return

        event.Skip()

    #################################################################
    ## Platform Menu Stuff
    #################################################################

    def OnMenuPlatformAddnodeMenu(self, event):
        self.AddNode()
        event.Skip()


################################################################################
## General Environment Functionality
################################################################################


    def ExpandTreeNode(self, whichBox, nodeId):
        if whichBox.ItemHasChildren(nodeId):
            whichBox.Expand(nodeId)
            cid1,cookie1 = whichBox.GetFirstChild(nodeId)
            self.ExpandTreeNode(whichBox,cid1)
            cid1 = whichBox.GetNextSibling(cid1)
            while cid1.IsOk():
                self.ExpandTreeNode(whichBox,cid1)
                cid1 = self.nodeBox.GetNextSibling(cid1)

###############################################################################
## LoadConfiguration
## This function is not a part of the frame class so that other modules can
## call it
###############################################################################
def LoadConfiguration(frame_obj):
    '''Extracts information from configuration file'''
    root = __file__
    if os.path.islink (root):
        root = os.path.realpath (root)
    root = os.path.dirname (os.path.abspath (root))

    doc_cfg = xml.dom.minidom.parse(root + '/../wavedev.cfg')

    # version
    try:
        frame_obj.version = \
                str(doc_cfg.getElementsByTagName("version")[0].firstChild.data)
    except:
        frame_obj.version = "unknown"

    # install path
    try:
        frame_obj.installPath = \
                str(doc_cfg.getElementsByTagName("installpath")[0].firstChild.data)
        if frame_obj.installPath[len(frame_obj.installPath)-1] != '/':
            frame_obj.installPath = frame_obj.installPath + '/'
    except:
        frame_obj.installPath = ""

    # standard IDL path
    use_default_stdidlpath = False
    try:
        frame_obj.stdIdlPath = str(doc_cfg.getElementsByTagName("stdidlpath")[0].firstChild.data)
    except:
        frame_obj.stdIdlPath = ""
    if len(frame_obj.stdIdlPath) > 0:
        if frame_obj.stdIdlPath[len(frame_obj.stdIdlPath)-1] != '/':
            frame_obj.stdIdlPath = frame_obj.stdIdlPath + '/'
        # see if directory actually exists
        if not os.path.isdir(frame_obj.stdIdlPath):
            print "warning: wavedev.cfg stdidl path " + frame_obj.stdIdlPath + " does not exist"
            print "  => using default standard idl path instead"
            use_default_stdidlpath = True
    else:
        use_default_stdidlpath = True

    if use_default_stdidlpath:
        if os.path.isdir("/usr/include/standardinterfaces"):
            frame_obj.stdIdlPath = "/usr/include/standardinterfaces/"
        elif os.path.isdir("/usr/local/include/standardinterfaces"):
            frame_obj.stdIdlPath = "/usr/local/include/standardinterfaces/"
        else:
            tmpstr = "StandardInterfaces does not appear to be installed!\n"
            tmpstr += "You will not be able to add ports to components.\n\n"
            tmpstr += "If you have standardinterfaces installed in a location\n"
            tmpstr += "other than the default, please specify that location\n"
            tmpstr += "in the wavedev.cfg file located in the top directory."
            errorMsg(frame_obj,tmpstr)


    # custom IDL path
    use_default_customidlpath = False
    try:
        frame_obj.customIdlPath = str(doc_cfg.getElementsByTagName("customidlpath")[0].firstChild.data)
    except:
        frame_obj.customIdlPath = ""
    if len(frame_obj.customIdlPath) > 0:
        if frame_obj.customIdlPath[len(frame_obj.customIdlPath)-1] != '/':
            frame_obj.customIdlPath = frame_obj.customIdlPath + '/'
        # see if directory actually exists
        if not os.path.isdir(frame_obj.customIdlPath):
            print "warning: wavedev.cfg customidl path " + frame_obj.customIdlPath + " does not exist"
            print "  => using default custom idl path instead"
            use_default_customidlpath = True
    else:
        use_default_customidlpath = True

    if use_default_customidlpath:
        if os.path.isdir("/usr/include/custominterfaces"):
            frame_obj.customIdlPath = "/usr/include/custominterfaces/"
        elif os.path.isdir("/usr/local/include/custominterfaces"):
            frame_obj.customIdlPath = "/usr/local/include/custominterfaces/"
        else:
            tmpstr = "CustomInterfaces does not appear to be installed!\n"
            tmpstr += "You will not be able to add ports to components.\n\n"
            tmpstr += "If you have standardinterfaces installed in a location\n"
            tmpstr += "other than the default, please specify that location\n"
            tmpstr += "in the wavedev.cfg file located in the top directory."
            errorMsg(frame_obj,tmpstr)

    # ossie include path
    try:
        frame_obj.ossieIncludePath = \
                str(doc_cfg.getElementsByTagName("ossieincludepath")[0].firstChild.data)
    except:
        frame_obj.ossieIncludePath = ""

    if len(frame_obj.ossieIncludePath) > 0:
        if frame_obj.ossieIncludePath[len(frame_obj.ossieIncludePath)-1] != '/':
            frame_obj.ossieIncludePath = frame_obj.ossieIncludePath + '/'
    else:
        if os.path.isdir("/usr/include/ossie"):
            frame_obj.ossieIncludePath = "/usr/include/ossie/"
        elif os.path.isdir("/usr/local/include/ossie"):
            frame_obj.ossieIncludePath = "/usr/local/include/ossie/"
        else:
            tmpstr = "OSSIE does not appear to be installed!\n"
            tmpstr += "You will not be able to add ports to components\n"
            tmpstr += "using CF interfaces.\n\n"
            tmpstr += "If you have ossie installed in a location other than\n"
            tmpstr += "the default please specify that location in the\n"
            tmpstr += "wavedev.cfg file located in the top directory."
            errorMsg(frame_obj,tmpstr)

    # home directory
    try:
        frame_obj.homeDir = str(doc_cfg.getElementsByTagName("homedir")[0].firstChild.data)
    except:
        frame_obj.homeDir = ""

    if len(frame_obj.homeDir) > 0:
        if frame_obj.homeDir[len(frame_obj.homeDir)-1] != '/':
            frame_obj.homeDir = frame_obj.homeDir + '/'


