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

import sys
import commands
import os
import shutil
import component_gen
import xml.dom.minidom
from xml.dom.minidom import Node
import xmlBeautify
import WaveDev.wavedev.ComponentClass as CC
import WaveDev.wavedev.uuidgen as uuidgen




commentLine = u'<!-- Created with OSSIE WaveDev-->\n<!--Powered by Python-->\n'

xmlpath = u'/xml/'
#######################################################################
# genxml generates xml profiles for each component and the waveform
#######################################################################
def genxml(complist, genPath, wavedevPath, waveName):

    if genPath[len(genPath)-1] != '/':
        genPath = genPath + '/'
    genPath = unicode(genPath)
    if len(wavedevPath) > 0 and wavedevPath[len(wavedevPath)-1] != '/':
        wavedevPath = wavedevPath + '/'
    waveformDir = unicode(genPath + waveName + '/')


    appName = unicode(waveName)
    #namingServicePrefix = u'ossie'
    outputFilename_sad = appName + u'.sad.xml'

    # Generate the individual component xml files
    for n in complist:
        if n.generate:
            component_gen.gen_scd(n, genPath, wavedevPath)
            component_gen.gen_spd(n, genPath, wavedevPath)
            component_gen.gen_prf(n, genPath, wavedevPath)

    #----------------------------------------------------------------------------
    # SAD Parser / Generator
    #

    # Use the minidom module to objectify and generate the SAD file
    try:  #if running from wavedev
        doc_sad = xml.dom.minidom.parse(wavedevPath + 'XML_gen/_sad.xml.tpl')
    except:   #if not being called from wavedev, try looking for the file
        doc_sad = xml.dom.minidom.parse('/sdr/tools/WaveDev/wavedev/XML_gen/_sad.xml.tpl')

    doc_sad.getElementsByTagName("softwareassembly")[0].setAttribute("name", u'OSSIE::' + appName )
    doc_sad.getElementsByTagName("softwareassembly")[0].setAttribute("id", u'DCE:' + unicode(uuidgen.uuidgen()) )

    # get root nodes for componentfiles, partitioning, assemblycontroller, and connections tags
    componentfilesNode = doc_sad.getElementsByTagName("componentfiles")[0]
    partitioningNode = doc_sad.getElementsByTagName("partitioning")[0]
    assemblycontrollerNode = doc_sad.getElementsByTagName("assemblycontroller")[0]
    connectionsNode = doc_sad.getElementsByTagName("connections")[0]

    baseComponentList = []
    for n in complist:
        # Generate the componentfile entries
        #tmpid = unicode(n.name) + u'_' + unicode(uuidgen.uuidgen())
        tmpid = unicode(n.baseName) + u'_' + unicode(n.file_uuid)

        if n.baseName not in baseComponentList:
            baseComponentList.append(n.baseName)

            # create component file tag node
            componentfileNode = doc_sad.createElement("componentfile")
            componentfileNode.setAttribute("type", "SPD")
            componentfileNode.setAttribute("id", tmpid)

            # create localfile tag node
            localfileNode = doc_sad.createElement("localfile")
            localfileNode.setAttribute("name", unicode(xmlpath + n.baseName + '/' + n.xmlName + '.spd.xml') )

            # append nodes to .sad.xml file
            componentfileNode.appendChild(localfileNode)
            componentfilesNode.appendChild(componentfileNode)

        # Generate the partitioning elements
        componentplacementNode = doc_sad.createElement("componentplacement")
        componentfilerefNode = doc_sad.createElement("componentfileref")
        componentinstantiationNode = doc_sad.createElement("componentinstantiation")
        usagenameNode = doc_sad.createElement("usagename")
        usagenameTextNode = doc_sad.createTextNode(unicode(n.name))
        usagenameNode.appendChild(usagenameTextNode)
        findcomponentNode = doc_sad.createElement("findcomponent")

        # Set attributes appropriately
        componentfilerefNode.setAttribute("refid", tmpid)
        componentinstantiationNode.setAttribute("id", u'DCE:' + unicode(n.uuid) )

        # Check for overloaded properties
        overload_flag = False
        for tmp_prop in n.properties:
            if tmp_prop.elementType == "Simple":
                if tmp_prop.value != tmp_prop.defaultValue:
                    overload_flag = True
            if tmp_prop.elementType == "SimpleSequence":
                try:
                    if tmp_prop.values != tmp_prop.defaultValues:
                        overload_flag = True
                except:
                    pass

        if overload_flag:
            componentpropertiesNode = doc_sad.createElement("componentproperties")
            for tmp_prop in n.properties:
                if tmp_prop.elementType == "Simple":
                    if tmp_prop.value != tmp_prop.defaultValue:
                        simplerefNode = doc_sad.createElement("simpleref")
                        simplerefNode.setAttribute("refid", unicode(tmp_prop.id))
                        simplerefNode.setAttribute("name", unicode(tmp_prop.name) )
                        simplerefNode.setAttribute("description", unicode(tmp_prop.description))
                        simplerefNode.setAttribute("value", unicode(tmp_prop.value))
                        componentpropertiesNode.appendChild(simplerefNode)

                if tmp_prop.elementType == "SimpleSequence":
                    ssflag = False
                    try:
                        if tmp_prop.values != tmp_prop.defaultValues:
                            ssflag = True
                    except:
                        pass

                    if ssflag:
                        simplesequencerefNode = doc_sad.createElement("simplesequenceref")
                        simplesequencerefNode.setAttribute("refid", unicode(tmp_prop.id) )
                        simplesequencerefNode.setAttribute("name", unicode(tmp_prop.name) )
                        simplesequencerefNode.setAttribute("description", unicode(tmp_prop.description) )
                        valuesNode = doc_sad.createElement("values")

                        for tmp_v2 in tmp_prop.values:
                            valueNode = doc_sad.createElement("value")
                            valuetextNode = doc_sad.createTextNode(tmp_v2)
                            valueNode.appendChild(valuetextNode)
                            valuesNode.appendChild(valueNode)

                        simplesequencerefNode.appendChild(valuesNode)
                        componentpropertiesNode.appendChild(simplesequencerefNode)

            # if there are overloaded properties, add to .sad.xml file
            componentinstantiationNode.appendChild(componentpropertiesNode)


        #NSname = u'DomainName1/' + namingServicePrefix + unicode(n.name) + u'Resource'
