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

import os, sys
import xml.dom.minidom
from xml.dom.minidom import Node
import ComponentClass as CC
from errorMsg import *

availableTypes = ["boolean", "char", "double", "float", "short", "long",
                    "objref", "octet", "string", "ulong","ushort"]
availableKinds = ["allocation", "configure", "test", "execparam", "factoryparam"]
availableActions = ["eq", "ne", "gt", "lt", "ge", "le", "external"]
availableModes = ["readonly", "readwrite", "writeonly"]

def getResource(path,Rname,parent):
    
    scdPath = findFile(path,Rname,".scd.xml")                
    if scdPath == None:         
        errorMsg(parent,"No scd file found for: " + Rname)
        return
    
    spdPath = findFile(path,Rname,".spd.xml")
    prfPath = findFile(path,Rname,".prf.xml")
    
    #
    # Build the main component or device from the SCD file    
    #
    doc_scd = xml.dom.minidom.parse(scdPath)
    try:
        componenttypeNode = doc_scd.getElementsByTagName("componenttype")
        componenttype = componenttypeNode[0].childNodes[0].data
    except:
        errorMsg(parent,"Invalid file: " + scdPath)
        return None
    
    doc_spd = xml.dom.minidom.parse(spdPath)

    # get resource description
    # note: this is not the same as the implementation description
    softpkgNode = doc_spd.getElementsByTagName("softpkg")[0]
    Rdescription = ''
    for n in softpkgNode.childNodes:
        if n.nodeName == "description":
            resDescriptionNode = doc_spd.getElementsByTagName("description")
            try:
                Rdescription = resDescriptionNode[0].firstChild.data
            except:
                pass
            break

    #Instantiate a new component of the appropriate type
    if componenttype == u'resource':
        newComp = CC.Component(name=Rname,type='resource',description=Rdescription)
    elif componenttype == u'executabledevice':
        newComp = CC.Component(name=Rname,type='executabledevice',description=Rdescription)
    elif componenttype == u'loadabledevice':
        newComp = CC.Component(name=Rname,type='loadabledevice',description=Rdescription)
    elif componenttype == u'device':
        newComp = CC.Component(name=Rname,type='device',description=Rdescription)
    else:
        errorMsg(parent,"Can't identify resource type for: " + Rname)
        return None
        
    # Get the Ports
    portsNodes = doc_scd.getElementsByTagName("ports")
    for node in portsNodes:
        providesPortsNodes = node.getElementsByTagName("provides")
        usesPortsNodes = node.getElementsByTagName("uses")

    # Provides ports
    for node in providesPortsNodes:
        tmpName = node.getAttribute("providesname")
        tmpInt = getInterface( node.getAttribute("repid"), tmpName )
        if tmpInt == None:
            return None
        portTypeNodeList = node.getElementsByTagName("porttype")
        tmpType = portTypeNodeList[0].getAttribute("type")
        newPort = CC.Port(tmpName,tmpInt,type='Provides',portType=tmpType)
        newComp.ports.append(newPort)

    # Uses ports
    for node in usesPortsNodes:
        tmpName = node.getAttribute("usesname")
        tmpInt = getInterface( node.getAttribute("repid"), tmpName )
        if tmpInt == None:
            return None
        portTypeNodeList = node.getElementsByTagName("porttype")
        tmpType = portTypeNodeList[0].getAttribute("type")
        newPort = CC.Port(tmpName,tmpInt,type='Uses',portType=tmpType)
        newComp.ports.append(newPort)

    # Make sure that xml and code are not generated for this resource
    newComp.generate = False        
    
    # Store the name of the file without the suffix (.scd.xml)
    i = scdPath.rfind("/")
    if i != -1:
        newComp.xmlName = scdPath[i+1:-8]
    else:
        newComp.xmlName = scdPath[:-8]
    
    #
    # Import the properties from the PRF file
    #
    # If there are no properties, just return the component as is
    if prfPath == None:
        return newComp
    doc_prf = xml.dom.minidom.parse(prfPath)
    try:
        propertyNodeList = doc_prf.getElementsByTagName("properties")
    except:
        errorMsg(parent,"Invalid file: " + prfPath)
        return None
    
    # get simple properties
    simplePropertyNodeList = doc_prf.getElementsByTagName("simple")
    for node in simplePropertyNodeList:
        p = getSimpleProperty(node)
        if p == None:
            print "There was an error parsing simple properties in the PRF file " + prfPath
            continue
        newComp.properties.append(p)

    # get simple sequence properties
    simpleSequencePropertyNodeList = doc_prf.getElementsByTagName("simplesequence")
    for node in simpleSequencePropertyNodeList:
        p = getSimpleSequenceProperty(node, prfPath)
        if p == None:
            print "There was an error parsing simple sequence properties in the PRF file " + prfPath
            continue
        newComp.properties.append(p)

    return newComp

def getInterface(repid,name):
    try:
        repid = repid.strip('IDL:')
        repid = repid[:repid.rfind(':')]
        tmpNS = repid[:repid.find('/')]
        tmpName = repid[repid.find('/')+1:]
        newInt = CC.Interface(tmpName,nameSpace=tmpNS)
        return newInt
        
    except:
        errorMsg(parent,"Can't read the Interface information for port: " + name)
        return None
    
    
