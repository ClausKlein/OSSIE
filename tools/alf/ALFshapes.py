## Copyright 2005, 2006, 2007, 2008 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE ALF Waveform Application Visualization Environment
##
## ALF is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## ALF is distributed in the hope that it will be useful, but WITHOUT ANY
## WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE Waveform Developer; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import wx
from wx.lib import ogl
import ALF

# This module defines the shapes used in ALF
#--------------------------------------------------------------------------------------------------------------
[wxID_PORT_POPUP_INFO, wxID_PORT_POPUP_COLOR] = [wx.NewId() for x in range(2)]
[wxID_COMP_POPUP_SENDTO] = [wx.NewId() for x in range(1)]
[wxID_PORT_MENU_INFO] = [wx.NewId() for x in range(1)]
[wxID_COMP_POPUP_USES, wxID_COMP_POPUP_PROVIDES] = [wx.NewId() for x in range(2)]

brushList = []
def initializeColours():
    colourDB = wx.ColourDatabase()
    colourStrs = ["LIGHT BLUE", "GREEN", "GOLD", "SIENNA", "VIOLET",
        "WHEAT", "RED", "DARK GREEN", "DIM GREY", "STEEL BLUE", "ORANGE",
        "YELLOW GREEN", "THISTLE", "WHITE", "CYAN", "CORNFLOWER BLUE"]
    for x in colourStrs:
        brushList.append(wx.Brush(colourDB.Find(x)))

