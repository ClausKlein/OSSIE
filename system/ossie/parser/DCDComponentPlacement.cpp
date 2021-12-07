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
#include <string>

#include "ossie/DCDComponentPlacement.h"

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

    using namespace std;


DCDComponentPlacement::DCDComponentPlacement
(DOMElement*  _elem, DOMDocument*  _doc):ComponentPlacement(_elem, _doc),
ifDeployOn(false), ifCompositePartOf(false),
ifDomainManager(false)
{
    this->parseElement();
}



DCDComponentPlacement::~DCDComponentPlacement()
{
}


void DCDComponentPlacement::parseElement()
{
    ComponentPlacement::parseElement();        // call the base class parsing 1st
    DCDComponentPlacement::parseDeployOnDevice(root);
    DCDComponentPlacement::parseCompositePartOfDevice(root);
    DCDComponentPlacement::parseDPDFileName(root);
    DCDComponentPlacement::parseInstantiations(root);


}


// \todo implement exception handling for extractFileRef
void DCDComponentPlacement::extractFileRef(DOMElement*  _elem)
{
    ifDomainManager = false;

    tmpXMLStr = XMLString::transcode("type");
    const XMLCh* _tmp = _elem->getAttribute(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    char* fileType = XMLString::transcode(_tmp);

    tmpXMLStr = XMLString::transcode("localfile");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    _elem =(DOMElement*) nodeList->item(0);

    if(strcmp(fileType, "DMD") == 0)
    {
        ifDomainManager = true;

        tmpXMLStr = XMLString::transcode("name");
        const XMLCh* _tmp1 = _elem->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        DMDFile = XMLString::transcode(_tmp1);

        DMDParser dmdParser(DMDFile.c_str());
        const char* tmpFilename = dmdParser.getDomainManagerSoftPkg();
        SPDFile = tmpFilename;

    }
    else if((strcmp(fileType, "Software Package Descriptor")) == 0 || (strcmp(fileType, "SPD") == 0))
        {
            tmpXMLStr = XMLString::transcode("name");
            const XMLCh* _tmp1 = _elem->getAttribute(tmpXMLStr);
            SPDFile = XMLString::transcode(_tmp1);
        }
        else
        {
            //Invalid Profile Exception
	    cout << "Invalid Profile in DCDComponentPlacement" << endl;
        }
}


void DCDComponentPlacement::parseDeployOnDevice(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("deployondevice");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() != 0)
    {
        ifDeployOn = true;
        DOMElement* tmpElement =(DOMElement* ) nodeList->item(0);

        tmpXMLStr = XMLString::transcode("refid");
        const XMLCh* _deployId = tmpElement->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        deployOnDeviceID = XMLString::transcode(_deployId);
    }
}


void DCDComponentPlacement::parseCompositePartOfDevice(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("compositepartofdevice");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() != 0)
    {
        DOMElement* tmpElement =(DOMElement* ) nodeList->item(0);
        tmpXMLStr = XMLString::transcode("refid");
        const XMLCh* _deviceId = tmpElement->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        compositePartOfDeviceID = XMLString::transcode(_deviceId);
    }
}


void DCDComponentPlacement::parseDPDFileName(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("devicepkgfile");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() != 0)
    {
        DOMElement* tmpElement =(DOMElement* ) nodeList->item(0);
        tmpXMLStr = XMLString::transcode("localfile");
        nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        tmpElement =(DOMElement* ) nodeList->item(0);

        tmpXMLStr = XMLString::transcode("name");
        const XMLCh* _tmp = tmpElement->getAttribute(XMLString::transcode("name"));
        DELARRAY(tmpXMLStr);
        DPDFile = XMLString::transcode(_tmp);
    }
}


void DCDComponentPlacement::parseInstantiations(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("componentinstantiation");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    int count = nodeList->getLength();
    if(count > 0)
    {
        std::vector <ComponentInstantiation* > _instantiations(count);
        DOMElement* tmpElement;

        for(int i = 0; i < count; i++)
        {
            tmpElement =(DOMElement* ) nodeList->item(i);
            _instantiations[i] = (ComponentInstantiation* ) new DCDComponentInstantiation(tmpElement);
	    _instantiationId = _instantiations[i]->getID();
	    _usageName = _instantiations[i]->getUsageName();

        }
    }

}


const char* DCDComponentPlacement::getDMDFile()
{
    return DMDFile.c_str();
}


const char* DCDComponentPlacement::getDeployOnDeviceID()
{
    return deployOnDeviceID.c_str();
}


const char* DCDComponentPlacement::getCompositePartOfDeviceID()
{
    return compositePartOfDeviceID.c_str();
}


const char* DCDComponentPlacement::getDPDFile()
{
    return DPDFile.c_str();
}


bool DCDComponentPlacement::isDeployOn()
{
    return ifDeployOn;
}


bool DCDComponentPlacement::isCompositePartOf()
{
    return ifCompositePartOf;
}


bool DCDComponentPlacement::isDomainManager()
{
    return ifDomainManager;
}


const char *DCDComponentPlacement::getFileRefId()
{
    return _fileRefId.c_str();
}

const char *DCDComponentPlacement::getInstantiationId()
{
    return _instantiationId.c_str();
}

const char *DCDComponentPlacement::getUsageName()
{
    return _usageName.c_str();
}

XMLCh* DCDComponentPlacement::tmpXMLStr = NULL;
