#!/usr/bin/env python

## Copyright 2007 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE ALF plot tool.
##
## OSSIE ALF plot is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## OSSIE ALF plot is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE ALF plot; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import  string as _string
import  time as _time
import  wx
import sys
from omniORB import CORBA
import CosNaming
from ossie.cf import CF, CF__POA
from ossie.standardinterfaces import standardInterfaces
from ossie.standardinterfaces import standardInterfaces__POA
import time, threading
import struct
import math
import sys

# Needs Numeric or numarray
try:
    #import Numeric as _Numeric
    import numpy as _Numeric
except:
    try:
        import numarray as _Numeric  #if numarray is used it is renamed Numeric
    except:
        msg= """
        This module requires the Numeric or numarray module,
        which could not be imported.  It probably is not installed
        (it's not part of the standard Python distribution). See the
        Python site (http://www.python.org) for information on
        downloading source or binaries."""
        raise ImportError, "Numeric or numarray not found. \n" + msg

# See if standardInterfaces.MetaData is available
try:
    x = standardInterfaces.MetaData
    # RadioMetaData interface is installed
    HAVE_RADIO_METADATA = True
except AttributeError:
    # RadioMetaData interface is not installed
    HAVE_RADIO_METADATA = False

#
# Plotting classes...
#
class PolyPoints:
    """Base Class for lines and markers
        - All methods are private.
    """

    def __init__(self, points, attr):
        self.points = _Numeric.array(points)
        self.currentScale= (1,1)
        self.currentShift= (0,0)
        self.scaled = self.points
        self.attributes = {}
        self.attributes.update(self._attributes)
        for name, value in attr.items():   
            if name not in self._attributes.keys():
                raise KeyError, "Style attribute incorrect. Should be one of %s" % self._attributes.keys()
            self.attributes[name] = value
        
    def boundingBox(self):
        if len(self.points) == 0:
            # no curves to draw
            # defaults to (-1,-1) and (1,1) but axis can be set in Draw
            minXY= _Numeric.array([-1,-1])
            maxXY= _Numeric.array([ 1, 1])
        else:
            minXY= _Numeric.minimum.reduce(self.points)
            maxXY= _Numeric.maximum.reduce(self.points)
        return minXY, maxXY

    def scaleAndShift(self, scale=(1,1), shift=(0,0)):
        if len(self.points) == 0:
            # no curves to draw
            return
        if (scale is not self.currentScale) or (shift is not self.currentShift):
            # update point scaling
            self.scaled = scale*self.points+shift
            self.currentScale= scale
            self.currentShift= shift
        # else unchanged use the current scaling
        
    def getLegend(self):
        return self.attributes['legend']

    def getClosestPoint(self, pntXY, pointScaled= True):
        """Returns the index of closest point on the curve, pointXY, scaledXY, distance
            x, y in user coords
            if pointScaled == True based on screen coords
            if pointScaled == False based on user coords
        """
        if pointScaled == True:
            #Using screen coords
            p = self.scaled
            pxy = self.currentScale * _Numeric.array(pntXY)+ self.currentShift
        else:
            #Using user coords
            p = self.points
            pxy = _Numeric.array(pntXY)
        #determine distance for each point
        d= _Numeric.sqrt(_Numeric.add.reduce((p-pxy)**2,1)) #sqrt(dx^2+dy^2)
        pntIndex = _Numeric.argmin(d)
        dist = d[pntIndex]
        return [pntIndex, self.points[pntIndex], self.scaled[pntIndex], dist]

class PolyLine(PolyPoints):
    """Class to define line type and style
        - All methods except __init__ are private.
    """
    
    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.SOLID,
                   'legend': ''}

    def __init__(self, points, **attr):
        """Creates PolyLine object
            points - sequence (array, tuple or list) of (x,y) points making up line
            **attr - key word attributes
                Defaults:
                    'colour'= 'black',          - wx.Pen Colour any wx.NamedColour
                    'width'= 1,                 - Pen width
                    'style'= wx.SOLID,          - wx.Pen style
                    'legend'= ''                - Line Legend to display
        """
        PolyPoints.__init__(self, points, attr)

    def draw(self, dc, printerScale, coord= None):
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale
        style= self.attributes['style']
        pen = wx.Pen(wx.NamedColour(colour), width, style)
        pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(pen)
        if coord == None:
            dc.DrawLines(self.scaled)
        else:
            dc.DrawLines(coord) # draw legend line

    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        h= self.attributes['width'] * printerScale
        w= 5 * h
        return (w,h)

class PolyMarker(PolyPoints):
    """Class to define marker type and style
        - All methods except __init__ are private.
    """
  
    _attributes = {'colour': 'black',
                   'width': 1,
                   'size': 2,
                   'fillcolour': None,
                   'fillstyle': wx.SOLID,
                   'marker': 'circle',
                   'legend': ''}

    def __init__(self, points, **attr):
        """Creates PolyMarker object
        points - sequence (array, tuple or list) of (x,y) points
        **attr - key word attributes
            Defaults:
                'colour'= 'black',          - wx.Pen Colour any wx.NamedColour
                'width'= 1,                 - Pen width
                'size'= 2,                  - Marker size
                'fillcolour'= same as colour,      - wx.Brush Colour any wx.NamedColour
                'fillstyle'= wx.SOLID,      - wx.Brush fill style (use wx.TRANSPARENT for no fill)
                'marker'= 'circle'          - Marker shape
                'legend'= ''                - Marker Legend to display
              
            Marker Shapes:
                - 'circle'
                - 'dot'
                - 'square'
                - 'triangle'
                - 'triangle_down'
                - 'cross'
                - 'plus'
        """
      
        PolyPoints.__init__(self, points, attr)

    def draw(self, dc, printerScale, coord= None):
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale
        size = self.attributes['size'] * printerScale
        fillcolour = self.attributes['fillcolour']
        fillstyle = self.attributes['fillstyle']
        marker = self.attributes['marker']

        dc.SetPen(wx.Pen(wx.NamedColour(colour), width))
        if fillcolour:
            dc.SetBrush(wx.Brush(wx.NamedColour(fillcolour),fillstyle))
        else:
            dc.SetBrush(wx.Brush(wx.NamedColour(colour), fillstyle))
        if coord == None:
            self._drawmarkers(dc, self.scaled, marker, size)
        else:
            self._drawmarkers(dc, coord, marker, size) # draw legend marker

    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        s= 5*self.attributes['size'] * printerScale
        return (s,s)

    def _drawmarkers(self, dc, coords, marker,size=1):
        f = eval('self._' +marker)
        f(dc, coords, size)

    def _circle(self, dc, coords, size=1):
        fact= 2.5*size
        wh= 2.0*size
        rect= _Numeric.zeros((len(coords),4))+[0.0,0.0,wh,wh]
        rect[:,0:2]= coords-[fact,fact]
        dc.DrawEllipseList(rect)

    def _dot(self, dc, coords, size=1):
        dc.DrawPointList(coords)

    def _square(self, dc, coords, size=1):
        fact= 2.5*size
        wh= 5.0*size
        rect= _Numeric.zeros((len(coords),4))+[0.0,0.0,wh,wh]
        rect[:,0:2]= coords-[fact,fact]
        dc.DrawRectangleList(rect.astype(_Numeric.Int32))

    def _triangle(self, dc, coords, size=1):
        shape= [(-2.5*size,1.44*size), (2.5*size,1.44*size), (0.0,-2.88*size)]
        poly= _Numeric.repeat(coords,3)
        poly.shape= (len(coords),3,2)
        poly += shape
        dc.DrawPolygonList(poly.astype(_Numeric.Int32))

    def _triangle_down(self, dc, coords, size=1):
        shape= [(-2.5*size,-1.44*size), (2.5*size,-1.44*size), (0.0,2.88*size)]
        poly= _Numeric.repeat(coords,3)
        poly.shape= (len(coords),3,2)
        poly += shape
        dc.DrawPolygonList(poly.astype(_Numeric.Int32))
      
    def _cross(self, dc, coords, size=1):
        fact= 2.5*size
        for f in [[-fact,-fact,fact,fact],[-fact,fact,fact,-fact]]:
            lines= _Numeric.concatenate((coords,coords),axis=1)+f
            dc.DrawLineList(lines.astype(_Numeric.Int32))

    def _plus(self, dc, coords, size=1):
        fact= 2.5*size
        for f in [[-fact,0,fact,0],[0,-fact,0,fact]]:
            lines= _Numeric.concatenate((coords,coords),axis=1)+f
            #dc.DrawLineList(lines.astype(_Numeric.Int32))
            dc.DrawLineList(lines)