#--------------------------------------------------------------------------------------------------------------
class ComponentShape(ogl.CompositeShape, ogl.DividedShape):
    """ComponentShape provides a graphical representation of an SCA component using OGL."""
    def __init__(self, canvas, component, wave_display):
        """__init__(self, canvas, component)

        Constructor for ComponentShape.  Sets up default shape sizes, regions, and constraints."""

        ogl.CompositeShape.__init__(self)
        self.compSizeX = 150
        self.compSizeY = 100
        ogl.DividedShape.__init__(self, self.compSizeX, self.compSizeY)
	
        self.SetCanvas(canvas)
        self.component = component
        self.canvas = canvas
        self.wave_display = wave_display    # Stores reference to encapsulating object - handles tool updates

        self.portSizeX = 10
        self.portSizeY = 10
        self.gaugeSizeX = 50
        self.gaugeSizeY = self.portSizeY
        self.portSpacing = 4
        
        nameRegion = ogl.ShapeRegion()
        nameRegion.SetText(component.name)
        nameRegion.SetProportions(0.0, 0.1)
        nameRegion.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        #nameRegion.SetFont(wx.Font(8, wx.SWISS, wx.BOLD, wx.BOLD))
        self.AddRegion(nameRegion)
        self.SetRegionSizes()
        self.ReformatRegions(canvas)

        self.constraining_shape = ogl.RectangleShape(self.compSizeX, self.compSizeY)
        self.uses_shapes = []
        self.prov_shapes = []
        self.gauge_shapes = []

        self.active_provides_port = None

        self.constraining_shape.SetBrush(wx.GREY_BRUSH)
        self.AddChild(self.constraining_shape)
        
        for p in component.ports:
            self.addPort(p)

        uses_constraints = []
        provides_constraints = []
        uses_constraints = self.createPortConstraints(self.constraining_shape, self.uses_shapes,"RIGHT")
        provides_constraints = self.createPortConstraints(self.constraining_shape, self.prov_shapes,"LEFT")

        for x in uses_constraints:
            self.AddConstraint(x)
        for x in provides_constraints:
            self.AddConstraint(x)
           
        self.setupTimingDisplay()
        self.Recompute()

        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        self.constraining_shape.SetDraggable(False)
        for x in self.uses_shapes:
            x.SetDraggable(False)
        for x in self.prov_shapes:
            x.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        self.constraining_shape.SetSensitivityFilter(0)
        
        # Setup a wx.Window so that we can support "right-click"ing
        self.window = wx.Window(self.GetCanvas(), id=-1, size=wx.Size(-1,-1))
        self.window.Show(False)

        self.compPopup = wx.Menu(title='')
        self.usesMenu = wx.Menu(title='')
        self.providesMenu = wx.Menu(title='')
        self._init_compPopup_Items(self.compPopup)


    def _init_usesMenu_Items(self, parent):
        """Initialize the menu that displays options for the uses ports in a component."""
        for port in self.component.ports:
            if port.type == "Uses":
                parent.AppendMenu(help='', id=-1, submenu=port.shape.portMenu, text=port.name)
                port.shape.setupPortMenuEventBindings(self.window)
    
    def _init_providesMenu_Items(self, parent):
        for port in self.component.ports:
            if port.type == "Provides":
                parent.AppendMenu(help='', id=-1, submenu=port.shape.portMenu, text=port.name)
                port.shape.setupPortMenuEventBindings(self.window)

    def _init_compPopup_Items(self, parent):
        self._init_usesMenu_Items(self.usesMenu)
        self._init_providesMenu_Items(self.providesMenu)
        parent.AppendMenu(help='', id=-1, submenu=self.usesMenu, text='Uses')
        parent.AppendMenu(help='', id=-1, submenu=self.providesMenu, text='Provides')

    def addPort(self, port):
        """Add a PortShape object to the component"""

        cs = PortShape(port, self.component, self.wave_display, self.portSizeX, self.portSizeY, self.GetCanvas())
        if port.type == "Uses":
            cs.SetBrush(wx.BLACK_BRUSH)
            self.uses_shapes.append(cs)
        else:
            self.prov_shapes.append(cs)
        
        port.shape = cs 
        cs.port = port

        self.AddChild(cs)

    def createPortConstraints(self, constraining_shape, shapes, orientation):
        """Create the contstraints needed to display the ports in relation to the component.
           Uses ports on the right and provides ports on the left."""
        if len(shapes) == 0:
            return []
        if orientation == "RIGHT":
            position = ogl.CONSTRAINT_RIGHT_OF
        else:
            position = ogl.CONSTRAINT_LEFT_OF
            
        constraints = []
        if len(shapes) > 0:
            constraints.append(ogl.Constraint(position,constraining_shape, [shapes[0]]))
            topShape = bottomShape = shapes[0]
            for x in range(1,len(shapes)):
                constraints.append(ogl.Constraint(ogl.CONSTRAINT_ALIGNED_LEFT,
                    topShape, [shapes[x]]))
                
                tmpCon = None
                if x%2:
                    tmpCon = ogl.Constraint(ogl.CONSTRAINT_ABOVE, topShape, [shapes[x]])
                    constraints.append(tmpCon)
                    tmpCon.SetSpacing(0,self.portSpacing)
                    topShape = shapes[x]
                else:
                    tmpCon = ogl.Constraint(ogl.CONSTRAINT_BELOW, bottomShape, [shapes[x]])
                    constraints.append(tmpCon)
                    tmpCon.SetSpacing(0,self.portSpacing)
                    bottomShape = shapes[x]
            return constraints

        else:
            return None

    def processTimingEvent(self, port_name, function_name, description, time_s, time_us, number_samples):
        """Process the timing event received by passing it on to the appropriate port or gauge."""

        for port in self.component.ports:
            if port.name == port_name:
                # Setup the gauges is displaying graphics
                if port.type == "Uses":
                    if not port.shape.gauge.show_gauge:
                        if self.canvas.frame.timing_view_state:
                            port.shape.gauge.ShowGauge(True)
                    else:
                        if not self.canvas.frame.timing_view_state:
                            port.shape.gauge.ShowGauge(False)
                    if self.active_provides_port != None and port.shape.gauge.provides_port == None:
                        port.shape.gauge.provides_port = self.active_provides_port
                        
                # Initialize the active provides port on the component: used for displaying gauges
                if port.type == "Provides" and self.active_provides_port == None:
                    self.active_provides_port = port
                    
                # Update gauges if displaying graphics
                if self.canvas.frame.timing_view_state:
                    for g in self.gauge_shapes:
                        g.processTimingEvent(port, description)

                port.shape.processTimingEvent(function_name, description, time_s, time_us, number_samples)

    def setupTimingDisplay(self):
        """Setup the initial timing display for the component."""

        for port in self.component.ports:
            if port.type == "Uses":
                self.addGauge(port)

    def addGauge(self, port):
        """Add a new GaugeShape to the component to be used when displaying timing events."""
    
        new_gauge = GaugeShape(self.gaugeSizeX,self.gaugeSizeY,self.GetCanvas(),port)
        port.shape.gauge = new_gauge
        self.gauge_shapes.append(new_gauge)
        self.AddChild(new_gauge)
        self.createGaugeConstraint(port.shape, new_gauge)
        new_gauge.SetDraggable(False)
       
    def createGaugeConstraint(self, constraining_shape, shape):
        """Create the contraints used to display the gauges in relation to uses ports they represent."""

        position1 = ogl.CONSTRAINT_LEFT_OF
        constraint = ogl.Constraint(position1, constraining_shape, [shape])
        self.AddConstraint(constraint)
        
        position2 = ogl.CONSTRAINT_CENTRED_VERTICALLY
        constraint = ogl.Constraint(position2, constraining_shape, [shape])
        self.AddConstraint(constraint)

    def ReformatRegions(self, canvas=None):
        """Used to format the regions of a composite shape."""
    
        rnum = 0
        if canvas is None:
            canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)  # used for measuring
        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1

    def GetChildShapes(self):
        tmpshapes = []
        tmpshapes.append(self.constraining_shape)
        for x in self.uses_shapes:
            tmpshapes.append(x)
            tmpshapes.extend(x.GetChildShapes())
        for x in self.prov_shapes:
            tmpshapes.append(x)
            tmpshapes.extend(x.GetChildShapes())
            tmpshapes.extend(x.GetLines())
        return tmpshapes 

    #--------------------------
    # Event handling
    #--------------------------
    def OnRightClick(self, x, y, keys=0, attachment=0):
        """Event handler for the Right Click event on the ComponentShape."""

        self.window.PopupMenu(self.compPopup)
    
    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        """Event handler for the Left Click event on the ComponentShape."""

        shape = self
        canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []
            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                canvas.Redraw(dc)

