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
import os, copy
import shutil

import xml.dom.minidom
from xml.dom.minidom import Node

import xmlBeautify
import WaveDev.wavedev.uuidgen as uuidgen 



xmlpath = u'xml/'
binpath = u'bin/'


commentLine = u'<!--Created with OSSIE WaveDev-->\n<!--Powered by Python-->\n'

def gen_scd(comp, waveformDir, wavedevPath):
    # Generate the componentfile entries
    doc_scd = xml.dom.minidom.parse(wavedevPath + '/XML_gen/_scd.xml.tpl')

    int_types = {}

    portsNode = doc_scd.getElementsByTagName("ports")[0]

    # add provides ports to .scd.xml file
    for p in comp.ports:
      if p.type == "Provides":
        # create node for <provides> tag
        tmp_repid = u'IDL:' + unicode(p.interface.nameSpace) + u'/' + unicode(p.interface.name) + u':1.0'
        providesPortNode = doc_scd.createElement("provides")
        providesPortNode.setAttribute("repid", tmp_repid)
        providesPortNode.setAttribute("providesname", unicode(p.name))

        # create node for <porttype/> tag
        portTypeNode = doc_scd.createElement("porttype")
        portTypeNode.setAttribute("type", unicode(p.portType))
        providesPortNode.appendChild(portTypeNode)

        # append new provides port to <ports>
        portsNode.appendChild(providesPortNode)

        if p.interface.name not in int_types:
            int_types[p.interface.name] = copy.deepcopy(p.interface)

        del providesPortNode, portTypeNode

    # add uses ports to .scd.xml file
    for p in comp.ports:
      if p.type == "Uses":
        # create node for <uses> tag
        tmp_repid = u'IDL:' + unicode(p.interface.nameSpace) + u'/' + unicode(p.interface.name) + u':1.0'
        usesPortNode = doc_scd.createElement("uses")
        usesPortNode.setAttribute("repid", tmp_repid)
        usesPortNode.setAttribute("usesname", unicode(p.name))

        # create node for <porttype/> tag
        portTypeNode = doc_scd.createElement("porttype")
        portTypeNode.setAttribute("type", unicode(p.portType))
        usesPortNode.appendChild(portTypeNode)

        # append new uses port to <ports>
        portsNode.appendChild(usesPortNode)

        if p.interface.name not in int_types:
            int_types[p.interface.name] = copy.deepcopy(p.interface)

        del usesPortNode, portTypeNode

    # Add interfaces
    interfacesRootNode = doc_scd.getElementsByTagName("softwarecomponent")[0].getElementsByTagName("interfaces")[0]
    for i in int_types.values():
        tmp_repid = u'IDL:' + unicode(i.nameSpace) + u'/' + unicode(i.name) + u':1.0'
        interfaceNode = doc_scd.createElement("interface")
        interfaceNode.setAttribute("repid", tmp_repid)
        interfaceNode.setAttribute("name", unicode(i.name))
        interfacesRootNode.appendChild(interfaceNode)
    del interfacesRootNode

    # Now do final processing and write to file
    compDir = waveformDir + comp.name + '/'
    outputFileName_scd = comp.name + '.scd.xml'

    data = doc_scd.toxml('UTF-8')
    xmlBeautify.beautify(data,compDir + '.' + outputFileName_scd + '.tmp')

    preProcessed_scd = open(compDir + '.' + outputFileName_scd + '.tmp', 'r')
    postProcessed_scd = open(compDir + outputFileName_scd, 'w')

    # Specify external DTD
    line0 = preProcessed_scd.readline()
    remaining = preProcessed_scd.readlines()
    postProcessed_scd.writelines(line0)
    postProcessed_scd.writelines(u'<!DOCTYPE softwarecomponent SYSTEM \"../dtd/softwarecomponent.dtd\">\n')
    postProcessed_scd.writelines(commentLine)
    postProcessed_scd.writelines(remaining)
    postProcessed_scd.close()

    # Remove temporary files
    os.remove(compDir + '.' + outputFileName_scd + '.tmp')
    data = doc_scd.toxml('UTF-8')
    xmlBeautify.beautify(data,compDir + '.' + outputFileName_scd + '.tmp')

    preProcessed_scd = open(compDir + '.' + outputFileName_scd + '.tmp', 'r')
    postProcessed_scd = open(compDir + outputFileName_scd, 'w')

    # Specify external DTD
    line0 = preProcessed_scd.readline()
    remaining = preProcessed_scd.readlines()
    postProcessed_scd.writelines(line0)
    #postProcessed_scd.writelines(u'<!DOCTYPE softwarecomponent SYSTEM \"../dtd/softwarecomponent.dtd\">\n')
    postProcessed_scd.writelines(commentLine)
    postProcessed_scd.writelines(remaining)
    postProcessed_scd.close()


    # Remove temporary files
    os.remove(compDir + '.' + outputFileName_scd + '.tmp')



