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

import os, sys
import xml.dom.minidom
from xml.dom.minidom import Node

try:  # mac ossie
    import WaveformClass as WC
    import ComponentClass as CC
    from errorMsg import *
    import importResource
    from XML_gen import xmlBeautify

except ImportError:     # 0.6.2
    import WaveDev.wavedev.WaveformClass as WC
    import WaveDev.wavedev.ComponentClass as CC
    from WaveDev.wavedev.errorMsg import *
    import WaveDev.wavedev.importResource as importResource
    from WaveDev.wavedev.XML_gen import xmlBeautify
    
import copy

def getWaveform(sad_path, parent, interfaces):
    if not os.path.isfile(sad_path) or sad_path[-8:].lower() != ".sad.xml":
        errorMsg(parent, "Invalid SAD file: " + sad_path)
        return None
    
    # Create a binding of the SAD file
    doc_sad = xml.dom.minidom.parse(sad_path)

    # TODO: validate SAD file against the dtd

    # try to find "softwareassembly" node
    try:
        softwareassemblyNode = doc_sad.getElementsByTagName("softwareassembly")[0]
    except:
        errorMsg(parent, "Invalid SAD file: " + sad_path + "; no \"softwareassembly\" tag")
        return None
    
    # try to find "componentfiles" node
    try:
        componentfilesNode = softwareassemblyNode.getElementsByTagName("componentfiles")[0]
    except:
        errorMsg(parent, "Invalid SAD file: " + sad_path + "; no \"componentfiles\" tag")
        return None

    # At this point, assume SAD file validates against the DTD; no longer
    # necessary to use try/except statements
    waveform_name = softwareassemblyNode.getAttribute("name")
    new_waveform = WC.Waveform(str(waveform_name))

    # Get list of "componentfile" nodes from SAD file
    componentfileNodeList = componentfilesNode.getElementsByTagName("componentfile")
    
    # Dictionary storing mapping of componentfile ids to file names (unicode)
    compfiles = {}  
    for componentfileNode in componentfileNodeList:
        localfilename = componentfileNode.getElementsByTagName("localfile")[0].getAttribute("name")
        #tmps = cf.localfile.name.replace('../..', '/sdr') # get absolute path
        tmps = "/sdr/" + localfilename
        base_name = getBaseName(tmps)
        # TODO: this next line is a dirty hack: use the python os module to strip name from path
        tmps = tmps[0:tmps.rfind('/')]  # remove actual file name (importResource format)
        componentfileid = componentfileNode.getAttribute("id")
        compfiles[componentfileid] = (tmps,base_name)

    # Create the component objects from the componentplacement section
    componentplacementNodeList = softwareassemblyNode.getElementsByTagName("componentplacement")
    for componentplacementNode in componentplacementNodeList:
        # get refid
        componentfilerefNode = componentplacementNode.getElementsByTagName("componentfileref")[0]
        refid = componentfilerefNode.getAttribute("refid")

        # get component path from compfiles dictionary
        comp_path = compfiles[refid][0]

        # get componentinstantiation id (strip off "DCE:")
        componentinstantiationNode = componentplacementNode.getElementsByTagName("componentinstantiation")[0]
        comp_id = str(componentinstantiationNode.getAttribute("id")).replace("DCE:","")

        # get component base name from compfiles dictionary
        comp_base_name = str(compfiles[refid][1])

        # get usagename
        usagenameNode = componentinstantiationNode.getElementsByTagName("usagename")[0]
        comp_name = str(usagenameNode.firstChild.data)

        new_comp = importResource.getResource(comp_path, comp_base_name, parent)
        new_comp.name = comp_name
        new_comp.uuid = comp_id
        new_comp.file_uuid = str(refid.replace(comp_base_name + '_',''))
        new_waveform.components.append(new_comp)
    
    # Assign interfaces based on import IDL - gets the operations right this way
    for comp in new_waveform.components:
        assignInterfaces(comp,interfaces)
    
    # Find and set the AssemblyController through its refid
    assemblycontrollerNode = softwareassemblyNode.getElementsByTagName("assemblycontroller")[0]
    # NOTE: first and only child is "componentinstantiationref"
    componentinstantiationrefNode = assemblycontrollerNode.getElementsByTagName("componentinstantiationref")[0]
    ac = str(componentinstantiationrefNode.getAttribute("refid"))
    ac = ac.replace("DCE:","")
    for c in new_waveform.components:
        if c.uuid == ac:
            c.AssemblyController = True


    # Create the connections
    connectinterfaceNodeList = softwareassemblyNode.getElementsByTagName("connectinterface")

    if len(connectinterfaceNodeList) != 0:
        for connectinterfaceNode in connectinterfaceNodeList:
            usesportNode = connectinterfaceNode.getElementsByTagName("usesport")[0]
            usesid = usesportNode.getElementsByTagName("usesidentifier")[0].firstChild.data
            # NOTE: first and only child of "findby" node is "namingservice"
            findbyNode = usesportNode.getElementsByTagName("findby")[0]
            nsname = findbyNode.getElementsByTagName("namingservice")[0].getAttribute("name")
            usesid = str(usesid)
            nsname = str(nsname)

            uses_comp = getCompFromNSName(nsname,new_waveform)

            # Check for providesport
            providesportNodeList = connectinterfaceNode.getElementsByTagName("providesport")
            if len(providesportNodeList) != 0:
                # "providesport" tag exists
                providesportNode = providesportNodeList[0]

                # get providesidentifier
                providesidentifierNode = providesportNode.getElementsByTagName("providesidentifier")[0]
                providesid = str(providesidentifierNode.firstChild.data)

                # get namingservice name
                # NOTE: first and only child of "findby" node is "namingservice"
                findbyNode = providesportNode.getElementsByTagName("findby")[0]
                nsname = str(findbyNode.getElementsByTagName("namingservice")[0].getAttribute("name"))
                provides_comp = getCompFromNSName(nsname,new_waveform)
            else:
                # "providesport" tag does not exist
                # Probably is a hardware port located directly on the naming service
                # Not supporting this quite yet
                continue
                # NOTE: the next line is only supported with amara
                if not hasattr(ci, 'findby'):
                    errorMsg(parent, "Invalid SAD file")
                    return None
                
                nsname = str(ci.findby.namingservice.name)


            uses_port = None
            provides_port = None

            #try statement is a temporary fix to ALF's inability to display devices
            try:
                for port in uses_comp.ports:
                    if port.name == usesid:
                        uses_port = port
                for port in provides_comp.ports:
                    if port.name == providesid:
                        provides_port = port

                # Unfortunately there is no information stored in the XML about which component
                # initiated the connection in OWD - so we'll say that uses is always the local port
                new_connection = CC.Connection(uses_port, provides_port, provides_comp)

                uses_comp.connections.append(new_connection)
            except:
                pass    #skip the device

    return new_waveform


# Find and return the component from its naming service name
def getCompFromNSName(nsname, waveform):
    nsname = nsname.replace("DomainName1/","")
    i = nsname.rfind('/')
    if i >= 0:
        nsname = nsname[i+1:]
    
    for comp in waveform.components:
        if comp.name == nsname:
            return comp

    return None

# parse the spd file and return the name of the component base class
def getBaseName(spd_path):
    if not os.path.isfile(spd_path) or spd_path[-8:].lower() != ".spd.xml":
        errorMsg(parent, "Invalid SPD file: " + spd_path)
        return None
    
    # Create a binding of the SAD file
    doc_spd = xml.dom.minidom.parse(spd_path)
    # TODO: validate against dtd
    try:
        softpkgNode = doc_spd.getElementsByTagName("softpkg")[0]
    except:
        errorMsg(parent, "Invalid SPD file: " + spd_path + "; no \"softpkg\" node found")
        return None
        
    return str(softpkgNode.getAttribute("name"))
    
def assignInterfaces(comp, interfaces):
    for port in comp.ports:
        for i in interfaces:
            if i.name == port.interface.name and i.nameSpace == port.interface.nameSpace:
                port.interface = copy.deepcopy(i)
    