#----------------------------------------------------------------------

class PortShape(ogl.RectangleShape):
    def __init__(self, port, parent_component, wave_display, w=0.0, h=0.0, canvas=None):
        ogl.RectangleShape.__init__(self, w, h)
        self.port = port
        self.parent_component = parent_component
        self.SetCanvas(canvas)
        self.brushIndex = 0
        self.gauge = None
        self.show_timing_display = False    # Used to keep from having to refresh port display when
                                            # timing display is turned off
        self.wave_display = wave_display

        # Store the timing info; each operation function supported by the port's
        # interface has a tuple, [0,0], for both input and output timing events
        self.timingData = {}
        
        # The operations are populated when ALF is loaded and the interfaces are imported
        for op in self.port.interface.operations:
            self.timingData[op.name] = {}
            self.timingData[op.name]['begin'] = [0,0,0,0,0]   # [sec, usec, num_samples]
            self.timingData[op.name]['end'] = [0,0,0,0,0]     # [sec, usec, num_samples]
        
        self.window = wx.Window(self.GetCanvas(), id=-1, size=wx.Size(-1,-1))
        self.window.Show(False)

        self.id_tool_dict = {}
        self.wxID_PORT_INFO = wx.NewId()

        self.portMenu = wx.Menu(title='')
        self.portMenuId = wx.NewId()
        self._init_portMenu_Items(self.portMenu)
        self.port_info_shape = None

    def setupPortMenuEventBindings(self, window):
        """Bind the menu events to the OnPortMenu event handler with the proper ids."""
        
        # Bind the PortInfo click first since they all have it
        window.Bind(wx.EVT_MENU, self.OnPortMenuInfoMenu, id=self.wxID_PORT_INFO)       # Bind component event
        self.window.Bind(wx.EVT_MENU, self.OnPortMenuInfoMenu, id=self.wxID_PORT_INFO)  # Bind port event

        # Bind the tool events now
        for x in self.id_tool_dict.keys():
            window.Bind(wx.EVT_MENU, self.OnPortMenu, id=x)         # Bind component event
            self.window.Bind(wx.EVT_MENU, self.OnPortMenu, id=x)    # Bind port event
    
    def _init_portMenu_Items(self, parent):
        self.portMenu.Append(id=self.wxID_PORT_INFO, kind=wx.ITEM_NORMAL, text='Info')
        self.portMenu.AppendSeparator()
        
        if self.GetCanvas().frame.tools == None:
            return
            
        supportedTools = None
        supportedTools = self.GetCanvas().frame.tools.getSupportedTools(self.port.interface.nameSpace, self.port.interface.name)

        if supportedTools != None:
            for x in supportedTools:
                newid = wx.NewId()
                self.portMenu.Append(id=newid, kind=wx.ITEM_NORMAL, text=str(x.name))
                self.id_tool_dict[newid] = x

    def processTimingEvent(self, function_name, description, time_s, time_us, number_samples):
        """Process the timing event for this port.  Store the timing information in self.timingData
           and forward the event to display if enabled."""

        opname = function_name
        opwhere = description
        old_time_us = 0
        old_time_s = 0
        if opname not in self.timingData.keys():
            print "This shouldn't really ever print, because the operations should have all already been imported"
            self.timingData[opname] = {}
            self.timingData[opname]['begin'] = [0,0,0,0,0]
            self.timingData[opname]['end'] = [0,0,0,0,0]
            old_time_s = time_s
            old_time_us = time_us
        else:
            old_time_s = self.timingData[opname][opwhere][0]
            old_time_us = self.timingData[opname][opwhere][1]
        
        self.timingData[opname][opwhere] = [time_s, time_us, number_samples, old_time_s, old_time_us]   # store timing info
        if self.port_info_shape != None:
            self.port_info_shape.UpdateText()
        if self.GetCanvas().frame.timing_view_state:
            if opwhere == "end":
                locker = wx.MutexGuiLocker()
                self.SetBrush(brushList[self.brushIndex])
                canvas = self.GetCanvas()
                dc = wx.ClientDC(canvas)
                canvas.PrepareDC(dc)
           
                r = self.GetRegions()
                x,y = r[0].GetSize()
                rect = wx.Rect(self.GetX()-x/2,self.GetY()-y/2,x,y)
                canvas.RefreshRect(rect)
                canvas.frame.Update()
                
                self.brushIndex = (self.brushIndex+1)%(len(brushList))

            # Set local flag for timing display
            if not self.show_timing_display:
                self.show_timing_display = True
        else:
            # Timing display has been turned off, but the port display hasn't been refreshed yet
            if self.show_timing_display:
                locker = wx.MutexGuiLocker()
                if (self.port.type == "Uses"):
                    self.SetBrush(wx.BLACK_BRUSH)
                else:
                    self.SetBrush(wx.WHITE_BRUSH)
                canvas = self.GetCanvas()
                dc = wx.ClientDC(canvas)
                canvas.PrepareDC(dc)
           
                r = self.GetRegions()
                x,y = r[0].GetSize()
                rect = wx.Rect(self.GetX()-x/2,self.GetY()-y/2,x,y)
                canvas.RefreshRect(rect)
                canvas.frame.Update()
                
                self.show_timing_display = False
    
    def GetChildShapes(self):
        tmpshapes = []
        if self.gauge != None:
            tmpshapes.append(self.gauge)
        tmpshapes.extend(self.GetLines())
        return tmpshapes

    
    #--------------------------
    # Event handling
    #--------------------------
    def OnPortMenu(self, event):
        id = event.GetId()
        if self.id_tool_dict.has_key(id):
            self.displayTool(self.id_tool_dict[id])

    def OnRightClick(self, x, y, keys=0, attachment=0):
        self.window.PopupMenu(self.portMenu)
    
    def OnPortMenuInfoMenu(self, event):
        self.displayPortInfoPopup()
    
    def displayPortInfoPopup(self):
        ds = PortInfoShape(240,150,self.GetCanvas(),self.port, self)
        ds.SetDraggable(True, True)
        ds.SetBrush(wx.Brush("WHEAT", wx.SOLID))
        dc = wx.ClientDC(self.GetCanvas())
        self.GetCanvas().PrepareDC(dc)
        ds.SetCanvas(self.GetCanvas)
        ds.SetShadowMode(ogl.SHADOW_RIGHT)
        self.GetCanvas().diagram.AddShape(ds)

        ds.Show(True)

        self.GetCanvas().shapes.append(ds)
        line = ogl.LineShape()
        line.SetCanvas(self.GetCanvas())
        line.SetPen(wx.BLACK_PEN)
        line.SetBrush(wx.BLACK_BRUSH)
        line.AddArrow(ogl.ARROW_ARROW)
        line.MakeLineControlPoints(2)
        self.AddLine(line, ds)
        self.GetCanvas().diagram.AddShape(line)
        line.Show(True)
        ds.line = line
                                                                                                                        
        ds.Move(dc, self.GetX()+25, self.GetY()+150)
        self.port_info_shape = ds
    
    def displayTool(self, tool):
        if tool.module == None:
            # NOTE: alf_plugins is now the package that contains all tools
            exec_string = "from alf_plugins." + tool.packagename + " import "
            exec_string += tool.modulename + " as tool_module"
            exec exec_string

            tool.module = tool_module
        else:
            tool_module = tool.module
            reload(tool_module)

        naming_context = ("DomainName1", self.GetCanvas().frame.active_wave.naming_context, self.parent_component.name)
        #newframe = tool_module.create(self.GetCanvas().frame, str(self.port.interface.nameSpace),
        newframe = tool_module.create(self.wave_display, str(self.port.interface.nameSpace),
            str(self.port.interface.name), naming_context, str(self.port.name))
        newframe.Show(True)
        #self.GetCanvas().frame.tool_frames.append(newframe)
        self.wave_display.tool_frames.append(newframe)
        #wav_data = self.GetCanvas().frame.last_waveform_data_update
        wav_data = self.wave_display.last_waveform_data_update
        if wav_data != None:
            if hasattr(newframe, 'updateWaveformData'):
                newframe.updateWaveformData(wav_data)
   