def gen_spd(comp, waveformDir, wavedevPath):
    componentName = unicode(comp.name)
    componentDescr = unicode(comp.description)

    doc_spd = xml.dom.minidom.parse(wavedevPath + '/XML_gen/_spd.xml.tpl')

    #doc_spd.softpkg.name = u'ossie' + componentName + u'Resource'
    softpkgNode = doc_spd.getElementsByTagName("softpkg")[0]
    softpkgNode.setAttribute("name",componentName)
    softpkgNode.setAttribute("id", u'DCE:' + unicode(uuidgen.uuidgen()) )

    # set the general resource description
    # note: this is NOT the description of the implementation
    for tmpNode in softpkgNode.childNodes:
        if tmpNode.nodeName == "description":
            tmpTextNode = doc_spd.createTextNode(componentDescr)
            tmpNode.appendChild(tmpTextNode)
            break

    # set the property file path
    propertyfilePathNode = softpkgNode.getElementsByTagName("propertyfile")[0].getElementsByTagName("localfile")[0]
    propertyfilePathNode.setAttribute("name", xmlpath + componentName  + '/' + componentName + u'.prf.xml')

    # set the descriptor file path
    descriptorPathNode = softpkgNode.getElementsByTagName("descriptor")[0].getElementsByTagName("localfile")[0]
    descriptorPathNode.setAttribute("name", xmlpath + componentName + '/' + componentName + u'.scd.xml')

    # set the implementation id
    implementationNode = softpkgNode.getElementsByTagName("implementation")[0]
    implementationNode.setAttribute("id", u'DCE:' + unicode(uuidgen.uuidgen()) )
    implementationNode.getElementsByTagName("code")[0].getElementsByTagName("localfile")[0].setAttribute( \
        "name", binpath + componentName)

    # Now do final processing and write to file
    compDir = waveformDir + comp.name + '/'
    outputFileName_spd = comp.name + '.spd.xml'
    #outputFileName_spd = comp.name + 'Resource' + '.spd.xml'

    data = doc_spd.toxml('UTF-8')
    xmlBeautify.beautify(data,compDir + '.' + outputFileName_spd + '.tmp')
    data = doc_spd.toxml('UTF-8')
    xmlBeautify.beautify(data,compDir + '.' + outputFileName_spd + '.tmp')


    preProcessed_spd = open(compDir + '.' + outputFileName_spd + '.tmp', 'r')
    postProcessed_spd = open(compDir + outputFileName_spd, 'w')

    # Specify external DTD
    line0 = preProcessed_spd.readline()
    remaining = preProcessed_spd.readlines()
    postProcessed_spd.writelines(line0)
    postProcessed_spd.writelines(u'<!DOCTYPE softpkg SYSTEM \"../dtd/softpkg.dtd\">\n')
    postProcessed_spd.writelines(commentLine)
    postProcessed_spd.writelines(remaining)
    postProcessed_spd.close()

    # Remove temporary files
    os.remove(compDir + '.' + outputFileName_spd + '.tmp')