def findFile(path,Rname,suf):
    tmpf = None
    if os.path.isfile(path + '/' + Rname +'Resource'+suf):
        tmpf = path + '/' + Rname +'Resource' + suf
    elif os.path.isfile(path + '/' + Rname + suf):
        tmpf = path + '/' + Rname + suf     
    else:
        tmpFiles = os.listdir(path)
        for f in tmpFiles:
            if len(f)>=8 and f[-8:] == suf:
                tmpf = path + '/' + f
                break
    return tmpf

def stripDoctype(xmlfile):
    """Strips out the DOCTYPE checking because the dtd files are positioned 
       in a relative location to the SCA (OSSIE) filesystem, so when Amara
       trys to validate against them, it bails out looking for the file.
       Returns a string representation of the xml file without the DOCTYPE line."""
   
    file = open(xmlfile, 'r')
    xml = ''
    line = file.readline()
    while len(line) > 0:
        if "DOCTYPE" in line:
            break
        xml += line
        line = file.readline()
    xml += file.read()

    return xml
                                                                    

def getSimpleProperty(n):
    tmpName = n.getAttribute("name")
    tmpID   = n.getAttribute("id")
    tmpType = n.getAttribute("type")
    tmpMode = n.getAttribute("mode")
    tmpDes = n.getAttribute("description")

    if tmpName == "" or tmpID == "" or tmpType == "" or tmpMode == "":
        return None
    if tmpMode not in availableModes:
        return None
    if tmpType not in availableTypes:
        return None
    
    newProp = CC.SimpleProperty(tmpName,tmpMode,tmpType,description=tmpDes)
   
    # Set ID
    #UUID in the sad file will need to match the UUID in the prf (tmpID is from prf)
    newProp.id = tmpID

    # Get/set property value
    valueNodeList = n.getElementsByTagName("value")
    value = valueNodeList[0].childNodes[0].data
    newProp.value = newProp.defaultValue = str(value)
    del valueNodeList, value
    
    # Get/set property units
    unitsNodeList = n.getElementsByTagName("units")
    if len(unitsNodeList) > 0:
        units = unitsNodeList[0].childNodes[0].data
        newProp.units = str(s.units)
    #del unitsNodeList, units
    
    # TODO: Get/set min/max values
    # TODO: Get/set enum
    
    # Get/set kind
    kindNodeList = n.getElementsByTagName("kind")
    kindtype = kindNodeList[0].getAttribute("kindtype")
    if kindtype == "":
        return None
    newProp.kind = str(kindtype)
    del kindNodeList, kindtype
    
    # Get/set action
    actionNodeList = n.getElementsByTagName("action")
    if len(actionNodeList) > 0:
        actiontype = actionNodeList[0].getAttribute("type")
        newProp.action = str(actiontype)
    #del actionNodeList, actiontype
        
    return newProp
    
def getSimpleSequenceProperty(n, prfPath):
    tmpName = n.getAttribute("name")
    tmpID   = n.getAttribute("id")
    tmpType = n.getAttribute("type")
    tmpMode = n.getAttribute("mode")
    tmpDes = n.getAttribute("description")

    if tmpName == "" or tmpID == "" or tmpType == "" or tmpMode == "":
        return None
    if tmpMode not in availableModes:
        return None
    if tmpType not in availableTypes:
        return None
    
    newProp = CC.SimpleSequenceProperty(tmpName,tmpMode,tmpType,description=tmpDes)
   
    # Set ID
    #UUID in the sad file will need to match the UUID in the prf (tmpID is from prf)
    newProp.id = tmpID


    # Get/set property values
    newProp.values = []
    newProp.defaultValues = []
    valuesNodeList = n.getElementsByTagName("values")
    
    try:
        valueNodeList = valuesNodeList[0].getElementsByTagName("value")
    except:
        valueNodeList = n.getElementsByTagName("value") #cbd
        #print "\nERROR in " + prfPath
        #print "ERROR parsing prf file.  You may be missing a values tag in a simple sequence property.\n"
        #sys.exit()
        print "\nWarning in " + prfPath
        print "Warning parsing prf file.  You may be missing a values tag in a simple sequence property.\n"

    for valueNode in valueNodeList:
        tmpVal = valueNode.childNodes[0].data
        newProp.values.append(str(tmpVal))
        newProp.defaultValues.append(str(tmpVal))
    del valueNodeList

    # Get/set property units
    unitsNodeList = n.getElementsByTagName("units")
    if len(unitsNodeList) > 0:
        units = unitsNodeList[0].childNodes[0].data
        newProp.units = str(s.units)
    #del unitsNodeList, units
    
    # TODO: Get/set min/max values
    # TODO: Get/set enum
    
    # Get/set kind
    kindNodeList = n.getElementsByTagName("kind")
    kindtype = kindNodeList[0].getAttribute("kindtype")
    if kindtype == "":
        return None
    newProp.kind = str(kindtype)
    del kindNodeList, kindtype

    # Get/set action
    actionNodeList = n.getElementsByTagName("action")
    if len(actionNodeList) > 0:
        actiontype = actionNodeList[0].getAttribute("type")
        newProp.action = str(actiontype)
    #del actionNodeList, actiontype

    return newProp