#----------------------------------------------------------------------

class PortInfoShape(ogl.DividedShape):
    def __init__(self, x=0.0, y=0.0, canvas=None, port=None, parent_port=None):
    
        ogl.DividedShape.__init__(self, x, y)

        nameRegion = ogl.ShapeRegion()
        nameRegion.SetText(port.name)
        nameRegion.SetProportions(0.0, 0.2)
        nameRegion.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        self.AddRegion(nameRegion)
       
        intRegion = ogl.ShapeRegion()
        ts = port.interface.nameSpace + "::" + port.interface.name
        intRegion.SetText(ts)
        intRegion.SetProportions(0.0, 0.3)
        intRegion.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        self.AddRegion(intRegion)
        self.canvas = canvas
        
        opRegion = ogl.ShapeRegion()
        self.parent_port = parent_port
        ts = ''

        for op in port.interface.operations:
            ts += op.cxxReturnType + " " + op.name + " ("
            for x in range(len(op.params)):
                param = op.params[x]
                ts += param.direction + " " + param.cxxType + " " + param.name
                if x != len(op.params)-1:
                    ts += ", "
                else:
                    ts += ")"
            if (self.parent_port.timingData[op.name]['end'][2] != 0):
                time_diff = (self.parent_port.timingData[op.name]['end'][0]-self.parent_port.timingData[op.name]['end'][3])+((self.parent_port.timingData[op.name]['end'][1]-self.parent_port.timingData[op.name]['end'][4])/1000000.0)
                throughput = self.parent_port.timingData[op.name]['end'][2]/time_diff
                ts += "\n\tThroughput: " + "%.2f" % throughput + " sps"
            if op != port.interface.operations[len(port.interface.operations)-1]:
                ts += "\n"

        opRegion.SetText(ts)
        opRegion.SetProportions(0.0, 0.5)
        opRegion.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        x,y = opRegion.GetSize()
        self.text_region = opRegion
        self.port = port
        self.AddRegion(opRegion)

        self.SetRegionSizes()
        self.ReformatRegions(canvas)
    
    def UpdateText(self):
        ts=''
        for op in self.port.interface.operations:
            ts += op.cxxReturnType + " " + op.name + " ("
            for x in range(len(op.params)):
                param = op.params[x]
                ts += param.direction + " " + param.cxxType + " " + param.name
                if x != len(op.params)-1:
                    ts += ", "
                else:
                    ts += ")"
            if (self.parent_port.timingData[op.name]['end'][2] != 0):
                time_diff = (self.parent_port.timingData[op.name]['end'][0]-self.parent_port.timingData[op.name]['end'][3])+((self.parent_port.timingData[op.name]['end'][1]-self.parent_port.timingData[op.name]['end'][4])/1000000.0)
                throughput = self.parent_port.timingData[op.name]['end'][2]/time_diff
                ts += "\n\tThroughput: " + "%.2f" % throughput + " sps"
            if op != self.port.interface.operations[len(self.port.interface.operations)-1]:
                ts += "\n"

        self.text_region.SetText(ts)
        self.ReformatRegions(self.canvas)
        locker = wx.MutexGuiLocker()
        
        canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
        r = self.GetRegions()
        x,y = r[2].GetSize()
        rect = wx.Rect(self.GetX()-x/2,self.GetY(),x,y)
        canvas.RefreshRect(rect)
        canvas.frame.Update()
        #self.GetCanvas().Refresh()


    def ReformatRegions(self, canvas=None):
        rnum = 0
        if canvas is None:
            canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)  # used for measuring
        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1
    
    #--------------------------
    # Event handling
    #--------------------------
    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.DividedShape.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.SetRegionSizes()
        self.ReformatRegions()
        self.GetCanvas().Refresh()

    def OnRightClick(self, x, y, keys=0, attachment=0):
        # Remove info box and line from canvas
        self.parent_port.port_info_shape = None
        dc = wx.ClientDC(self.GetCanvas())
        self.GetCanvas().PrepareDC(dc)
        if self.Selected():
            self.Select(False, dc)
        self.RemoveLine(self.line)
        self.GetCanvas().diagram.RemoveShape(self.line)
        self.GetCanvas().diagram.RemoveShape(self)
        self.GetCanvas().Refresh()

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        shape = self
        canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []
            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                canvas.Redraw(dc)