def gen_prf(comp, waveformDir, wavedevPath):
    componentName = unicode(comp.name)
    doc_prf = xml.dom.minidom.parse(wavedevPath + '/XML_gen/_prf.xml.tpl')

    propertiesNode = doc_prf.getElementsByTagName("properties")[0]

    for p in comp.properties:
        if p.elementType == "Simple":
            e = doc_prf.createElement("simple")

            # Add the property value
            valueNode = doc_prf.createElement("value")
            valueText = doc_prf.createTextNode(unicode(p.value))
            valueNode.appendChild(valueText)

            e.appendChild(valueNode)

        elif p.elementType == "SimpleSequence":
            e = doc_prf.createElement("simplesequence")

            # Add the property values
            valuesNode = doc_prf.createElement("values")
            for x in p.values:
                valueNode = doc_prf.createElement("value")
                valueText = doc_prf.createTextNode(x[0])
                valueNode.appendChild(valueText)
                valuesNode.appendChild(valueNode)

            e.appendChild(valuesNode)

        e.setAttribute("type", unicode(p.type))
        e.setAttribute("id", unicode(p.id))
        e.setAttribute("name", unicode(p.name))
        e.setAttribute("mode", unicode(p.mode))

        # Add the property description
        descriptionNode = doc_prf.createElement("description")
        descriptionText = doc_prf.createTextNode(unicode(p.description))
        descriptionNode.appendChild(descriptionText)
        e.appendChild(descriptionNode)

        # Add the property kind
        kindNode = doc_prf.createElement("kind")
        kindNode.setAttribute("kindtype", unicode(p.kind))
        e.appendChild(kindNode)

        propertiesNode.appendChild(e)

    # Create a simplesequence of string type that lists each Provides port in the component
    # Used for connecting to components from outside the framework (ex. control gui)
    providesFlag = False
    for p in comp.ports:
        if p.type == "Provides":
            providesFlag = True
    if providesFlag:
        e = doc_prf.createElement("simplesequence")
        e.setAttribute("name", "port_list")
        e.setAttribute("id", "port_list")
        e.setAttribute("type", "string")
        e.setAttribute("mode", "readonly")

        # create description
        ts = 'Returns a sequence of strings with the names of the available Provides ports'
        descriptionNode = doc_prf.createElement("description")
        descriptionText = doc_prf.createTextNode(unicode(ts))
        descriptionNode.appendChild(descriptionText)
        e.appendChild(descriptionNode)

        # create kind
        kindNode = doc_prf.createElement("kind")
        kindNode.setAttribute("kindtype","configure")
        e.appendChild(kindNode)

        valuesNode = doc_prf.createElement("values")
        for p in comp.ports:
            if p.type == "Uses":
                continue
            ts = p.name + "::" + p.interface.nameSpace + "." + p.interface.name
            valueNode = doc_prf.createElement("value")
            valueText = doc_prf.createTextNode(unicode(ts))
            valueNode.appendChild(valueText)
            valuesNode.appendChild(valueNode)

        e.appendChild(valuesNode)

        propertiesNode.appendChild(e)

    # Now do final processing and write to file
    compDir = waveformDir + comp.name + '/'
    outputFileName_prf = comp.name + '.prf.xml'
    #outputFileName_prf = comp.name + 'Resource' + '.prf.xml'

    data = doc_prf.toxml('UTF-8')
    xmlBeautify.beautify(data,compDir + '.' + outputFileName_prf + '.tmp')
    data = doc_prf.toxml('UTF-8')
    xmlBeautify.beautify(data,compDir + '.' + outputFileName_prf + '.tmp')

    preProcessed_prf = open(compDir + '.' + outputFileName_prf + '.tmp', 'r')
    postProcessed_prf = open(compDir + outputFileName_prf, 'w')


    # Specify external DTD
    line0 = preProcessed_prf.readline()
    remaining = preProcessed_prf.readlines()
    postProcessed_prf.writelines(line0)
    postProcessed_prf.writelines(u'<!DOCTYPE properties SYSTEM \"../dtd/properties.dtd\">\n')
    postProcessed_prf.writelines(commentLine)
    postProcessed_prf.writelines(remaining)
    postProcessed_prf.close()


    # Remove temporary files
    os.remove(compDir + '.' + outputFileName_prf + '.tmp')
