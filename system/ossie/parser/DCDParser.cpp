/*******************************************************************************

Copyright 2008, Virginia Polytechnic Institute and State University

This file is part of the OSSIE Parser.

OSSIE Parser is free software; you can redistribute it and/or modify
it under the terms of the Lesser GNU General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

OSSIE Parser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with OSSIE Parser; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Even though all code is original, the architecture of the OSSIE Parser is based
on the architecture of the CRCs SCA Reference Implementation(SCARI)
see: http://www.crc.ca/en/html/rmsc/home/sdr/projects/scari

*********************************************************************************/

#include <iostream>

#ifdef HAVE_STRING_H
#include <string.h>    // using POSIX strcpy
#endif

#include "ossie/DCDParser.h"

    using namespace std;

#define DELPTR(x) if(x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if(x!=NULL) delete []x, x=NULL;


componentFile::componentFile(const char *id, const char *fileName)

{

    _fileName = fileName;
    _id = id;
    
}

const char* componentFile::fileName()

{
    return _fileName.c_str();
}

const char* componentFile::id()

{
    return _id.c_str();
}


componentPlacement::componentPlacement(const char *refId, const char *id, const char *usageName)
{

    _refId = refId;
    _id = id;
    _usageName = usageName;
}

const char *componentPlacement::refId()
{

    return _refId.c_str();
}

const char *componentPlacement::id()
{

    return _id.c_str();
}

const char *componentPlacement::usageName()
{

    return _usageName.c_str();
}

/** default constructor with initialised value
*/
DCDParser::DCDParser(const char* _DCDFile):ComponentAssemblyParser(_DCDFile)
{
    initializeDCD();
    this->parseFile();
}


DCDParser::~DCDParser()
{
    DELPTR(domainManagerComponent);
/*
    // This shouldn't cause seg faults. But it does. Need to find out why. -TT
    for (unsigned int i=0; localComponents.size(); i++)
    {
        DELARRAY(localComponents[i]);
    }
*/

    // This will cause seg faults. See copy constructor. -TT    
    // not anymore! TP 10/14/05
    for (unsigned int i=0; deployOnComponents.size(); i++)
    {
        DELPTR(deployOnComponents[i]);
    }
}


// \todo implement exception handling
void DCDParser::initializeDCD()
{
    domainManagerComponent = NULL;

    // Testing -TT
    deployOnComponents.clear();

    char* tmp = XMLString::transcode(doc->getDocumentElement()->getNodeName());

    if(strcmp(tmp, "deviceconfiguration") != 0)
    {
    //InvalidProfile
	cout << "Invalid profile in DCD Parser" << endl;
    }
    delete []tmp;
}


void DCDParser::parseFile()
{
    DOMElement* _root = doc->getDocumentElement();
    this->parseIdAndName(_root);
    this->parseDeviceManagerSoftPkg(_root);
    this->parseComponentPlacement(_root);
    this->parseDomainManager(_root);
    this->parseConnections(_root);
    this->parseLocalComponents(_root);
}


void DCDParser::parseDeviceManagerSoftPkg(DOMElement*  _elem)
{
    XMLCh* tmpXMLStr = XMLString::transcode("devicemanagersoftpkg");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    DOMElement* tmpElement = (DOMElement*) nodeList->item(0);
    tmpXMLStr = XMLString::transcode("localfile");
    nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    tmpElement =(DOMElement* ) nodeList->item(0);

    tmpXMLStr = XMLString::transcode("name");
    const XMLCh* _tmp = tmpElement->getAttribute(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    deviceManagerSoftPkg = XMLString::transcode(_tmp);
}


void DCDParser::parseLocalComponents(DOMElement*  _elem)
{
    DOMElement* tmpElement;

    XMLCh* tmpXMLStr = XMLString::transcode("componentfile");
    DOMNodeList* nodeList =_elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);



    DOMNodeList* nodeList2;

    for(unsigned int i = 0; i < nodeList->getLength(); i++)
    {
	tmpElement =(DOMElement* ) nodeList->item(i);
	tmpXMLStr = XMLString::transcode("id");
	const XMLCh* id = tmpElement->getAttribute(tmpXMLStr);
	DELARRAY(tmpXMLStr);
	
        tmpElement =(DOMElement* ) nodeList->item(i);
        tmpXMLStr = XMLString::transcode("localfile");
        nodeList2 = tmpElement->getElementsByTagName(tmpXMLStr);
        DELARRAY(tmpXMLStr);

        tmpElement =(DOMElement* ) nodeList2->item(0);
        tmpXMLStr = XMLString::transcode("name");
        const XMLCh* name = tmpElement->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);

	componentFiles.push_back(componentFile(XMLString::transcode(id), XMLString::transcode(name)));

    }

}