#----------------------------------------------------------------------
class GaugeShape(ogl.RectangleShape):
    def __init__(self, w=0.0, h=0.0, canvas=None, port=None):
        ogl.RectangleShape.__init__(self, w, h)
        self.uses_port = port
        self.provides_port = None
        if canvas != None:
            self.SetCanvas(canvas)
        self.gauge_range = 100

        self.gauge = wx.Gauge(self.GetCanvas(), id=-1, range=self.gauge_range,
            size=wx.Size(int(w),int(h)), style=wx.GA_HORIZONTAL)
        self.gauge.Show(False)
        self.show_gauge = False
        self.gauge.SetValue(75)
        self.delta = 5
    
    def ShowGauge(self, show):
        if show:
            locker = wx.MutexGuiLocker()
            self.show_gauge = True
            self.Show(True)
            self.gauge.Show(True)
            self.GetCanvas().Refresh()
        else:
            locker = wx.MutexGuiLocker()
            self.show_gauge = False
            self.Show(False)
            self.gauge.Show(False)
            self.GetCanvas().Refresh()
            
    def processTimingEvent(self, port, description):
        if self.GetCanvas().frame.timing_view_state:
            locker = wx.MutexGuiLocker()
            current_value = self.gauge.GetValue()
            if port == self.uses_port:
                if self.GetCanvas().frame.timing_view_state:
                    if current_value - self.delta < 0:
                        self.gauge.SetValue(self.gauge_range)
                    else:    
                        self.gauge.SetValue(current_value - self.delta)
            if port == self.provides_port:
                if self.GetCanvas().frame.timing_view_state:
                    if current_value + self.delta > self.gauge_range:
                        self.gauge.SetValue(0)
                    else:    
                        self.gauge.SetValue(current_value + self.delta)
    
    #--------------------------
    # Event handling
    #--------------------------
    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        r = self.GetRegions()
        rx,ry = r[0].GetSize()
        gauge_size = self.gauge.GetSizeTuple()
        if rx != gauge_size[0] or ry != gauge_size[1]:
            self.gauge.SetSize(wx.Size(rx,ry))
            
        self.gauge.Move((x-rx/2,y-ry/2))
    
    def OnDraw(self, dc):
        if not self.show_gauge:
            self.Show(False)
        ogl.RectangleShape.OnDraw(self, dc)