#        NSname = u'DomainName1/' + unicode(n.name)
        NSname = unicode(n.name)

        namingserviceNode = doc_sad.createElement("namingservice")
        namingserviceNode.setAttribute("name", NSname)
        findcomponentNode.appendChild(namingserviceNode)

        #TODO: append child nodes to componentplacement
        componentinstantiationNode.appendChild(usagenameNode)
        componentinstantiationNode.appendChild(findcomponentNode)
        componentplacementNode.appendChild(componentfilerefNode)
        componentplacementNode.appendChild(componentinstantiationNode)

        partitioningNode.appendChild(componentplacementNode)

        # Generate the connections entries
        for i in n.connections:
            cname = unicode(n.name)
            devFlag = False

#            print "Processing connection : "
#            print "  component name  : " + cname
#            print "  local comp type : " + n.type
#            print "  local port type : " + i.localPort.type
#            print "  local port name : " + unicode(i.localPort.name)
#            print "  remote comp type: " + i.remoteComp.type
#            print "  remote port type: " + i.remotePort.type
#            print "  remote port name: " + unicode(i.remotePort.name)

            if i.localPort.type == 'Uses':
                uname = unicode(i.localPort.name)
                pname = unicode(i.remotePort.name)
#                c1name = u'DomainName1/' + cname
#                c2name = u'DomainName1/' + unicode(i.remoteComp.name)
                c1name = cname
                c2name = unicode(i.remoteComp.name)
                if i.remoteComp.type.lower() == "device" \
                or i.remoteComp.type.lower() == "executabledevice" \
                or i.remoteComp.type.lower() == "aggregatedevice":
                    dev_pname = u'DomainName1/' + pname
                    devFlag = True
            else:
                pname = unicode(i.localPort.name)
                uname = unicode(i.remotePort.name)
 #               c2name = u'DomainName1/' + cname
 #               c1name = u'DomainName1/' + unicode(i.remoteComp.name)
                c2name = cname
                c1name = unicode(i.remoteComp.name)
                if n.type.lower() == "device" \
                or n.type.lower() == "executabledevice" \
                or n.type.lower() == "aggregatedevice":
                    dev_pname = u'DomainName1/' + pname
                    devFlag = True

            connectinterfaceNode = doc_sad.createElement("connectinterface")
            connectinterfaceNode.setAttribute("id",u'DCE:' + unicode(uuidgen.uuidgen()))

            usesportNode = doc_sad.createElement("usesport")
            usesidentifierNode = doc_sad.createElement("usesidentifier")
            usesidentifierTextNode = doc_sad.createTextNode(uname)
            findbyUsesNode = doc_sad.createElement("findby")
            namingserviceUsesNode = doc_sad.createElement("namingservice")
            # TODO: this is a dirty hack that needs to be fixed!
            if c1name == "USRP1":
                c1name = "DomainName1/USRP1"
            namingserviceUsesNode.setAttribute("name", c1name)

            # Append child nodes
            usesidentifierNode.appendChild(usesidentifierTextNode)
            findbyUsesNode.appendChild(namingserviceUsesNode)
            usesportNode.appendChild(usesidentifierNode)
            usesportNode.appendChild(findbyUsesNode)

            if devFlag != True:
                providesportNode = doc_sad.createElement("providesport")
                providesidentifierNode = doc_sad.createElement("providesidentifier")
                providesidentifierTextNode = doc_sad.createTextNode(pname)
                findbyProvidesNode = doc_sad.createElement("findby")
                namingserviceProvidesNode = doc_sad.createElement("namingservice")
                namingserviceProvidesNode.setAttribute("name", c2name)

                # Make connections
                providesidentifierNode.appendChild(providesidentifierTextNode)
                findbyProvidesNode.appendChild(namingserviceProvidesNode)
                providesportNode.appendChild(providesidentifierNode)
                providesportNode.appendChild(findbyProvidesNode)
                connectinterfaceNode.appendChild(providesportNode)
                connectinterfaceNode.appendChild(usesportNode)

            else:
                findbyProvidesNode = doc_sad.createElement("findby")
                namingserviceProvidesNode = doc_sad.createElement("namingservice")
                namingserviceProvidesNode.setAttribute("name", dev_pname)

                # Make connections
                # TODO: validate this XML
                findbyProvidesNode.appendChild(namingserviceProvidesNode)
                connectinterfaceNode.appendChild(findbyProvidesNode)
                connectinterfaceNode.appendChild(usesportNode)

            # Append connectinterface to connections
            connectionsNode.appendChild(connectinterfaceNode)

        # Specify the uuid for the Assembly Controller
        if n.AssemblyController == True:
            assemblycontroller_id = u'DCE:' + unicode(n.uuid)
            assemblycontrollerNode.getElementsByTagName("componentinstantiationref")[0].setAttribute("refid", assemblycontroller_id)

    # Create and beautify the SAD file as a temporary file
    data = doc_sad.toxml('UTF-8')
    xmlBeautify.beautify(data,waveformDir + '.' + outputFilename_sad + '.tmp')

    # Post Processing - add some of the header lines


    preProcessed_sad = open(waveformDir + '.' + outputFilename_sad + '.tmp', 'r')
    postProcessed_sad = open(waveformDir + outputFilename_sad, 'w')

    # Specify external DTD
    line0 = preProcessed_sad.readline()
    remaining = preProcessed_sad.readlines()
    postProcessed_sad.writelines(line0)
    postProcessed_sad.writelines(u'<!DOCTYPE softwareassembly SYSTEM \"../../xml/dtd/softwareassembly.dtd\">\n')
    postProcessed_sad.writelines(commentLine)
    postProcessed_sad.writelines(remaining)
    postProcessed_sad.close()

    # Remove temporary files
    os.remove(waveformDir + '.' + outputFilename_sad + '.tmp')


    #######################
    #Generate the DCD file
    #######################
    #genDCD(complist,genPath,waveName,xmlpath)

