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

#include "ossie/ExternalPort.h"
#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;


ExternalPort::ExternalPort(DOMElement* _elem):
root(_elem),
ifUsesIdentifier(false),
ifProvidesIdentifier(false),
ifSupportedIdentifier(false)
{
    this->parseElement();
}

ExternalPort::~ExternalPort()
{
   if (this->root !=NULL) this->root->release();
}


void ExternalPort::parseElement()
{
    parseUsesIdentifier(root);

    if(!isUsesIdentifier())
    {
        parseProvidesIdentifier(root);

        if(!isProvidesIdentifier()) parseSupportedIdentifier(root);
    }

    parseComponentInstantiationRefId(root);
}


void ExternalPort::parseUsesIdentifier(DOMElement* _elem)
{
    tmpXMLStr = XMLString::transcode("usesidentifier");
    DOMNodeList*nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() == 0)
    return;

    usesIdentifier = getTextNode((DOMElement*) nodeList->item(0));
    ifUsesIdentifier = true;
}


void ExternalPort::parseProvidesIdentifier(DOMElement* _elem)
{
    tmpXMLStr = XMLString::transcode("providesidentifier");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() == 0)
    return;

    providesIdentifier = getTextNode((DOMElement*) nodeList->item(0));
    ifProvidesIdentifier = true;    // this could be problematic if getTextNode
                    // returns "Not Specified"
}


void ExternalPort::parseSupportedIdentifier(DOMElement* _elem)
{
    tmpXMLStr = XMLString::transcode("supportedidentifier");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() == 0)
    return;

    supportedIdentifier = getTextNode((DOMElement*) nodeList->item(0));
    ifSupportedIdentifier = true;
}


void ExternalPort::parseComponentInstantiationRefId(DOMElement* _elem)
{
    tmpXMLStr = XMLString::transcode("componentinstantiationref");
    DOMNodeList*nodeList =_elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() == 0)
    return;

    DOMElement*tmpElement =(DOMElement*) nodeList->item(0);
    tmpXMLStr = XMLString::transcode("refid");
    const XMLCh*_tmp = tmpElement->getAttribute(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    componentInstantiationRefId = XMLString::transcode(_tmp);
}


char* ExternalPort::getTextNode(DOMElement* _elem)
{
    DOMNodeList*nodeList = _elem->getChildNodes();

    if(nodeList->getLength() == 0)
    {
        char* astr = new char[strlen("Not Specified") +1];
        strcpy(astr,"Not Specified");
        return astr;
    }
    else return XMLString::transcode(nodeList->item(0)->getNodeValue());
}


char* ExternalPort::toString()
{
    char*str = new char[MAX_BUFFER];

    if(isUsesIdentifier())
    {
    str = strcpy(str, "\n    UsesIdentifier=");
    str = strcat(str, getUsesIdentifier());
    }
    else if(isProvidesIdentifier())
    {
    str = strcpy(str, "\n    ProvidesIdentifier=");
    str = strcat(str, getProvidesIdentifier());
    }
    else if(isSupportedIdentifier())
    {
    str = strcpy(str, "\n    SupportedIdentifier=");
    str = strcat(str, getSupportedIdentifier());
    }
    else
    str = strcpy(str, "\n   NO IDENTIFIER PROVIDED...this is an ERROR!! ");

    str = strcat(str, "\n    ComponentInstantiationRefId=");
    str = strcat(str, getComponentInstantiationRefId());

    return str;
}


bool ExternalPort::isUsesIdentifier()
{
    return ifUsesIdentifier;
}


bool ExternalPort::isProvidesIdentifier()
{
    return ifProvidesIdentifier;
}


bool ExternalPort::isSupportedIdentifier()
{
    return ifSupportedIdentifier;
}


const char* ExternalPort::getUsesIdentifier()
{
    return usesIdentifier.c_str();
}


const char* ExternalPort::getProvidesIdentifier()
{
    return providesIdentifier.c_str();
}


const char* ExternalPort::getSupportedIdentifier()
{
    return supportedIdentifier.c_str();
}


const char* ExternalPort::getComponentInstantiationRefId()
{
    return componentInstantiationRefId.c_str();
}

XMLCh* ExternalPort::tmpXMLStr = NULL;
