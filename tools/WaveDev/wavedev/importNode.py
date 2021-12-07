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
from importResource import getSimpleProperty, getSimpleSequenceProperty

import ComponentClass as CC
from errorMsg import *

availableTypes = ["boolean", "char", "double", "float", "short", "long",
                    "objref", "octet", "string", "ulong","ushort"]
availableKinds = ["allocation", "configure", "test", "execparam", "factoryparam"]
availableActions = ["eq", "ne", "gt", "lt", "ge", "le", "external"]
availableModes = ["readonly", "readwrite", "writeonly"]

def getNode(inpath,Nname,parent):

    scdPath = inpath + "DeviceManager" + ".scd.xml"
    spdPath = inpath + "DeviceManager" + ".spd.xml"
    prfPath = inpath + "DeviceManager" + ".prf.xml"
    dcdPath = inpath + "DeviceManager" + ".dcd.xml"

    # import the node description from the node's .spd.xml file
    doc_node_spd = xml.dom.minidom.parse(spdPath)
    softpkgNode = doc_node_spd.getElementsByTagName("softpkg")[0]
    Ndescription = ''
    for n in softpkgNode.childNodes:
        if n.nodeName == "description":
            nDescriptionNode = doc_node_spd.getElementsByTagName("description")
            try:
                Ndescription = nDescriptionNode[0].firstChild.data
            except:
                pass
            break

    newNode = CC.Node(name=Nname, path=inpath, description=Ndescription, generate=False)

    #
    # Build the node from the DCD
    #
    doc_dcd = xml.dom.minidom.parse(dcdPath)
    partitioningNodeList = doc_dcd.getElementsByTagName('partitioning')
    if len(partitioningNodeList) != 1:
        errorMsg(parent,"Invalid file: " + dcdPath + " (partitioning)")
        return None

    try:
        deviceconfigurationNode = doc_dcd.getElementsByTagName('deviceconfiguration')[0]
    except:
        errorMsg(parent,"Invalid file: " + dcdPath + " (deviceconfiguration)")
        return None
    newNode.id = deviceconfigurationNode.getAttribute("id")

    #
    componentplacementNodeList = doc_dcd.getElementsByTagName("componentplacement")
    for componentplacementNode in componentplacementNodeList:
        newComp = CC.Component(type='executabledevice')
        newComp.name = componentplacementNode.getElementsByTagName("usagename")[0].firstChild.data

        # componentinstantiation
        # strip off the DCE: part of the id becuase it will get added back in later
        tmpUUID = componentplacementNode.getElementsByTagName("componentinstantiation")[0].getAttribute("id")
        newComp.uuid = str( tmpUUID ).strip("DCE:")

        # componentfileref
        tmpNode = componentplacementNode.getElementsByTagName("componentfileref")
        newComp.file_uuid = str( tmpNode[0].getAttribute("refid") ).strip("DCE:") # is this strip necessary?  -JDG

        local_SPD = ""
        componentfileNodeList = doc_dcd.getElementsByTagName("componentfile")
        for componentfileNode in componentfileNodeList:
            if componentfileNode.getAttribute("id") == newComp.file_uuid:
                localfileNodeList = componentfileNode.getElementsByTagName("localfile")
                local_SPD = localfileNodeList[0].getAttribute("name")
                del localfileNodeList
                break
        pathSPD = parent.installPath + local_SPD

        if not os.path.exists(pathSPD):
            errorMsg(parent, "Warning! Could not find " + pathSPD + ".\nCannot import node " + Nname)
            return None

        doc_spd = xml.dom.minidom.parse(pathSPD)
        softpkgNode = doc_spd.getElementsByTagName("softpkg")[0]
        newComp.baseName = softpkgNode.getAttribute("name")
        #pathSCD = "/sdr/sca/xml/"+newComp.baseName+"/"+doc_spd.softpkg.descriptor.localfile.name
        localfileNode = softpkgNode.getElementsByTagName("localfile")[0]
        pathSCD = parent.installPath + "/"  + localfileNode.getAttribute("name")

        doc_scd = xml.dom.minidom.parse(pathSCD)

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
        newComp.xmlName =  os.path.splitext(os.path.splitext(os.path.basename(pathSCD))[0])[0]

        newNode.Devices.append(newComp)

        #
        # Import the properties from the PRF file
        #
        # If there are no properties, just return the component as is
        #if pathPRF == None:
        #    return newComp
        #
        #doc_prf = amara.parse(stripDoctype(prfPath))
        ##doc_prf = binderytools.bind_file(prfPath)
        #if not hasattr(doc_prf,'properties'):
        #    errorMsg(parent,"Invalid file: " + prfPath)
        #    return None
        #
        #if hasattr(doc_prf.properties,"simple"):
        #    for s in doc_prf.properties.simple:
        #        p = getSimpleProperty(s)
        #        if p == None:
        #            #errorMsg(parent,"Invalid file: " + prfPath)
        #            continue
        #        newComp.properties.append(p)
        #
        #if hasattr(doc_prf.properties,"simplesequence"):
        #    for s in doc_prf.properties.simplesequence:
        #        p = getSimpleSequenceProperty(s)
        #        if p == None:
        #            #errorMsg(parent,"Invalid file: " + prfPath)
        #            continue
        #        newComp.properties.append(p)

    return newNode



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