################################################################################
# Generate the Device Assignment Sequence
def genDAS(complist, path, wavedevPath, waveName):
    if path[len(path)-1] != '/':
        path = path + '/'
    path += waveName + '/'

    try:
        # try to find the DAS template using a relative path (being called by OWD)
        das = xml.dom.minidom.parse(wavedevPath + 'XML_gen/_DAS.xml.tpl')
    except:
        # try to find the DAS template using an absolute path
        # (being called by other application)
        # if DAS file is still not found, should throw an IO Error
        das = xml.dom.minidom.parse('/sdr/tools/WaveDev/wavedev/XML_gen/_DAS.xml.tpl')

    deviceassignmentsequenceNode = das.getElementsByTagName("deviceassignmentsequence")[0]

    for n in complist:
        if n.uuid[0:4] == "DCE:":
            tmpName = unicode(n.uuid)
        else:
            tmpName = u'DCE:' + unicode(n.uuid)
        #tmpDev = u'DCE:b35dcdfa-a858-4b33-94b5-5feb007dd15c'
        if n.device == None:
            continue
        tmpDev = u'DCE:' + unicode(n.device.uuid)

        deviceassignmenttypeNode = das.createElement("deviceassignmenttype")
        componentidNode = das.createElement("componentid")
        componentidTextNode = das.createTextNode(tmpName)
        assigndeviceidNode = das.createElement("assigndeviceid")
        assigndeviceidTextNode = das.createTextNode(tmpDev)

        # Append nodes
        componentidNode.appendChild(componentidTextNode)
        assigndeviceidNode.appendChild(assigndeviceidTextNode)
        deviceassignmenttypeNode.appendChild(componentidNode)
        deviceassignmenttypeNode.appendChild(assigndeviceidNode)
        deviceassignmentsequenceNode.appendChild(deviceassignmenttypeNode)

    data = das.toxml('UTF-8')
    xmlBeautify.beautify(data,path+'.'+waveName+'_DAS.xml.tmp')



    # Post Processing - add some of the header lines

    preProcessed_das = open(path+'.'+waveName+'_DAS.xml.tmp', 'r')
    postProcessed_das = open(path+waveName+'_DAS.xml', 'w')

    # Specify external DTD
    line0 = preProcessed_das.readline()
    remaining = preProcessed_das.readlines()
    postProcessed_das.writelines(line0)
    postProcessed_das.writelines(u'<!DOCTYPE deploymentenforcement SYSTEM "dtd/deploymentenforcement.dtd\">\n')
    postProcessed_das.writelines(commentLine)
    postProcessed_das.writelines(remaining)
    postProcessed_das.close()

    # Remove temporary files
    os.remove(path+'.'+waveName+'_DAS.xml.tmp')