# -------------------------------------------------------------------------------------------------
class WaveformShapes(wx.Window):
    """A wrapper class to encapsulate all the shapes and tool data for a waveform instance"""
    def __init__(self, waveform, canvas):
        self.waveform = waveform
        self.canvas = canvas
        self.tool_frames = []
        self.shapes = []
        self.lines = []

        # This is a little bit of a workaround so we can pass an instance of this class
        # to spawned tools so they can have encapsulated metadata
        self.window = wx.Window(canvas, id=-1, size=wx.Size(-1,-1))
        wx.Window.__init__(self,parent=self.window, id=-1)
        self.window.Show(False)
        
        # Structures to deal with storage and updating of tools
        self.waveformData = {}
        self.last_waveform_data_update = None
        self.tool_frames = []

        self.comp_locationX = 100
        self.comp_locationY = 200

    def AddTool(self, frame):
        self.tool_frames.append(frame)

    def AddComponentShape(self, comp):
        tmpshape = ComponentShape(self.canvas, comp, self)
        
        # Composites have to be moved for all children to get in place
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)
        tmpshape.Move(dc, self.comp_locationX, self.comp_locationY)

        tmpshape.SetX(self.comp_locationX)
        tmpshape.SetY(self.comp_locationY)
        tmpshape.SetPen(wx.BLACK_PEN)
        tmpshape.SetBrush(wx.RED_BRUSH)

        comp.shape = tmpshape

        self.shapes.extend(tmpshape.GetChildShapes())
        self.shapes.append(tmpshape)
        self.comp_locationX += 200

    def ConnectComponents(self):
        """Show the connections between components with lines"""

        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)

        for comp in self.waveform.components:
            for con in comp.connections:
                if not hasattr(con.localPort,"shape"):
                    return
                if not hasattr(con.remotePort,"shape"):
                    return
                fromShape = con.localPort.shape
                toShape = con.remotePort.shape

                line = ogl.LineShape()
                line.SetCanvas(self.canvas)
                line.SetPen(wx.BLACK_PEN)
                line.SetBrush(wx.BLACK_BRUSH)
                line.AddArrow(ogl.ARROW_ARROW)
                line.MakeLineControlPoints(2)
                fromShape.AddLine(line, toShape)

                #self.lines.append(line)
                self.shapes.append(line)
                #self.diagram.AddShape(line)
                #line.Show(True)

                # for some reason, the shapes have to be moved for the line to show up...
                #fromShape.Move(dc, fromShape.GetX(), fromShape.GetY())
        
    def updateWaveformData(self, data):
        for d in data:
            self.waveformData[d[0]] = d[1]

        self.last_waveform_data_update = self.waveformData.copy()

        for frame in self.tool_frames:
            if hasattr(frame, 'updateWaveformData'):
                frame.updateWaveformData(self.waveformData)

    def removeToolFrame(self, frame):
        if frame not in self.tool_frames:
            return
        else:
            index = self.tool_frames.index(frame)
            del self.tool_frames[index]
                                                        