class PlotGraphics:
    """Container to hold PolyXXX objects and graph labels
        - All methods except __init__ are private.
    """

    def __init__(self, objects, title='', xLabel='', yLabel= ''):
        """Creates PlotGraphics object
        objects - list of PolyXXX objects to make graph
        title - title shown at top of graph
        xLabel - label shown on x-axis
        yLabel - label shown on y-axis
        """
        if type(objects) not in [list,tuple]:
            raise TypeError, "objects argument should be list or tuple"
        self.objects = objects
        self.title= title
        self.xLabel= xLabel
        self.yLabel= yLabel

    def boundingBox(self):
        p1, p2 = self.objects[0].boundingBox()
        for o in self.objects[1:]:
            p1o, p2o = o.boundingBox()
            p1 = _Numeric.minimum(p1, p1o)
            p2 = _Numeric.maximum(p2, p2o)
        return p1, p2

    def scaleAndShift(self, scale=(1,1), shift=(0,0)):
        for o in self.objects:
            o.scaleAndShift(scale, shift)

    def setPrinterScale(self, scale):
        """Thickens up lines and markers only for printing"""
        self.printerScale= scale

    def setXLabel(self, xLabel= ''):
        """Set the X axis label on the graph"""
        self.xLabel= xLabel

    def setYLabel(self, yLabel= ''):
        """Set the Y axis label on the graph"""
        self.yLabel= yLabel
        
    def setTitle(self, title= ''):
        """Set the title at the top of graph"""
        self.title= title

    def getXLabel(self):
        """Get x axis label string"""
        return self.xLabel

    def getYLabel(self):
        """Get y axis label string"""
        return self.yLabel

    def getTitle(self, title= ''):
        """Get the title at the top of graph"""
        return self.title

    def draw(self, dc):
        for o in self.objects:
            #t=_time.clock()          # profile info
            o.draw(dc, self.printerScale)
            #dt= _time.clock()-t
            #print o, "time=", dt

    def getSymExtent(self, printerScale):
        """Get max width and height of lines and markers symbols for legend"""
        symExt = self.objects[0].getSymExtent(printerScale)
        for o in self.objects[1:]:
            oSymExt = o.getSymExtent(printerScale)
            symExt = _Numeric.maximum(symExt, oSymExt)
        return symExt
    
    def getLegendNames(self):
        """Returns list of legend names"""
        lst = [None]*len(self)
        for i in range(len(self)):
            lst[i]= self.objects[i].getLegend()
        return lst
            
    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]


#-------------------------------------------------------------------------------
# Main window that you will want to import into your application.

