#Boa:Dialog:PropertiesDialog

import os
import wx
import wx.gizmos
import ComponentClass as CC
from errorMsg import *
import commands
import uuidgen

def create(parent):
    return PropertiesDialog(parent)

[wxID_PROPERTIESDIALOG, wxID_PROPERTIESDIALOGACTIONCHOICE,
 wxID_PROPERTIESDIALOGADDPROP, wxID_PROPERTIESDIALOGADDVALUE,
 wxID_PROPERTIESDIALOGCANCEL, wxID_PROPERTIESDIALOGDESCRIPTION,
 wxID_PROPERTIESDIALOGELEMENTCHOICE, wxID_PROPERTIESDIALOGENUMBOX,
 wxID_PROPERTIESDIALOGIDBOX, wxID_PROPERTIESDIALOGKINDCHOICE,
 wxID_PROPERTIESDIALOGMAXBOX, wxID_PROPERTIESDIALOGMINBOX,
 wxID_PROPERTIESDIALOGMODECHOICE, wxID_PROPERTIESDIALOGNAMEBOX,
 wxID_PROPERTIESDIALOGOK, wxID_PROPERTIESDIALOGSASHWINDOW1,
 wxID_PROPERTIESDIALOGSASHWINDOW2, wxID_PROPERTIESDIALOGSPLITTERWINDOW1,
 wxID_PROPERTIESDIALOGSTATICTEXT1, wxID_PROPERTIESDIALOGSTATICTEXT10,
 wxID_PROPERTIESDIALOGSTATICTEXT11, wxID_PROPERTIESDIALOGSTATICTEXT12,
 wxID_PROPERTIESDIALOGSTATICTEXT2, wxID_PROPERTIESDIALOGSTATICTEXT3,
 wxID_PROPERTIESDIALOGSTATICTEXT4, wxID_PROPERTIESDIALOGSTATICTEXT5,
 wxID_PROPERTIESDIALOGSTATICTEXT6, wxID_PROPERTIESDIALOGSTATICTEXT7,
 wxID_PROPERTIESDIALOGSTATICTEXT8, wxID_PROPERTIESDIALOGSTATICTEXT9,
 wxID_PROPERTIESDIALOGTYPECHOICE, wxID_PROPERTIESDIALOGUNITSCHOICE,
 wxID_PROPERTIESDIALOGVALUEBOX, wxID_PROPERTIESDIALOGVALUELIST,
] = [wx.NewId() for _init_ctrls in range(34)]

[wxID_PROPERTIESDIALOGVALUELISTPOPUPREMOVE] = [wx.NewId() for _init_coll_valueListPopup_Items in range(1)]