void DCDParser::parseComponentPlacement(DOMElement*  _elem)
{
    XMLCh* tmpXMLStr = XMLString::transcode("componentplacement"); 
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    
    DOMElement* tmpElement;

    for(unsigned int i = 0; i < nodeList->getLength(); i++)
    {
        tmpElement =(DOMElement*) nodeList->item(i);
        DCDComponentPlacement* dcdComponent = new DCDComponentPlacement(tmpElement, doc);

        if(dcdComponent->isDomainManager()) {
            domainManagerComponent = dcdComponent;
        } else if(dcdComponent->isDeployOn()) {
	    deployOnComponents.push_back(dcdComponent);
        }
	else {
	    componentPlacements.push_back(componentPlacement(dcdComponent->getFileRefId(), dcdComponent->getInstantiationId(), dcdComponent->getUsageName()));
	}
    }
}


void DCDParser::parseDomainManager(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("domainmanager");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    
    DOMElement* tmpElement =(DOMElement* ) nodeList->item(0);
    tmpXMLStr = XMLString::transcode("namingservice");
    nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() != 0)
    {
        tmpElement =(DOMElement* ) nodeList->item(0);

        tmpXMLStr = XMLString::transcode("name");
        const XMLCh* _name = tmpElement->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        domainManagerName = XMLString::transcode(_name);
    }
    else
    {
        tmpXMLStr = XMLString::transcode("stringifiedobjectref");
        nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
        DELARRAY(tmpXMLStr);

        if(nodeList->getLength() != 0)
        {
            tmpElement =(DOMElement*) nodeList->item(0);
            domainManagerIOR = getTextNode(tmpElement);
        }
        //else //invalid profile
    }
}


const char* DCDParser::getDCDFilename()
{
    return fileName.c_str();
}


const char* DCDParser::getDeviceManagerSoftPkg()
{
    return deviceManagerSoftPkg.c_str();
}


const char* DCDParser::getDomainManagerName()
{
    return domainManagerName.c_str();
}


const char* DCDParser::getDomainManagerIOR()
{
    return domainManagerIOR.c_str();
}


DCDComponentPlacement* DCDParser::getDomainManagerComponent() const
{
    return domainManagerComponent;
}


std::vector <DCDComponentPlacement*>*
DCDParser::getDeployOnComponents()
{
    return &deployOnComponents;
}

std::vector <componentFile> DCDParser::getComponentFiles()

{

    return componentFiles;
}

std::vector <componentPlacement> DCDParser::getComponentPlacements()
{

    return componentPlacements;
}

const char *DCDParser::getFileNameFromRefId(const char *refid)
{
    for (unsigned int i=0; i<componentFiles.size(); i++) {
	if (strcmp(refid, componentFiles[i].id()) == 0)
	    return componentFiles[i].fileName();
    }
    return NULL;
}

char* DCDParser::toString()
{
    std::vector < DCDComponentPlacement*  >*dcdComponentArray = NULL;
    std::vector < char* >*dcdLocalComponentsArray = NULL;
    char* str = new char[MAX_DCD_BUF];

    str = strcat(str, "\n  DCDFilename=");
    str = strcat(str, getDCDFilename());
    str = strcat(str, "\n  ID=");
    str = strcat(str, getID());
    str = strcat(str, "\n  Name=");
    str = strcat(str, getName());
    str = strcat(str, "\n  deviceManagerSoftPkg=");
    str = strcat(str, getDeviceManagerSoftPkg());

    if(domainManagerName != "")
    {
    str = strcat(str, "\n  domainManagerName=");
    str = strcat(str, getDomainManagerName());
    }
    else
    {
    str = strcat(str, "\n  domainManagerIOR=");
    str = strcat(str, getDomainManagerIOR());
    }

    if(domainManagerComponent != NULL)
    str = strcat(str, "\n   domainManagerComponent");


    dcdComponentArray = getDeployOnComponents();

    if(dcdComponentArray->size() > 0)
    {
    for(unsigned int i = 0; i < dcdComponentArray->size(); i++)
    {
    char _tmp;
    str = strcat(str, "\n   DeployOnComponent[");
    //str = strcat(str, ACE_OS::itoa(i, &_tmp, 10));
    str = strcat(str, "]");
    str = strcat(str,(*dcdComponentArray)[i]->getSPDFile());
    }
    }
    else
    str = strcat(str, "\n   There are no Deploy Components");
/*
    std::vector<Connection*> _connections = getConnections();

    if(_connections.size()>0)
    {

    for(int i = 0; i < _connections.size(); i++)
    {
    str = str + "\n   Connections[" +(char* )i + "]" +  _connections[i].getID();
    }
    }
else
{
str = str + "\n   There are no connections";
}
*/
    return str;
}
XMLCh* DCDParser::tmpXMLStr = NULL;