################################################################################
# Generate the DeviceManager XML files
def genDeviceManager(node, path, wavedevPath, wavName, dmName, folder = False):
    if path[len(path)-1] != '/':
        path = path + '/'
    path += wavName + '/'

    waveformDir = path
    if folder == True:
        if os.path.exists(path + node.name) == False:
            os.mkdir(path + node.name)
        path += node.name + '/'

    #Generate the DCD file for the Device Manager
    genDCD(node.Devices, path, wavedevPath, node.name, dmName, folder, node.generate, node.id)

    outputFilename_spd = dmName + '.spd.xml'
    outputFilename_scd = dmName + '.scd.xml'
    outputFilename_prf = dmName + '.prf.xml'

    #Copy and modify the spd file
    doc_spd = xml.dom.minidom.parse(wavedevPath + 'XML_gen/DevMan/_spd.xml.tpl')
    doc_spd.getElementsByTagName("softpkg")[0].setAttribute("name", dmName)
    localfileNode = doc_spd.getElementsByTagName("descriptor")[0].getElementsByTagName("localfile")[0]
    localfileNode.setAttribute("name", unicode(dmName) + u'.scd.xml')

    data = doc_spd.toxml('UTF-8')
    xmlBeautify.beautify(data,path + '.' + outputFilename_spd + '.tmp')
    data = doc_spd.toxml('UTF-8')
    xmlBeautify.beautify(data,path + '.' + outputFilename_spd + '.tmp')


    # Post Processing - add some of the header lines

    preProcessed_spd = open(path + '.' + outputFilename_spd + '.tmp', 'r')
    postProcessed_spd = open(path + outputFilename_spd, 'w')

    # Specify external DTD
    line0 = preProcessed_spd.readline()
    remaining = preProcessed_spd.readlines()
    postProcessed_spd.writelines(line0)
    postProcessed_spd.writelines(u'<!DOCTYPE softpkg SYSTEM \"../../xml/dtd/softpkg.dtd\">\n')
    postProcessed_spd.writelines(commentLine)
    postProcessed_spd.writelines(remaining)
    postProcessed_spd.close()

    #tempDM = CC.Component(dmName,generate=False)
    #component_gen.gen_scd(tempDM,waveformDir,node.name)


    # Post Processing - add some of the header lines
    preProcessed_spd = open(path + '.' + outputFilename_spd + '.tmp', 'r')
    postProcessed_spd = open(path + outputFilename_spd, 'w')

    # Specify external DTD
    line0 = preProcessed_spd.readline()
    remaining = preProcessed_spd.readlines()
    postProcessed_spd.writelines(line0)
    postProcessed_spd.writelines(u'<!DOCTYPE softpkg SYSTEM \"../../xml/dtd/softpkg.dtd\">\n')
    postProcessed_spd.writelines(commentLine)
    postProcessed_spd.writelines(remaining)
    postProcessed_spd.close()

    # Remove temporary files
    os.remove(path + '.' + outputFilename_spd + '.tmp')

    #tempDM = CC.Component(dmName,generate=False)
    #component_gen.gen_scd(tempDM,waveformDir,node.name)


    # Copy the scd and prf files to directory - these aren't changed yet
    print "Performing a copy to: " + path + outputFilename_scd
    shutil.copyfile(wavedevPath + 'XML_gen/DevMan/_scd.xml.tpl', path + outputFilename_scd)
    shutil.copyfile(wavedevPath + 'XML_gen/DevMan/_prf.xml.tpl', path + outputFilename_prf)