class PropertiesDialog(wx.Dialog):
    def _init_coll_valueListPopup_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_PROPERTIESDIALOGVALUELISTPOPUPREMOVE,
              kind=wx.ITEM_NORMAL, text=u'Remove')
        self.Bind(wx.EVT_MENU, self.OnValueListPopupRemoveMenu,
              id=wxID_PROPERTIESDIALOGVALUELISTPOPUPREMOVE)

    def _init_coll_valueList_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading=u'Value',
              width=92)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Default', width=92)

    def _init_utils(self):
        # generated method, don't edit
        self.valueListPopup = wx.Menu(title=u'')

        self._init_coll_valueListPopup_Items(self.valueListPopup)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_PROPERTIESDIALOG,
              name=u'PropertiesDialog', parent=prnt, pos=wx.Point(483, 325),
              size=wx.Size(775, 446), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Properties')
        self._init_utils()
        self.SetClientSize(wx.Size(775, 446))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_ACTIVATE, self.OnPropertiesDialogActivate)

        self.AddProp = wx.Button(id=wxID_PROPERTIESDIALOGADDPROP,
              label=u'Add Property', name=u'AddProp', parent=self,
              pos=wx.Point(439, 399), size=wx.Size(125, 30), style=0)
        self.AddProp.Bind(wx.EVT_BUTTON, self.OnAddPropButton,
              id=wxID_PROPERTIESDIALOGADDPROP)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_PROPERTIESDIALOGSPLITTERWINDOW1,
              name='splitterWindow1', parent=self, point=wx.Point(8, 79),
              size=wx.Size(760, 308), style=wx.ALWAYS_SHOW_SB | wx.SP_3D)
        self.splitterWindow1.SetBestFittingSize(wx.Size(760, 305))

        self.sashWindow2 = wx.SashWindow(id=wxID_PROPERTIESDIALOGSASHWINDOW2,
              name='sashWindow2', parent=self.splitterWindow1, pos=wx.Point(204,
              0), size=wx.Size(556, 305),
              style=wx.ALWAYS_SHOW_SB | wx.CLIP_CHILDREN | wx.HSCROLL | wx.VSCROLL | wx.SW_3D)
        self.sashWindow2.SetAutoLayout(True)
        self.sashWindow2.SetBestFittingSize(wx.Size(556, 285))
        self.sashWindow2.SetMaximumSizeY(375)

        self.nameBox = wx.TextCtrl(id=wxID_PROPERTIESDIALOGNAMEBOX,
              name=u'nameBox', parent=self, pos=wx.Point(208, 40),
              size=wx.Size(144, 25), style=0, value=u'')

        self.idBox = wx.TextCtrl(id=wxID_PROPERTIESDIALOGIDBOX, name=u'idBox',
              parent=self, pos=wx.Point(360, 40), size=wx.Size(283, 25),
              style=0, value=u'')

        self.typeChoice = wx.Choice(choices=["boolean", "char", "double",
              "float", "short", "long", "objref", "octet", "string", "ulong",
              "ushort"], id=wxID_PROPERTIESDIALOGTYPECHOICE, name=u'typeChoice',
              parent=self.sashWindow2, pos=wx.Point(32, 105), size=wx.Size(100,
              27), style=0)
        self.typeChoice.SetBestFittingSize(wx.Size(100, 27))

        self.elementChoice = wx.Choice(choices=["Simple", "SimpleSequence",
              "Test", "Struct", "StructSequence"],
              id=wxID_PROPERTIESDIALOGELEMENTCHOICE, name=u'elementChoice',
              parent=self, pos=wx.Point(32, 40), size=wx.Size(152, 27),
              style=0)
        self.elementChoice.Bind(wx.EVT_CHOICE, self.OnElementChoiceChoice,
              id=wxID_PROPERTIESDIALOGELEMENTCHOICE)

        self.modeChoice = wx.Choice(choices=["readonly", "readwrite",
              "writeonly"], id=wxID_PROPERTIESDIALOGMODECHOICE,
              name=u'modeChoice', parent=self, pos=wx.Point(653, 39),
              size=wx.Size(104, 27), style=0)

        self.description = wx.TextCtrl(id=wxID_PROPERTIESDIALOGDESCRIPTION,
              name=u'description', parent=self.sashWindow2, pos=wx.Point(16,
              32), size=wx.Size(272, 40), style=wx.TE_MULTILINE, value=u'')

        self.unitsChoice = wx.Choice(choices=["None", "Hz", "W", "V", "cycles_per_sample"],
              id=wxID_PROPERTIESDIALOGUNITSCHOICE, name=u'unitsChoice',
              parent=self.sashWindow2, pos=wx.Point(185, 105), size=wx.Size(85,
              27), style=0)
        self.unitsChoice.SetBestFittingSize(wx.Size(85, 27))

        self.minBox = wx.TextCtrl(id=wxID_PROPERTIESDIALOGMINBOX,
              name=u'minBox', parent=self.sashWindow2, pos=wx.Point(184, 236),
              size=wx.Size(80, 25), style=0, value=u'min')

        self.maxBox = wx.TextCtrl(id=wxID_PROPERTIESDIALOGMAXBOX,
              name=u'maxBox', parent=self.sashWindow2, pos=wx.Point(184, 268),
              size=wx.Size(80, 25), style=0, value=u'max')

        self.staticText1 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT1,
              label=u'Description', name='staticText1', parent=self.sashWindow2,
              pos=wx.Point(16, 11), size=wx.Size(76, 17), style=0)

        self.kindChoice = wx.Choice(choices=["allocation", "configure", "test",
              "execparam", "factoryparam"], id=wxID_PROPERTIESDIALOGKINDCHOICE,
              name=u'kindChoice', parent=self.sashWindow2, pos=wx.Point(27,
              170), size=wx.Size(110, 27), style=0)
        self.kindChoice.SetBestFittingSize(wx.Size(110, 27))
        self.kindChoice.Bind(wx.EVT_CHOICE, self.OnKindChoiceChoice,
              id=wxID_PROPERTIESDIALOGKINDCHOICE)

        self.staticText2 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT2,
              label=u'Type', name='staticText2', parent=self.sashWindow2,
              pos=wx.Point(65, 84), size=wx.Size(39, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT3,
              label=u'Units', name='staticText3', parent=self.sashWindow2,
              pos=wx.Point(212, 84), size=wx.Size(41, 17), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT4,
              label=u'Kind', name='staticText4', parent=self.sashWindow2,
              pos=wx.Point(69, 149), size=wx.Size(36, 17), style=0)

        self.staticText5 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT5,
              label=u'Range', name='staticText5', parent=self.sashWindow2,
              pos=wx.Point(205, 215), size=wx.Size(48, 17), style=0)

        self.staticText6 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT6,
              label=u'Value(s)', name='staticText6', parent=self.sashWindow2,
              pos=wx.Point(362, 23), size=wx.Size(58, 17), style=0)

        self.sashWindow1 = wx.SashWindow(id=wxID_PROPERTIESDIALOGSASHWINDOW1,
              name='sashWindow1', parent=self.splitterWindow1, pos=wx.Point(0,
              0), size=wx.Size(199, 305), style=wx.CLIP_CHILDREN | wx.SW_3D)
        self.splitterWindow1.SplitVertically(self.sashWindow1, self.sashWindow2,
              200)

        self.valueBox = wx.TextCtrl(id=wxID_PROPERTIESDIALOGVALUEBOX,
              name=u'valueBox', parent=self.sashWindow2, pos=wx.Point(336, 44),
              size=wx.Size(100, 25), style=0, value=u'')
        self.valueBox.SetBestFittingSize(wx.Size(100, 25))

        root = __file__
        if os.path.islink (root):
              root = os.path.realpath (root)
        root = os.path.dirname (os.path.abspath (root))
        self.addValue = wx.BitmapButton(bitmap=wx.Bitmap( root + '/images/plus.bmp',
              wx.BITMAP_TYPE_BMP), id=wxID_PROPERTIESDIALOGADDVALUE,
              name=u'addValue', parent=self.sashWindow2, pos=wx.Point(456, 44),
              size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.addValue.Bind(wx.EVT_BUTTON, self.OnAddValueButton,
              id=wxID_PROPERTIESDIALOGADDVALUE)

        self.staticText7 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT7,
              label=u'Element Type', name='staticText7', parent=self,
              pos=wx.Point(57, 16), size=wx.Size(141, 17), style=0)

        self.staticText8 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT8,
              label=u'Name', name='staticText8', parent=self, pos=wx.Point(252,
              16), size=wx.Size(45, 17), style=0)

        self.staticText9 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT9,
              label=u'ID', name='staticText9', parent=self, pos=wx.Point(485,
              16), size=wx.Size(24, 17), style=0)

        self.staticText10 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT10,
              label=u'Mode', name='staticText10', parent=self, pos=wx.Point(687,
              16), size=wx.Size(42, 17), style=0)

        self.valueList = wx.ListCtrl(id=wxID_PROPERTIESDIALOGVALUELIST,
              name=u'valueList', parent=self.sashWindow2, pos=wx.Point(316, 82),
              size=wx.Size(185, 206),
              style=wx.ALWAYS_SHOW_SB | wx.LC_EDIT_LABELS | wx.LC_VRULES | wx.LC_REPORT | wx.SIMPLE_BORDER | wx.LC_HRULES | wx.VSCROLL | wx.LC_SINGLE_SEL)
        self.valueList.SetBestFittingSize(wx.Size(185, 206))
        self._init_coll_valueList_Columns(self.valueList)
        self.valueList.Bind(wx.EVT_RIGHT_UP, self.OnValueListRightUp)

        self.Cancel = wx.Button(id=wxID_PROPERTIESDIALOGCANCEL, label=u'Cancel',
              name=u'Cancel', parent=self, pos=wx.Point(680, 399),
              size=wx.Size(85, 30), style=0)
        self.Cancel.Bind(wx.EVT_BUTTON, self.OnCancelButton,
              id=wxID_PROPERTIESDIALOGCANCEL)

        self.enumBox = wx.TextCtrl(id=wxID_PROPERTIESDIALOGENUMBOX,
              name=u'enumBox', parent=self.sashWindow2, pos=wx.Point(20, 251),
              size=wx.Size(125, 25), style=0, value=u'')

        self.staticText11 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT11,
              label=u'Enumeration', name=u'staticText11',
              parent=self.sashWindow2, pos=wx.Point(36, 230), size=wx.Size(90,
              17), style=0)

        self.ok = wx.Button(id=wxID_PROPERTIESDIALOGOK, label=u'OK', name=u'ok',
              parent=self, pos=wx.Point(579, 399), size=wx.Size(85, 30),
              style=0)
        self.ok.Bind(wx.EVT_BUTTON, self.OnOkButton, id=wxID_PROPERTIESDIALOGOK)

        self.actionChoice = wx.Choice(choices=["eq", "ne", "gt", "lt", "ge",
              "le", "external"], id=wxID_PROPERTIESDIALOGACTIONCHOICE,
              name=u'actionChoice', parent=self.sashWindow2, pos=wx.Point(185,
              170), size=wx.Size(85, 27), style=0)

        self.staticText12 = wx.StaticText(id=wxID_PROPERTIESDIALOGSTATICTEXT12,
              label=u'Action', name='staticText12', parent=self.sashWindow2,
              pos=wx.Point(209, 149), size=wx.Size(50, 17), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.parent = parent
        self.calledByParent = False
        self.active_prop = None

    def OnPropertiesDialogActivate(self, event):
        if self.calledByParent == True:

            self.active_comp = self.parent.active_comp

            if self.active_prop == None:
                self.elementType = "Simple"
                self.elementChoice.SetSelection(0)
                self.modeChoice.SetSelection(0)
                self.typeChoice.SetStringSelection("short")
                self.kindChoice.SetStringSelection("configure")
                self.unitsChoice.SetStringSelection("None")
                self.AddProp.Enable(True)
                self.idBox.SetValue("DCE:"+uuidgen.uuidgen())
                self.ok.Enable(False)
            else:
                #read in the property and display
                self.AddProp.Enable(False)
                self.ok.Enable(True)
                self.idBox.SetValue(self.active_prop.id)
                self.nameBox.SetValue(self.active_prop.name)
                tmp = self.modeChoice.FindString(self.active_prop.mode)
                self.modeChoice.SetSelection(tmp)
                self.elementType = self.active_prop.elementType
                tmp = self.elementChoice.FindString(self.elementType)
                self.elementChoice.SetSelection(tmp)
                self.description.SetValue(self.active_prop.description)

                self.initializeDisplay()

            self.unitsChoice.Enable(False) # we don't support units yet

            self.refreshDisplay()

            self.calledByParent = False
        event.Skip()

    def OnPropBoxLeftUp(self, event):
        self.propBox.Refresh()

        event.Skip()

    def OnElementChoiceChoice(self, event):
        pos = self.elementChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            return
        self.elementType = self.elementChoice.GetString(pos)
        if self.elementType != "Simple" and self.elementType != "SimpleSequence":
            errorMsg(self,'This element type is not supported yet!')
            self.elementType = "Simple"
            self.elementChoice.SetSelection(0)

        self.refreshDisplay()
        event.Skip()

    def refreshDisplay(self):
        if self.active_prop != None:

            if self.active_prop.elementType == "Simple":
                pass
        if self.elementType == "Simple":
            if self.valueList.GetItemCount() >= 1:
                self.addValue.Enable(False)
            else:
                self.addValue.Enable(True)
            self.enumBox.Enable(True)

            pos = self.kindChoice.GetSelection()
            if pos != wx.NOT_FOUND:
                if self.kindChoice.GetString(pos) == "allocation":
                    self.actionChoice.Enable(True)
                else:
                    self.actionChoice.Enable(False)

        elif self.elementType == "SimpleSequence":
            self.addValue.Enable(True)
            self.enumBox.Enable(False)

    def initializeDisplay(self):
        if self.elementType == "Simple" or self.elementType == "SimpleSequence":
            # Load the type (ie. long, string, boolean)
            pos = self.typeChoice.FindString(self.active_prop.type)
            self.typeChoice.SetSelection(pos)

            # Load the action (ie. eq, lt, ge)
            if self.active_prop.action != None:
                pos = self.actionChoice.FindString(self.active_prop.action)
                self.actionChoice.SetSelection(pos)

            # Load the kind (ie. allocation, configure, execparam)
            pos = self.kindChoice.FindString(self.active_prop.kind)
            self.kindChoice.SetSelection(pos)

            # Load the range of the value(s)
            if self.active_prop.range[0] == -1 and self.active_prop.range[1] == -1:
                pass
            else:
                self.minBox.SetValue(str(self.active_prop.range[0]))
                self.maxBox.SetValue(str(self.active_prop.range[1]))

            # If this is already installed on the system - can't change anything but the value(s)
            if self.editable == False:
                self.nameBox.Enable(False)
                self.idBox.Enable(False)
                self.typeChoice.Enable(False)
                self.kindChoice.Enable(False)
                self.elementChoice.Enable(False)
                self.actionChoice.Enable(False)
                self.enumBox.Enable(False)
                self.minBox.Enable(False)
                self.maxBox.Enable(False)
                self.modeChoice.Enable(False)
                self.description.Enable(False)

        if self.elementType == "Simple":
            # Load the value for a Simple type
            self.valueList.InsertStringItem(0,unicode(self.active_prop.value))
            self.valueList.SetStringItem(0,1,unicode(self.active_prop.defaultValue))

            # Load the enumeration
            if self.active_prop.enum != '':
                self.enumBox.SetValue(self.active_prop.enum)

        if self.elementType == "SimpleSequence":
            for v in self.active_prop.values:
                self.valueList.InsertStringItem(0,v)  #create list (backwards at first)
            tmpPropCounter = 0
            for v in self.active_prop.values:
                self.valueList.SetStringItem(tmpPropCounter,0,v)  #set the items in the listin the correct order
                tmpPropCounter = tmpPropCounter + 1
            tmpPropCounter = 0
            for dv in self.active_prop.defaultValues:
                self.valueList.SetStringItem(tmpPropCounter,1,dv)
                tmpPropCounter = tmpPropCounter + 1

    def OnBitmapButton1Button(self, event):
        event.Skip()

    def OnAddValueButton(self, event):
        tmpStr = self.valueBox.GetLineText(0)
        if tmpStr != '':
            self.valueList.InsertStringItem(0,tmpStr)
            self.valueList.SetStringItem(0,1,tmpStr)
            self.valueBox.Clear()

        self.refreshDisplay()
        event.Skip()

    def OnValueListPopupRemoveMenu(self, event):
        if self.editable == False:
            errorMsg(self,"This property is not removable!")
            return
        sel = self.valueList.GetFirstSelected()
        if sel >= 0:
            if self.elementType == "Simple":
                self.addValue.Enable(True)
            self.valueList.DeleteItem(sel)
        event.Skip()

    def OnValueListRightUp(self, event):
        self.valueList.PopupMenu(self.valueListPopup)

        event.Skip()

    def OnCancelButton(self, event):
        self.Close()
        event.Skip()

    def OnAddPropButton(self, event):
        # Check for the name
        tmpName = self.nameBox.GetLineText(0)
        if tmpName == '':
            errorMsg(self,"Please enter a property name first!")
            return

        # Check for the id
        tmpid = self.idBox.GetLineText(0)
        if tmpid == '':
            errorMsg(self,"Please enter a property id first!")
            return

        # Check for the mode
        pos = self.modeChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            errorMsg(self,"Please select a property mode first!")
            return
        tmpMode = self.modeChoice.GetString(pos)

        # Get the description
        tmpDes = self.description.GetValue()

        # Check for the type ex: bool, char, short, etc.
        pos = self.typeChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            errorMsg(self,"Please select a type first!")
            return
        tmpType = self.typeChoice.GetString(pos)

        if self.elementType == "Simple":
            # instantiate the property object
            newProp = CC.SimpleProperty(tmpName,tmpMode,tmpType,tmpDes)

            # store the default value and the value
            if self.valueList.GetItemCount() == 0:
                errorMsg(self,"Please enter a value first!")
                return

            v = self.valueList.GetItem(0,0)
            dv = self.valueList.GetItem(0,1)
            newProp.value = v.GetText()
            newProp.defaultValue = dv.GetText()

        if self.elementType == "SimpleSequence":
            # store the default value and the value
            if self.valueList.GetItemCount() == 0:
                    errorMsg(self,"Please enter a value first!")
                    return

            newProp = CC.SimpleSequenceProperty(tmpName,tmpMode,tmpType,tmpDes)


            newProp.values = []
            newProp.defaultValues = []

            for x in range(self.valueList.GetItemCount()):
                v = self.valueList.GetItem(x,0)
                dv = self.valueList.GetItem(x,1)

                newProp.values.append(v.GetText())
                newProp.defaultValues.append(dv.GetText())

        # store the enum if any
        newProp.enum = self.enumBox.GetLineText(0)

        # Check for the kind ex: allocation, configure, test, etc.
        pos = self.kindChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            errorMsg(self,"Please select a kind first!")
            return
        newProp.kind = self.kindChoice.GetString(pos)

        # Check and store the range
        tmpMin = self.minBox.GetLineText(0)
        tmpMax = self.maxBox.GetLineText(0)

        if tmpMin == 'min' or tmpMin == '':
            tmpMin = -1

        if tmpMax == 'max' or tmpMax == '':
            tmpMax = -1

        newProp.range = (tmpMin,tmpMax)

        # Check and store the action
        pos = self.actionChoice.GetSelection()
        if pos == wx.NOT_FOUND:
            if newProp.kind == "allocation":
                errorMsg(self,"Please select an action first!")
                return
        else:
            newProp.action = self.actionChoice.GetString(pos)

        self.parent.active_comp.properties.append(newProp)
        self.Close()

        event.Skip()

    def OnOkButton(self, event):
        if self.editable:
            # Check for the name
            tmpName = self.nameBox.GetLineText(0)
            if tmpName == '':
                errorMsg(self,"Please enter a property name first!")
                return
            self.active_prop.name = tmpName

            # Check for the id
            tmpid = self.idBox.GetLineText(0)
            if tmpid == '':
                errorMsg(self,"Please enter a property id first!")
                return
            self.active_prop.id = tmpid

            # Check for the mode
            pos = self.modeChoice.GetSelection()
            if pos == wx.NOT_FOUND:
                errorMsg(self,"Please select a property mode first!")
                return
            tmpMode = self.modeChoice.GetString(pos)
            self.active_prop.mode = tmpMode

            # Get the description
            tmpDes = self.description.GetValue()
            self.active_prop.description = tmpDes

            # Check for the type ex: bool, char, short, etc.
            pos = self.typeChoice.GetSelection()
            if pos == wx.NOT_FOUND:
                errorMsg(self,"Please select a type first!")
                return
            tmpType = self.typeChoice.GetString(pos)
            self.active_prop.type = tmpType

            if self.elementType == "Simple":
                # store the default value and the value
                if self.valueList.GetItemCount() == 0:
                    errorMsg(self,"Please enter a value first!")
                    return

                v = self.valueList.GetItem(0,0)
                dv = self.valueList.GetItem(0,1)
                self.active_prop.value = v.GetText()
                self.active_prop.defaultValue = dv.GetText()

            if self.elementType == "SimpleSequence":
                # store the default value and the value
                if self.valueList.GetItemCount() == 0:
                    errorMsg(self,"Please enter a value first!")
                    return

                self.active_prop.values = []
                self.active_prop.defaultValues = []

                for x in range(self.valueList.GetItemCount()):
                    v = self.valueList.GetItem(x,0)
                    dv = self.valueList.GetItem(x,1)

                    self.active_prop.values.append(v.GetText())
                    self.active_prop.defaultValues.append(dv.GetText())

            # store the enum if any
            self.active_prop.enum = self.enumBox.GetLineText(0)

            # Check for the kind ex: allocation, configure, test, etc.
            pos = self.kindChoice.GetSelection()
            if pos == wx.NOT_FOUND:
                errorMsg(self,"Please select a kind first!")
                return
            self.active_prop.kind = self.kindChoice.GetString(pos)

            # Check and store the range
            tmpMin = self.minBox.GetLineText(0)
            tmpMax = self.maxBox.GetLineText(0)

            if tmpMin == 'min' or tmpMin == '':
                tmpMin = -1

            if tmpMax == 'max' or tmpMax == '':
                tmpMax = -1

            self.active_prop.range = (tmpMin,tmpMax)

            # Check and store the action
            pos = self.actionChoice.GetSelection()
            if pos == wx.NOT_FOUND:
                if self.active_prop.kind == "allocation":
                    errorMsg(self,"Please select an action first!")
                    return
            else:
                self.active_prop.action = self.actionChoice.GetString(pos)

        else:
            if self.elementType == "Simple":
                # store the default value and the value
                if self.valueList.GetItemCount() == 0:
                    errorMsg(self,"Please enter a value first!")
                    return

                v = self.valueList.GetItem(0,0)
                dv = self.valueList.GetItem(0,1)
                self.active_prop.value = v.GetText()
                self.active_prop.defaultValue = dv.GetText()

            if self.elementType == "SimpleSequence":
                # store the default value and the value
                if self.valueList.GetItemCount() == 0:
                    errorMsg(self,"Please enter a value first!")
                    return

                self.active_prop.values = []
                self.active_prop.defaultValues = []

                for x in range(self.valueList.GetItemCount()):
                    v = self.valueList.GetItem(x,0)
                    dv = self.valueList.GetItem(x,1)
                    self.active_prop.values.append(v.GetText())
                    self.active_prop.defaultValues.append(dv.GetText())

        self.Close()

    def OnKindChoiceChoice(self, event):
        self.refreshDisplay()
        event.Skip()