class PlotCanvas(wx.Window):
    """Subclass of a wx.Window to allow simple general plotting
    of data with zoom, labels, and automatic axis scaling."""

    def __init__(self, parent, id = -1, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style= wx.DEFAULT_FRAME_STYLE, name= ""):
        """Constucts a window, which can be a child of a frame, dialog or
        any other non-control window"""
    
        wx.Window.__init__(self, parent, id, pos, size, style, name)
        self.border = (1,1)

        self._DrawEnabled = True
  
        self.SetBackgroundColour("white")
        
        # Create some mouse events for zooming
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDoubleClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)

        # set curser as cross-hairs
        self.SetCursor(wx.CROSS_CURSOR)

        # Things for printing
        #self.print_data = wx.PrintData()
        #self.print_data.SetPaperId(wx.PAPER_LETTER)
        #self.print_data.SetOrientation(wx.LANDSCAPE)
        #self.pageSetupData= wx.PageSetupDialogData()
        #self.pageSetupData.SetMarginBottomRight((25,25))
        #self.pageSetupData.SetMarginTopLeft((25,25))
        #self.pageSetupData.SetPrintData(self.print_data)
        self.printerScale = 1
        self.parent= parent

        # Zooming variables
        self._zoomInFactor =  0.5
        self._zoomOutFactor = 2
        self._zoomCorner1= _Numeric.array([0.0, 0.0]) # left mouse down corner
        self._zoomCorner2= _Numeric.array([0.0, 0.0])   # left mouse up corner
        self._zoomEnabled= False
        self._hasDragged= False
        
        # Drawing Variables
        self.last_draw = None
        self._pointScale= 1
        self._pointShift= 0
        self._xSpec= 'auto'
        self._ySpec= 'auto'
        self._gridEnabled= True
        self._legendEnabled= False
        
        # Fonts
        self._fontCache = {}
        self._fontSizeAxis= 10
        self._fontSizeTitle= 15
        self._fontSizeLegend= 7

        # pointLabels
        self._pointLabelEnabled= False
        self.last_PointLabel= None
        self._pointLabelFunc= None
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        if wx.Platform != "__WXMAC__":
            self.OnSize(None) # sets the initial size based on client size

    def SetFontSizeAxis(self, point= 10):
        """Set the tick and axis label font size (default is 10 point)"""
        self._fontSizeAxis= point
        
    def GetFontSizeAxis(self):
        """Get current tick and axis label font size in points"""
        return self._fontSizeAxis
    
    def SetFontSizeTitle(self, point= 15):
        """Set Title font size (default is 15 point)"""
        self._fontSizeTitle= point

    def GetFontSizeTitle(self):
        """Get current Title font size in points"""
        return self._fontSizeTitle
    
    def SetFontSizeLegend(self, point= 7):
        """Set Legend font size (default is 7 point)"""
        self._fontSizeLegend= point
        
    def GetFontSizeLegend(self):
        """Get current Legend font size in points"""
        return self._fontSizeLegend

    def SetEnableZoom(self, value):
        """Set True to enable zooming."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        self._zoomEnabled= value

    def GetEnableZoom(self):
        """True if zooming enabled."""
        return self._zoomEnabled

    def SetEnableGrid(self, value):
        """Set True to enable grid."""
        if value not in [True,False,'Horizontal','Vertical']:
            raise TypeError, "Value should be True, False, Horizontal or Vertical"
        self._gridEnabled= value
        self.Redraw()

    def GetEnableGrid(self):
        """True if grid enabled."""
        return self._gridEnabled

    def SetEnableLegend(self, value):
        """Set True to enable legend."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        self._legendEnabled= value 
        self.Redraw()

    def GetEnableLegend(self):
        """True if Legend enabled."""
        return self._legendEnabled

    def SetEnablePointLabel(self, value):
        """Set True to enable pointLabel."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        self._pointLabelEnabled= value 
        self.Redraw()  #will erase existing pointLabel if present
        self.last_PointLabel = None

    def GetEnablePointLabel(self):
        """True if pointLabel enabled."""
        return self._pointLabelEnabled

    def SetPointLabelFunc(self, func):
        """Sets the function with custom code for pointLabel drawing
            ******** more info needed ***************
        """
        self._pointLabelFunc= func

    def GetPointLabelFunc(self):
        """Returns pointLabel Drawing Function"""
        return self._pointLabelFunc

    def Reset(self):
        """Unzoom the plot."""
        self.last_PointLabel = None        #reset pointLabel
        if self.last_draw is not None:
            self.Draw(self.last_draw[0])
        
    def ScrollRight(self, units):          
        """Move view right number of axis units."""
        self.last_PointLabel = None        #reset pointLabel
        if self.last_draw is not None:
            graphics, xAxis, yAxis= self.last_draw
            xAxis= (xAxis[0]+units, xAxis[1]+units)
            self.Draw(graphics,xAxis,yAxis)

    def ScrollUp(self, units):
        """Move view up number of axis units."""
        self.last_PointLabel = None        #reset pointLabel
        if self.last_draw is not None: 	
             graphics, xAxis, yAxis= self.last_draw
             yAxis= (yAxis[0]+units, yAxis[1]+units)
             self.Draw(graphics,xAxis,yAxis)

        
    def GetXY(self,event):
        """Takes a mouse event and returns the XY user axis values."""
        x,y= self.PositionScreenToUser(event.GetPosition())
        return x,y

    def PositionUserToScreen(self, pntXY):
        """Converts User position to Screen Coordinates"""
        userPos= _Numeric.array(pntXY)
        x,y= userPos * self._pointScale + self._pointShift
        return x,y
        
    def PositionScreenToUser(self, pntXY):
        """Converts Screen position to User Coordinates"""
        screenPos= _Numeric.array(pntXY)
        x,y= (screenPos-self._pointShift)/self._pointScale
        return x,y
        
    def SetXSpec(self, type= 'auto'):
        """xSpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:
            'none' - shows no axis or tick mark values
            'min' - shows min bounding box values
            'auto' - rounds axis range to sensible values
        """
        self._xSpec= type
        
    def SetYSpec(self, type= 'auto'):
        """ySpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:
            'none' - shows no axis or tick mark values
            'min' - shows min bounding box values
            'auto' - rounds axis range to sensible values
        """
        self._ySpec= type

    def GetXSpec(self):
        """Returns current XSpec for axis"""
        return self._xSpec
    
    def GetYSpec(self):
        """Returns current YSpec for axis"""
        return self._ySpec
    
    def GetXMaxRange(self):
        """Returns (minX, maxX) x-axis range for displayed graph"""
        graphics= self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        xAxis = self._axisInterval(self._xSpec, p1[0], p2[0]) # in user units
        return xAxis

    def GetYMaxRange(self):
        """Returns (minY, maxY) y-axis range for displayed graph"""
        graphics= self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
        return yAxis

    def GetXCurrentRange(self):
        """Returns (minX, maxX) x-axis for currently displayed portion of graph"""
        return self.last_draw[1]
    
    def GetYCurrentRange(self):
        """Returns (minY, maxY) y-axis for currently displayed portion of graph"""
        return self.last_draw[2]
        
    def Draw(self, graphics, xAxis = None, yAxis = None, dc = None):
        """Draw objects in graphics with specified x and y axis.
        graphics- instance of PlotGraphics with list of PolyXXX objects
        xAxis - tuple with (min, max) axis range to view
        yAxis - same as xAxis
        dc - drawing context - doesn't have to be specified.    
        If it's not, the offscreen buffer is used
        """
        if not self._DrawEnabled:
            return
        # check Axis is either tuple or none
        if type(xAxis) not in [type(None),tuple]:
            raise TypeError, "xAxis should be None or (minX,maxX)"
        if type(yAxis) not in [type(None),tuple]:
            raise TypeError, "yAxis should be None or (minY,maxY)"
             
        # check case for axis = (a,b) where a==b caused by improper zooms
        if xAxis != None:
            if xAxis[0] == xAxis[1]:
                return
        if yAxis != None:
            if yAxis[0] == yAxis[1]:
                return
            
        if dc == None:
            # sets new dc and clears it 
            dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
            dc.Clear()
            
        dc.BeginDrawing()
        # dc.Clear()
        
        # set font size for every thing but title and legend
        dc.SetFont(self._getFont(self._fontSizeAxis))

        # sizes axis to axis type, create lower left and upper right corners of plot
        if xAxis == None or yAxis == None:
            # One or both axis not specified in Draw
            p1, p2 = graphics.boundingBox()     # min, max points of graphics
            if xAxis == None:
                xAxis = self._axisInterval(self._xSpec, p1[0], p2[0]) # in user units
            if yAxis == None:
                yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
            # Adjust bounding box for axis spec
            p1[0],p1[1] = xAxis[0], yAxis[0]     # lower left corner user scale (xmin,ymin)
            p2[0],p2[1] = xAxis[1], yAxis[1]     # upper right corner user scale (xmax,ymax)
        else:
            # Both axis specified in Draw
            p1= _Numeric.array([xAxis[0], yAxis[0]])    # lower left corner user scale (xmin,ymin)
            p2= _Numeric.array([xAxis[1], yAxis[1]])     # upper right corner user scale (xmax,ymax)

        self.last_draw = (graphics, xAxis, yAxis)       # saves most recient values

        # Get ticks and textExtents for axis if required
        if self._xSpec is not 'none':        
            xticks = self._ticks(xAxis[0], xAxis[1])
            xTextExtent = dc.GetTextExtent(xticks[-1][1])# w h of x axis text last number on axis
        else:
            xticks = None
            xTextExtent= (0,0) # No text for ticks
        if self._ySpec is not 'none':
            yticks = self._ticks(yAxis[0], yAxis[1])
            yTextExtentBottom= dc.GetTextExtent(yticks[0][1])
            yTextExtentTop   = dc.GetTextExtent(yticks[-1][1])
            yTextExtent= (max(yTextExtentBottom[0],yTextExtentTop[0]),
                        max(yTextExtentBottom[1],yTextExtentTop[1]))
        else:
            yticks = None
            yTextExtent= (0,0) # No text for ticks

        # TextExtents for Title and Axis Labels
        titleWH, xLabelWH, yLabelWH= self._titleLablesWH(dc, graphics)

        # TextExtents for Legend
        legendBoxWH, legendSymExt, legendTextExt = self._legendWH(dc, graphics)

        # room around graph area
        rhsW= max(xTextExtent[0], legendBoxWH[0]) # use larger of number width or legend width
        lhsW= yTextExtent[0]+ yLabelWH[1]
        bottomH= max(xTextExtent[1], yTextExtent[1]/2.)+ xLabelWH[1]
        topH= yTextExtent[1]/2. + titleWH[1]
        textSize_scale= _Numeric.array([rhsW+lhsW,bottomH+topH]) # make plot area smaller by text size
        textSize_shift= _Numeric.array([lhsW, bottomH])          # shift plot area by this amount

        # drawing title and labels text
        dc.SetFont(self._getFont(self._fontSizeTitle))
        titlePos= (self.plotbox_origin[0]+ lhsW + (self.plotbox_size[0]-lhsW-rhsW)/2.- titleWH[0]/2.,
                 self.plotbox_origin[1]- self.plotbox_size[1])
        dc.DrawText(graphics.getTitle(),titlePos[0],titlePos[1])
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabelPos= (self.plotbox_origin[0]+ lhsW + (self.plotbox_size[0]-lhsW-rhsW)/2.- xLabelWH[0]/2.,
                 self.plotbox_origin[1]- xLabelWH[1])
        dc.DrawText(graphics.getXLabel(),xLabelPos[0],xLabelPos[1])
        yLabelPos= (self.plotbox_origin[0],
                 self.plotbox_origin[1]- bottomH- (self.plotbox_size[1]-bottomH-topH)/2.+ yLabelWH[0]/2.)
        if graphics.getYLabel():  # bug fix for Linux
            dc.DrawRotatedText(graphics.getYLabel(),yLabelPos[0],yLabelPos[1],90)

        # drawing legend makers and text
        if self._legendEnabled:
            self._drawLegend(dc,graphics,rhsW,topH,legendBoxWH, legendSymExt, legendTextExt)

        # allow for scaling and shifting plotted points
        scale = (self.plotbox_size-textSize_scale) / (p2-p1)* _Numeric.array((1,-1))
        shift = -p1*scale + self.plotbox_origin + textSize_shift * _Numeric.array((1,-1))
        self._pointScale= scale  # make available for mouse events
        self._pointShift= shift        
        self._drawAxes(dc, p1, p2, scale, shift, xticks, yticks)
        
        graphics.scaleAndShift(scale, shift)
        graphics.setPrinterScale(self.printerScale)  # thicken up lines and markers if printing
        
        # set clipping area so drawing does not occur outside axis box
        ptx,pty,rectWidth,rectHeight= self._point2ClientCoord(p1, p2)
        dc.SetClippingRegion(ptx,pty,rectWidth,rectHeight)
        # Draw the lines and markers
        #start = _time.clock()
        graphics.draw(dc)
        # print "entire graphics drawing took: %f second"%(_time.clock() - start)
        # remove the clipping region
        dc.DestroyClippingRegion()
        dc.EndDrawing()

    def Redraw(self, dc= None):
        """Redraw the existing plot."""
        if self.last_draw is not None:
            graphics, xAxis, yAxis= self.last_draw
            self.Draw(graphics,xAxis,yAxis,dc)

    def Clear(self):
        """Erase the window."""
        self.last_PointLabel = None        #reset pointLabel
        dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
        dc.Clear()
        self.last_draw = None

    def Zoom(self, Center, Ratio):
        """ Zoom on the plot
            Centers on the X,Y coords given in Center
            Zooms by the Ratio = (Xratio, Yratio) given
        """
        self.last_PointLabel = None   #reset maker
        x,y = Center
        if self.last_draw != None:
            (graphics, xAxis, yAxis) = self.last_draw
            w = (xAxis[1] - xAxis[0]) * Ratio[0]
            h = (yAxis[1] - yAxis[0]) * Ratio[1]
            xAxis = ( x - w/2, x + w/2 )
            yAxis = ( y - h/2, y + h/2 )
            self.Draw(graphics, xAxis, yAxis)
        
    def GetClosestPoints(self, pntXY, pointScaled= True):
        """Returns list with
            [curveNumber, legend, index of closest point, pointXY, scaledXY, distance]
            list for each curve.
            Returns [] if no curves are being plotted.
            
            x, y in user coords
            if pointScaled == True based on screen coords
            if pointScaled == False based on user coords
        """
        if self.last_draw == None:
            #no graph available
            return []
        graphics, xAxis, yAxis= self.last_draw
        l = []
        for curveNum,obj in enumerate(graphics):
            #check there are points in the curve
            if len(obj.points) == 0:
                continue  #go to next obj
            #[curveNumber, legend, index of closest point, pointXY, scaledXY, distance]
            cn = [curveNum]+ [obj.getLegend()]+ obj.getClosestPoint( pntXY, pointScaled)
            l.append(cn)
        return l

    def GetClosetPoint(self, pntXY, pointScaled= True):
        """Returns list with
            [curveNumber, legend, index of closest point, pointXY, scaledXY, distance]
            list for only the closest curve.
            Returns [] if no curves are being plotted.
            
            x, y in user coords
            if pointScaled == True based on screen coords
            if pointScaled == False based on user coords
        """
        #closest points on screen based on screen scaling (pointScaled= True)
        #list [curveNumber, index, pointXY, scaledXY, distance] for each curve
        closestPts= self.GetClosestPoints(pntXY, pointScaled)
        if closestPts == []:
            return []  #no graph present
        #find one with least distance
        dists = [c[-1] for c in closestPts]
        mdist = min(dists)  #Min dist
        i = dists.index(mdist)  #index for min dist
        return closestPts[i]  #this is the closest point on closest curve

    def UpdatePointLabel(self, mDataDict):
        """Updates the pointLabel point on screen with data contained in
            mDataDict.

            mDataDict will be passed to your function set by
            SetPointLabelFunc.  It can contain anything you
            want to display on the screen at the scaledXY point
            you specify.

            This function can be called from parent window with onClick,
            onMotion events etc.            
        """
        if self.last_PointLabel != None:
            #compare pointXY
            if mDataDict["pointXY"] != self.last_PointLabel["pointXY"]:
                #closest changed
                self._drawPointLabel(self.last_PointLabel) #erase old
                self._drawPointLabel(mDataDict) #plot new
        else:
            #just plot new with no erase
            self._drawPointLabel(mDataDict) #plot new
        #save for next erase
        self.last_PointLabel = mDataDict

    # event handlers **********************************
    def OnMotion(self, event):
        if self._zoomEnabled and event.LeftIsDown():
            if self._hasDragged:
                self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # remove old
            else:
                self._hasDragged= True
            self._zoomCorner2[0], self._zoomCorner2[1] = self.GetXY(event)
            self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # add new

    def OnMouseLeftDown(self,event):
        self._zoomCorner1[0], self._zoomCorner1[1]= self.GetXY(event)
        self._DrawEnabled = False

    def OnMouseLeftUp(self, event):
        if self._zoomEnabled:
            if self._hasDragged == True:
                self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # remove old
                self._zoomCorner2[0], self._zoomCorner2[1]= self.GetXY(event)
                self._hasDragged = False  # reset flag
                minX, minY= _Numeric.minimum( self._zoomCorner1, self._zoomCorner2)
                maxX, maxY= _Numeric.maximum( self._zoomCorner1, self._zoomCorner2)
                self.last_PointLabel = None        #reset pointLabel
                if self.last_draw != None:
                    self._DrawEnabled = True
                    if self.parent.my_local_plot != None:
                        self.parent.my_local_plot.updateAxes((minX,maxX), (minY,maxY))
                    self.Draw(self.last_draw[0], xAxis = (minX,maxX), yAxis = (minY,maxY), dc = None)
            #else: # A box has not been drawn, zoom in on a point
            ## this interfered with the double click, so I've disables it.
            #    X,Y = self.GetXY(event)
            #    self.Zoom( (X,Y), (self._zoomInFactor,self._zoomInFactor) )
        self._DrawEnabled = True

    def OnMouseDoubleClick(self,event):
        if self._zoomEnabled:
            self.Reset()
        
    def OnMouseRightDown(self,event):
        if self._zoomEnabled:
            X,Y = self.GetXY(event)
            self.Zoom( (X,Y), (self._zoomOutFactor, self._zoomOutFactor) )

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if self.last_PointLabel != None:
            self._drawPointLabel(self.last_PointLabel) #erase old
            self.last_PointLabel = None
        dc = wx.BufferedPaintDC(self, self._Buffer)

    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSize()
        if Size.width <= 0 or Size.height <= 0:
            return
        
        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(Size[0],Size[1])
        self._setSize()

        self.last_PointLabel = None        #reset pointLabel

        if self.last_draw is None:
            self.Clear()
        else:
            graphics, xSpec, ySpec = self.last_draw
            self.Draw(graphics,xSpec,ySpec)

    def OnLeave(self, event):
        """Used to erase pointLabel when mouse outside window"""
        if self.last_PointLabel != None:
            self._drawPointLabel(self.last_PointLabel) #erase old
            self.last_PointLabel = None

        
    # Private Methods **************************************************
    def _setSize(self, width=None, height=None):
        """DC width and height."""
        if width == None:
            (self.width,self.height) = self.GetClientSize()
        else:
            self.width, self.height= width,height    
        self.plotbox_size = 0.97*_Numeric.array([self.width, self.height])
        xo = 0.5*(self.width-self.plotbox_size[0])
        yo = self.height-0.5*(self.height-self.plotbox_size[1])
        self.plotbox_origin = _Numeric.array([xo, yo])
    
    def _setPrinterScale(self, scale):
        """Used to thicken lines and increase marker size for print out."""
        # line thickness on printer is very thin at 600 dot/in. Markers small
        self.printerScale= scale
     
    def _printDraw(self, printDC):
        """Used for printing."""
        if self.last_draw != None:
            graphics, xSpec, ySpec= self.last_draw
            self.Draw(graphics,xSpec,ySpec,printDC)

    def _drawPointLabel(self, mDataDict):
        """Draws and erases pointLabels"""
        width = self._Buffer.GetWidth()
        height = self._Buffer.GetHeight()
        tmp_Buffer = wx.EmptyBitmap(width,height)
        dcs = wx.MemoryDC()
        dcs.SelectObject(tmp_Buffer)
        dcs.Clear()
        dcs.BeginDrawing()
        self._pointLabelFunc(dcs,mDataDict)  #custom user pointLabel function
        dcs.EndDrawing()

        dc = wx.ClientDC( self )
        #this will erase if called twice
        dc.Blit(0, 0, width, height, dcs, 0, 0, wx.EQUIV)  #(NOT src) XOR dst
        

    def _drawLegend(self,dc,graphics,rhsW,topH,legendBoxWH, legendSymExt, legendTextExt):
        """Draws legend symbols and text"""
        # top right hand corner of graph box is ref corner
        trhc= self.plotbox_origin+ (self.plotbox_size-[rhsW,topH])*[1,-1]
        legendLHS= .091* legendBoxWH[0]  # border space between legend sym and graph box
        lineHeight= max(legendSymExt[1], legendTextExt[1]) * 1.1 #1.1 used as space between lines
        dc.SetFont(self._getFont(self._fontSizeLegend))
        for i in range(len(graphics)):
            o = graphics[i]
            s= i*lineHeight
            if isinstance(o,PolyMarker):
                # draw marker with legend
                pnt= (trhc[0]+legendLHS+legendSymExt[0]/2., trhc[1]+s+lineHeight/2.)
                o.draw(dc, self.printerScale, coord= _Numeric.array([pnt]))
            elif isinstance(o,PolyLine):
                # draw line with legend
                pnt1= (trhc[0]+legendLHS, trhc[1]+s+lineHeight/2.)
                pnt2= (trhc[0]+legendLHS+legendSymExt[0], trhc[1]+s+lineHeight/2.)
                o.draw(dc, self.printerScale, coord= _Numeric.array([pnt1,pnt2]))
            else:
                raise TypeError, "object is neither PolyMarker or PolyLine instance"
            # draw legend txt
            pnt= (trhc[0]+legendLHS+legendSymExt[0], trhc[1]+s+lineHeight/2.-legendTextExt[1]/2)
            dc.DrawText(o.getLegend(),pnt[0],pnt[1])
        dc.SetFont(self._getFont(self._fontSizeAxis)) # reset

    def _titleLablesWH(self, dc, graphics):
        """Draws Title and labels and returns width and height for each"""
        # TextExtents for Title and Axis Labels
        dc.SetFont(self._getFont(self._fontSizeTitle))
        title= graphics.getTitle()
        titleWH= dc.GetTextExtent(title)
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabel, yLabel= graphics.getXLabel(),graphics.getYLabel()
        xLabelWH= dc.GetTextExtent(xLabel)
        yLabelWH= dc.GetTextExtent(yLabel)
        return titleWH, xLabelWH, yLabelWH
    
    def _legendWH(self, dc, graphics):
        """Returns the size in screen units for legend box"""
        if self._legendEnabled != True:
            legendBoxWH= symExt= txtExt= (0,0)
        else:
            # find max symbol size
            symExt= graphics.getSymExtent(self.printerScale)
            # find max legend text extent
            dc.SetFont(self._getFont(self._fontSizeLegend))
            txtList= graphics.getLegendNames()
            txtExt= dc.GetTextExtent(txtList[0])
            for txt in graphics.getLegendNames()[1:]:
                txtExt= _Numeric.maximum(txtExt,dc.GetTextExtent(txt))
            maxW= symExt[0]+txtExt[0]    
            maxH= max(symExt[1],txtExt[1])
            # padding .1 for lhs of legend box and space between lines
            maxW= maxW* 1.1
            maxH= maxH* 1.1 * len(txtList)
            dc.SetFont(self._getFont(self._fontSizeAxis))
            legendBoxWH= (maxW,maxH)
        return (legendBoxWH, symExt, txtExt)

    def _drawRubberBand(self, corner1, corner2, flag=True):
        """Draws/erases rect box from corner1 to corner2"""
        ptx,pty,rectWidth,rectHeight= self._point2ClientCoord(corner1, corner2)
        # draw rectangle
        dc = wx.ClientDC( self )
        dc.BeginDrawing()                 
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush( wx.WHITE, wx.TRANSPARENT ) )
        if flag:
            dc.SetLogicalFunction(wx.INVERT)
        else:
            dc.SetLogicalFunction(wx.COPY)
            
        dc.DrawRectangle( ptx,pty, rectWidth,rectHeight)
        dc.SetLogicalFunction(wx.COPY)
        dc.EndDrawing()

    def _getFont(self,size):
        """Take font size, adjusts if printing and returns wx.Font"""
        s = size*self.printerScale
        of = self.GetFont()
        # Linux speed up to get font from cache rather than X font server
        key = (int(s), of.GetFamily (), of.GetStyle (), of.GetWeight ())
        font = self._fontCache.get (key, None)
        if font:
            return font                 # yeah! cache hit
        else:
            font =  wx.Font(int(s), of.GetFamily(), of.GetStyle(), of.GetWeight())
            self._fontCache[key] = font
            return font


    def _point2ClientCoord(self, corner1, corner2):
        """Converts user point coords to client screen int coords x,y,width,height"""
        c1= _Numeric.array(corner1)
        c2= _Numeric.array(corner2)
        # convert to screen coords
        pt1= c1*self._pointScale+self._pointShift
        pt2= c2*self._pointScale+self._pointShift
        # make height and width positive
        pul= _Numeric.minimum(pt1,pt2) # Upper left corner
        plr= _Numeric.maximum(pt1,pt2) # Lower right corner
        rectWidth, rectHeight= plr-pul
        ptx,pty= pul
        return ptx, pty, rectWidth, rectHeight 
    
    def _axisInterval(self, spec, lower, upper):
        """Returns sensible axis range for given spec"""
        if spec == 'none' or spec == 'min':
            if lower == upper:
                return lower-0.5, upper+0.5
            else:
                return lower, upper
        elif spec == 'auto':
            range = upper-lower
            if range == 0.:
                return lower-0.5, upper+0.5
            log = _Numeric.log10(range)
            power = _Numeric.floor(log)
            fraction = log-power
            if fraction <= 0.05:
                power = power-1
            grid = 10.**power
            lower = lower - lower % grid
            mod = upper % grid
            if mod != 0:
                upper = upper - mod + grid
            return lower, upper
        elif type(spec) == type(()):
            lower, upper = spec
            if lower <= upper:
                return lower, upper
            else:
                return upper, lower
        else:
            raise ValueError, str(spec) + ': illegal axis specification'

    def _drawAxes(self, dc, p1, p2, scale, shift, xticks, yticks):
        
        penWidth= self.printerScale        # increases thickness for printing only
        dc.SetPen(wx.Pen(wx.NamedColour('BLACK'), penWidth))
        
        # set length of tick marks--long ones make grid
        if self._gridEnabled:
            x,y,width,height= self._point2ClientCoord(p1,p2)
            if self._gridEnabled == 'Horizontal':
                yTickLength= width/2.0 +1
                xTickLength= 3 * self.printerScale
            elif self._gridEnabled == 'Vertical':
                yTickLength= 3 * self.printerScale
                xTickLength= height/2.0 +1
            else:
                yTickLength= width/2.0 +1
                xTickLength= height/2.0 +1
        else:
            yTickLength= 3 * self.printerScale  # lengthens lines for printing
            xTickLength= 3 * self.printerScale
        
        if self._xSpec is not 'none':
            lower, upper = p1[0],p2[0]
            text = 1
            for y, d in [(p1[1], -xTickLength), (p2[1], xTickLength)]:   # miny, maxy and tick lengths
                a1 = scale*_Numeric.array([lower, y])+shift
                a2 = scale*_Numeric.array([upper, y])+shift
                dc.DrawLine(a1[0],a1[1],a2[0],a2[1])  # draws upper and lower axis line
                for x, label in xticks:
                    pt = scale*_Numeric.array([x, y])+shift
                    dc.DrawLine(pt[0],pt[1],pt[0],pt[1] + d) # draws tick mark d units
                    if text:
                        dc.DrawText(label,pt[0],pt[1])
                text = 0  # axis values not drawn on top side

        if self._ySpec is not 'none':
            lower, upper = p1[1],p2[1]
            text = 1
            h = dc.GetCharHeight()
            for x, d in [(p1[0], -yTickLength), (p2[0], yTickLength)]:
                a1 = scale*_Numeric.array([x, lower])+shift
                a2 = scale*_Numeric.array([x, upper])+shift
                dc.DrawLine(a1[0],a1[1],a2[0],a2[1])
                for y, label in yticks:
                    pt = scale*_Numeric.array([x, y])+shift
                    dc.DrawLine(pt[0],pt[1],pt[0]-d,pt[1])
                    if text:
                        dc.DrawText(label,pt[0]-dc.GetTextExtent(label)[0],
                                    pt[1]-0.5*h)
                text = 0    # axis values not drawn on right side

    def _ticks(self, lower, upper):
        ideal = (upper-lower)/7.
        log = _Numeric.log10(ideal)
        power = _Numeric.floor(log)
        fraction = log-power
        factor = 1.
        error = fraction
        for f, lf in self._multiples:
            e = _Numeric.fabs(fraction-lf)
            if e < error:
                error = e
                factor = f
        grid = factor * 10.**power
        if power > 4 or power < -4:
            format = '%+7.1e'        
        elif power >= 0:
            digits = max(1, int(power))
            format = '%' + `digits`+'.0f'
        else:
            digits = -int(power)
            format = '%'+`digits+2`+'.'+`digits`+'f'
        ticks = []
        t = -grid*_Numeric.floor(-lower/grid)
        while t <= upper:
            ticks.append( (t, format % (t,)) )
            t = t + grid
        return ticks

    _multiples = [(2., _Numeric.log10(2.)), (5., _Numeric.log10(5.))]

class TestFrame(wx.Frame):
    def __init__(self, parent, id, title, namespace, interface, component_name, port_name):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, (600, 400))

        self.parent = parent
        self.namespace = namespace
        self.interface = interface
        self.my_local_plot = None
        self.component_name = component_name
        self.port_name = port_name
        self.setup_graphics()
        
        # Now Create the menu bar and items
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(205, 'E&xit', 'Enough of this already!')
        self.Bind(wx.EVT_MENU, self.OnFileExit, id=205)
        self.mainmenu.Append(menu, '&File')
        
        menu = wx.Menu()
        menu.Append(206, 'I/Q', 'Make a scatter plot of the I/Q data')
        self.Bind(wx.EVT_MENU,self.OnIQDraw, id=206)
        menu.Append(207, 'Spectrum', 'Plot and FFT of the signal')
        self.Bind(wx.EVT_MENU,self.OnSpectrumDraw, id=207)
        self.mainmenu.Append(menu, "&Plotting")

        menu = wx.Menu()
        menu.Append(300, '&About', 'About this thing...')
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=300)
        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

        # A status bar to tell people what's happening
        self.CreateStatusBar(1)
        
        self.client = PlotCanvas(self)
        #define the function for drawing pointLabels
        self.client.SetPointLabelFunc(self.DrawPointLabel)
        # Create mouse event for showing cursor coords in status bar
        self.client.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        # Show closest point when enabled
        self.client.Bind(wx.EVT_MOTION, self.OnMotion)
        
        # Initialize the plot to display the spectrum
        self.DrawMode = 2
        self.client.SetXSpec('min')
        self.client.SetYSpec('min')
        self.client.SetEnableZoom(True)

        # Bind the close event so we can disconnect the ports
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Show(True)

    def DrawPointLabel(self, dc, mDataDict):
        """This is the fuction that defines how the pointLabels are plotted
            dc - DC that will be passed
            mDataDict - Dictionary of data that you want to use for the pointLabel

            As an example I have decided I want a box at the curve point
            with some text information about the curve plotted below.
            Any wxDC method can be used.
        """
        # ----------
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush( wx.BLACK, wx.SOLID ) )
        
        sx, sy = mDataDict["scaledXY"] #scaled x,y of closest point
        dc.DrawRectangle( sx-5,sy-5, 10, 10)  #10by10 square centered on point
        px,py = mDataDict["pointXY"]
        cNum = mDataDict["curveNum"]
        pntIn = mDataDict["pIndex"]
        legend = mDataDict["legend"]
        #make a string to display
        s = "Crv# %i, '%s', Pt. (%.2f,%.2f), PtInd %i" %(cNum, legend, px, py, pntIn)
        dc.DrawText(s, sx , sy+1)
        # -----------

    def OnMouseLeftDown(self,event):
        s= "Left Mouse Down at Point: (%.4f, %.4f)" % self.client.GetXY(event)
        self.SetStatusText(s)
        event.Skip()            #allows plotCanvas OnMouseLeftDown to be called

    def OnMotion(self, event):
        #show closest point (when enbled)
        if self.client.GetEnablePointLabel() == True:
            #make up dict with info for the pointLabel
            #I've decided to mark the closest point on the closest curve
            dlst= self.client.GetClosetPoint( self.client.GetXY(event), pointScaled= True)
            if dlst != []:    #returns [] if none
                curveNum, legend, pIndex, pointXY, scaledXY, distance = dlst
                #make up dictionary to pass to my user function (see DrawPointLabel) 
                mDataDict= {"curveNum":curveNum, "legend":legend, "pIndex":pIndex,\
                            "pointXY":pointXY, "scaledXY":scaledXY}
                #pass dict to update the pointLabel
                self.client.UpdatePointLabel(mDataDict)
        event.Skip()           #go to next handler

    def OnFileExit(self, event):
        self.Close()

    def OnIQDraw(self, event):
        self.DrawMode = 1
        self.my_local_plot.first_draw = True
        self.my_local_plot.update_draw = False
    
    def OnSpectrumDraw(self, event):
        self.DrawMode = 2
        self.my_local_plot.first_draw = True
        self.client.SetXSpec('min')
        self.client.SetYSpec('min')

    def OnPlotRedraw(self,event):
        self.client.Redraw()

    def OnPlotClear(self,event):
        self.client.Clear()
        
    def OnPlotScale(self, event):
        if self.client.last_draw != None:
            graphics, xAxis, yAxis= self.client.last_draw
            self.client.Draw(graphics,(1,3.05),(0,1))

    def OnEnableZoom(self, event):
        self.client.SetEnableZoom(event.IsChecked())
        
    def OnEnableGrid(self, event):
        self.client.SetEnableGrid(event.IsChecked())
        
    def OnEnableLegend(self, event):
        self.client.SetEnableLegend(event.IsChecked())

    def OnEnablePointLabel(self, event):
        self.client.SetEnablePointLabel(event.IsChecked())

    def OnScrUp(self, event):
        self.client.ScrollUp(1)
        
    def OnScrRt(self,event):
        self.client.ScrollRight(2)

    def OnReset(self,event):
        self.client.Reset()

    def OnHelpAbout(self, event):
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, "This is a simple plotting widget", "About...")
        about.ShowModal()

    def resetDefaults(self):
        """Just to reset the fonts back to the PlotCanvas defaults"""
        self.client.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL))
        self.client.SetFontSizeAxis(10)
        self.client.SetFontSizeLegend(7)
        self.client.SetXSpec('auto')
        self.client.SetYSpec('auto')
    
    def setup_graphics(self):
        self.CORBA_being_used = False

        if True:		
         self.CORBA_being_used = True
         self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
         obj = self.orb.resolve_initial_references("NameService")
         rootContext = obj._narrow(CosNaming.NamingContext)
         if rootContext is None:
             print "Failed to narrow the root naming context"
             sys.exit(1)
         name = [CosNaming.NameComponent(self.component_name[0],""),
             CosNaming.NameComponent(self.component_name[1],""),
             CosNaming.NameComponent(self.component_name[2],"")]
     
         try:
             ResourceRef = rootContext.resolve(name)
     
         except:
             print "Required resource not found"
             sys.exit(1)
     
         ResourceHandle = ResourceRef._narrow(CF.Resource)
         PortReference = ResourceHandle.getPort(self.port_name)
         if PortReference is None:
             print "Failed to get Port reference"
         self.PortHandle = PortReference._narrow(CF.Port)
         
         self.my_local_plot = None
         
         if self.interface == "complexFloat":
             self.my_local_plot = my_graph_structure_complexFloat(self.orb, self)
         elif self.interface == "complexShort":
             self.my_local_plot = my_graph_structure_complexShort(self.orb, self)
         elif self.interface == "realChar":
             self.my_local_plot = my_graph_structure_realChar(self.orb, self)

         obj_poa = self.orb.resolve_initial_references("RootPOA")
         poaManager = obj_poa._get_the_POAManager()
         poaManager.activate()
         obj_poa.activate_object(self.my_local_plot)
         self.PortHandle.connectPort(self.my_local_plot._this(), "thisismyconnectionid_plot")
         #orb.run()
    
    def updateWaveformData(self, data):
        if data.has_key('center_freq'):
            self.my_local_plot.center_freq = data['center_freq']
        if data.has_key('sample_rate'):
            self.my_local_plot.sample_rate = data['sample_rate']
        if data.has_key('decimation'):
            self.my_local_plot.decimation = data['decimation']

        self.my_local_plot.updateSpectrumPlotData()

    def OnCloseWindow(self,event):
        if hasattr(self.parent, 'removeToolFrame'):
            self.parent.removeToolFrame(self)
        self = None
        event.Skip()

    def __del__(self):
        if self.CORBA_being_used:
            self.PortHandle.disconnectPort("thisismyconnectionid_plot")
            while (_time.time() - self.my_local_plot.end_time) < 1.5:
                #print (time.time() - self.my_local_plot.end_time)
                pass
                #_time.sleep(1)

class my_graph_structure:
    '''
    Base class for plotting
    '''
    def __init__(self, orb, gui):
        #print "Initializing consumer..."
        self.orb = orb
        self.gui = gui
        self.end_time = time.time()
        self.begin_time = time.time()
        self.first_draw = True
        self.center_freq = 0.0
        self.sample_rate = 0.0
        self.decimation = 20
        self.packet_counter = 0
        self.last_plot_time = 0
        self.plot_interval = 1 # interval at which plot is refreshed (seconds)
        self.bandwidth = 0.0
        self.yAxis = (3000,10000)
        self.xAxis = None
        self.minX=100000
        self.maxX=-100000
        self.minY=100000
        self.maxY=-100000
        self.minX_old=0
        self.maxX_old=0
        self.minY_old=0
        self.maxY_old=0
        self.dataHasChanged = False
        self.fftOrder = 512
        self.i_array = _Numeric.array(range(self.fftOrder),copy=False)
        self.q_array = _Numeric.array(range(self.fftOrder),copy=False)
        self.c_array = _Numeric.array(range(self.fftOrder),copy=False)
        self.initialArray = _Numeric.arange(-self.fftOrder/2, self.fftOrder/2, step=0.5)
        self.plottingPeriodogram = False #True #False


    def updateOnMetaData(self, metadata):
        self.center_freq = metadata.carrier_frequency
        self.sample_rate = metadata.sampling_frequency
        if self.gui.DrawMode == 2:
            self.updateSpectrumPlotData()

    def pushPacketMetaData(self, I_data, Q_data, metadata):
        self.updateOnMetaData(metadata)
        self.pushPacket(I_data, Q_data)

 #   def pushPacket(self, I_data, Q_data):
 #       if self.packet_counter == 0:
 #           self.plotData(I_data, Q_data)
 #       if self.packet_counter < (self.decimation -1):
 #           self.packet_counter = self.packet_counter + 1
 #       else:
 #           self.packet_counter = 0

    def pushPacket(self, I_data, Q_data):
        pushPacket_start_time = _time.time()
        if (pushPacket_start_time - self.last_plot_time)  > self.plot_interval:
            self.plotData(I_data, Q_data)
            self.last_plot_time = pushPacket_start_time
            self.plot_interval = 3 * (time.time() - pushPacket_start_time)

    def plotData(self, I_data, Q_data):
        locker = wx.MutexGuiLocker()

        graph_legend = ''
        x_axis_label = ''
        y_axis_label = ''
        if self.gui.DrawMode == 1:
            self.data1 = _Numeric.arange(len(I_data)*2)
            self.data1.shape = (len(I_data), 2)
            self.data1[:,0] = I_data
            self.data1[:,1] = Q_data
            graph_legend = 'I/Q Data'
            x_axis_label = 'I'
            y_axis_label = 'Q'
            # set plot to scatter, not line
            markers1 = PolyMarker(self.data1, legend=graph_legend, colour='purple')
            if not self.first_draw:
                minX = _Numeric.minimum.reduce(self.data1[:,0])
                maxX = _Numeric.maximum.reduce(self.data1[:,0])
                minY = _Numeric.minimum.reduce(self.data1[:,1])
                maxY = _Numeric.maximum.reduce(self.data1[:,1])
                if (minX < self.minX) or (maxX > self.maxX) or (minY < self.minY) or (maxY > self.maxY):
                    self.first_draw = True
                    self.update_draw = True
        elif self.gui.DrawMode == 2:

            # the input array should not be shorter than the FFT
            if len(I_data) < self.fftOrder:
                # zero-pad data to fit length
                for tmp_index in range(self.fftOrder-len(I_data)):
                    I_data.append(0)
                    Q_data.append(0)
            self.i_array[:] = I_data[0:self.fftOrder]
            self.q_array[:] = Q_data[0:self.fftOrder]
            self.c_array = self.i_array + self.q_array*1j

            spectrum = _Numeric.fft.fft(self.c_array, n=self.fftOrder)
            spectrum = _Numeric.fft.helper.fftshift(spectrum)
            self.data1 = self.initialArray.copy()
            self.data1=self.data1/(self.fftOrder/2)
            self.data1.shape = (len(spectrum), 2)

            if self.plottingPeriodogram:
                my_sp = 10 * _Numeric.log10(pow(abs(spectrum),2) + 0.00001)
            else:
                my_sp = 20 * _Numeric.log10(abs(spectrum) + 0.00001)
            #my_sp =  my_sp * 1000
            self.data1[:,1] = my_sp.astype('i4')
            if self.plottingPeriodogram:
                graph_legend = 'Periodogram'
                y_axis_label = '|FFT|^2 (dB)'
            else:
                graph_legend = 'Spectral Data'
                y_axis_label = 'Magnitude (dB)'
            x_axis_label = 'Normalized Frequency'
            self.yAxis = (-50,150)
            self.xAxis = None
            markers1 = PolyLine(self.data1, legend=graph_legend, colour='red')
    
        if self.first_draw:
            if self.gui.DrawMode == 1:
                minX = _Numeric.minimum.reduce(self.data1[:,0])
                maxX = _Numeric.maximum.reduce(self.data1[:,0])
                minY = _Numeric.minimum.reduce(self.data1[:,1])
                maxY = _Numeric.maximum.reduce(self.data1[:,1])
                multiply_factor = 1.5
                if self.update_draw:
                    if self.minX > minX:
                        if (self.minX_old > minX and self.minX > (minX * multiply_factor)):
                            if self.minX_old > minX:
                                self.minX = self.minX_old
                            else:
                                self.minX = minX
                        self.minX_old = minX
                    if self.maxX < maxX:
                        if (self.maxX_old < maxX and self.maxX < (maxX * multiply_factor)):
                            if self.maxX_old < maxX:
                                self.maxX = self.maxX_old
                            else:
                                self.maxX = maxX
                        self.maxX_old = maxX
                    if self.minY > minY:
                        if (self.minY_old > minY and self.minY > (minY * multiply_factor)):
                            if self.minY_old > minY:
                               self.minY = self.minY_old
                            else:
                               self.minY = minY
                        self.minY_old = minY
                    if self.maxY < maxY:
                        if (self.maxY_old < maxY and self.maxY < (maxY * multiply_factor)):
                            if self.maxY_old < maxY:
                                self.maxY = self.maxY_old
                            else:
                                self.maxY = maxY
                        self.maxY_old = maxY
                    self.update_draw = False
                else:
                    if self.minX > minX:
                        self.minX = minX
                    if self.maxX < maxX:
                        self.maxX = maxX
                    if self.minY > minY:
                        self.minY = minY
                    if self.maxY < maxY:
                        self.maxY = maxY
                self.updateAxes((self.minX,self.maxX), (self.minY,self.maxY))
            self.gui.client.Draw(PlotGraphics([markers1],self.gui.component_name[2], x_axis_label, y_axis_label),yAxis=self.yAxis, xAxis=self.xAxis)
            self.first_draw = False
        else:
            if self.gui.DrawMode == 1:
                self.gui.client.Draw(PlotGraphics([markers1],self.gui.component_name[2], x_axis_label, y_axis_label),yAxis=self.gui.client.last_draw[2],xAxis=self.xAxis)
            else:
                self.gui.client.Draw(PlotGraphics([markers1],self.gui.component_name[2], x_axis_label, y_axis_label),yAxis=self.gui.client.last_draw[2])
            pass
            
        self.end_time = _time.time()

    def updateSpectrumPlotData(self):
        self.bandwidth = self.sample_rate
        self.xAxis = (self.center_freq - self.bandwidth/2.0, self.center_freq + self.bandwidth/2.0)
        # next line sometimes throws divide by zero exception
        #self.initialArray = (_Numeric.arange(self.xAxis[0],self.xAxis[1],step=self.bandwidth/(self.fftOrder*2.0)))/1000000

    def updateAxes(self, x_axis, y_axis):
        self.xAxis = x_axis
        self.yAxis = y_axis

class my_graph_structure_complexFloat(my_graph_structure, standardInterfaces__POA.complexFloat):
    '''Derived class for plotting complexFloat data'''

class my_graph_structure_complexShort(my_graph_structure, standardInterfaces__POA.complexShort):
    '''Derived class for plotting complexShort data'''

class my_graph_structure_realChar(my_graph_structure, standardInterfaces__POA.realChar):
    '''Derived class for plotting realChar data'''

def create(parent,namespace, interface, ns_name, port_name):
    return TestFrame(parent, -1, "PlotCanvas", namespace, interface, ns_name, port_name)

def __test(argv):

    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = create(None, argv[1], argv[2], [argv[3], argv[4], argv[5]], argv[6])
            self.SetTopWindow(frame)
            return True


    app = MyApp(0)
    app.MainLoop()

if __name__ == '__main__':
    if not (len(sys.argv)==7):
        print "usage: plot.py <interface_namespace> <type> <Domain_name> <Waveform_name> <Component_name> <port_name>"
        sys.exit(1)
    __test(sys.argv)