################################################################################
# Generate the DeviceManager DCD.xml file
def genDCD(devlist, path, wavedevPath, nodeName, dmName = 'DeviceManager', folder = False, generate = True, devconf = ""):

    outputFilename_dcd = dmName + '.dcd.xml'

    doc_dcd = xml.dom.minidom.parse(wavedevPath + 'XML_gen/_dcd.xml.tpl')

    deviceconfigurationNode = doc_dcd.getElementsByTagName("deviceconfiguration")[0]

    if devconf=="":
        deviceconfigurationNode.setAttribute("id", u'DCE:' + unicode(uuidgen.uuidgen()))
    else:
        deviceconfigurationNode.setAttribute("id", unicode(devconf) )

    deviceconfigurationNode.setAttribute("name", unicode(dmName) )

    devicemanagersoftpkgNode = deviceconfigurationNode.getElementsByTagName("devicemanagersoftpkg")[0]
    devicemanagersoftpkgNode.getElementsByTagName("localfile")[0].setAttribute("name", unicode(dmName) + u'.spd.xml')

    baseDeviceList = []
    componentfilesNode = deviceconfigurationNode.getElementsByTagName("componentfiles")[0]
    partitioningNode = deviceconfigurationNode.getElementsByTagName("partitioning")[0]
    for n in devlist:
        if generate:
            tmpid = unicode(n.name) + u'_' + unicode(n.file_uuid)
        else:
            tmpid = unicode(n.file_uuid)

        if n.baseName not in baseDeviceList:
        # Generate the componentfile entries
            baseDeviceList.append(n.baseName)
            componentfileNode = doc_dcd.createElement("componentfile")
            componentfileNode.setAttribute("type", "SPD")
            componentfileNode.setAttribute("id", tmpid)

            localcomponentfileNode = doc_dcd.createElement("localfile")
            localcomponentfileNode.setAttribute("name", unicode(xmlpath + n.baseName + '/' + n.baseName + '.spd.xml') )

            componentfileNode.appendChild(localcomponentfileNode)
            componentfilesNode.appendChild(componentfileNode)

        # Generate the partitioning entries
        componentplacementNode = doc_dcd.createElement("componentplacement")
        componentfilerefNode = doc_dcd.createElement("componentfileref")
        componentfilerefNode.setAttribute("refid", tmpid)
        componentinstantiationNode = doc_dcd.createElement("componentinstantiation")
        componentinstantiationNode.setAttribute("id", u'DCE:' + unicode(n.uuid) )
        usagenameNode = doc_dcd.createElement("usagename")
        usagenameTextNode = doc_dcd.createTextNode(n.name)

        # Append nodes to partitioning
        usagenameNode.appendChild(usagenameTextNode)
        componentinstantiationNode.appendChild(usagenameNode)
        componentplacementNode.appendChild(componentfilerefNode)
        componentplacementNode.appendChild(componentinstantiationNode)
        partitioningNode.appendChild(componentplacementNode)

    # Create and beautify the dcd file as a temporary file
    data = doc_dcd.toxml('UTF-8')
    xmlBeautify.beautify(data,path + '.' + outputFilename_dcd + '.tmp')
    # Create and beautify the dcd file as a temporary file
    data = doc_dcd.toxml('UTF-8')
    xmlBeautify.beautify(data,path + '.' + outputFilename_dcd + '.tmp')

    # Post Processing - add some of the header lines

    preProcessed_dcd = open(path + '.' + outputFilename_dcd + '.tmp', 'r')
    postProcessed_dcd = open(path + outputFilename_dcd, 'w')

    # Specify external DTD
    line0 = preProcessed_dcd.readline()
    remaining = preProcessed_dcd.readlines()
    postProcessed_dcd.writelines(line0)
    postProcessed_dcd.writelines(u'<!DOCTYPE deviceconfiguration SYSTEM \"../../xml/dtd/deviceconfiguration.dtd\">\n')
    postProcessed_dcd.writelines(commentLine)
    postProcessed_dcd.writelines(remaining)
    postProcessed_dcd.close()

    # Remove temporary files
    os.remove(path + '.' + outputFilename_dcd + '.tmp')



def writeWaveSetuppy(wavePath, wavedevPath, waveName):
    '''
    ##############################################################################
    ## writeWaveSetuppy - generates the setup.py file for a waveform
    ##############################################################################
    '''

    if wavePath[len(wavePath)-1] != '/':
        wavePath = wavePath + '/' + waveName

    #copy over the readme file
    shutil.copy(wavedevPath + 'XML_gen/README', wavePath)

    output = open(wavePath + '/setup.py','w')
    ts = "\
#! /usr/bin/env python\n\
\n\
from distutils.core import setup\n\
import sys\n\
\n\
install_location = '/sdr'\n\
\n\
if len(sys.argv) != 2:\n\
        sys.exit(1)\n\
\n\
sys.argv.append('--install-lib='+install_location)\n\n"
    output.writelines(ts)

    ts = "setup(name='" + waveName + "', description='" + waveName + \
         "',data_files=[(install_location+'/waveforms/" + waveName + "',['" + \
         waveName + ".sad.xml', '" + waveName + "_DAS.xml'])])"
    output.writelines(ts)

    output.close()   #done creating the file

