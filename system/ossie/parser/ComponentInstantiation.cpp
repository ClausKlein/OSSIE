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
on the architecture of the CRCs SCA Reference Implementation (SCARI)
see: http://www.crc.ca/en/html/rmsc/home/sdr/projects/scari

*********************************************************************************/

#include "ossie/ComponentInstantiation.h"
#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

#include <string>
#include <iostream>


ComponentInstantiation::ComponentInstantiation (DOMElement* _element):
root(_element)
{
    this->parseElement();
}

ComponentInstantiation::~ComponentInstantiation()
{

    for (unsigned int i=0; i< properties.size(); i++)    // deep clean
    {
        DELPTR(properties[i]);
    }
}


void ComponentInstantiation::parseElement()
{
    parseID(root);
    parseName(root);
    parseProperties(root);
}

void ComponentInstantiation::parseID(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("id");
    const XMLCh *_id = _elem->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    instantiationId = XMLString::transcode(_id);
}


void ComponentInstantiation::parseName(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("usagename");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
        DOMElement* elem = (DOMElement*) nodeList->item(0);
        usageName = getTextNode(elem);
    }
}


void ComponentInstantiation::parseProperties(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("componentproperties");
    DOMNodeList* nodeList =  _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() > 0) {
	DOMNodeList *props = nodeList->item(0)->getChildNodes();
	
	for (unsigned int i = 0; i < props->getLength(); ++i) {
	    DOMElement *elem = (DOMElement *) props->item (i);
	    std::string str = XMLString::transcode(elem->getNodeName());
	    
	    if (str == "simpleref") {
		InstantiationProperty *i_prop = parseSimpleRef (elem);
		properties.push_back(i_prop);

	    } else if (str == "simplesequenceref") {
		InstantiationProperty *i_prop = parseSimpleSequenceRef (elem);
		properties.push_back(i_prop);
	    }
	}
	
    }
}


InstantiationProperty* ComponentInstantiation::parseSimpleRef(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("refid");
    const XMLCh *_propId = _elem->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    tmpXMLStr = XMLString::transcode("value");
    const XMLCh *_propVal =    _elem->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    char* tmpStr1 = XMLString::transcode(_propId);
    char* tmpStr2 = XMLString::transcode(_propVal);
    InstantiationProperty* property = new InstantiationProperty(tmpStr1,tmpStr2);

    delete []tmpStr1;
    delete []tmpStr2;

    return property;
}

InstantiationProperty* ComponentInstantiation::parseSimpleSequenceRef(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("refid");
    const XMLCh *propId = _elem->getAttribute(tmpXMLStr);

    InstantiationProperty* property = new InstantiationProperty(XMLString::transcode(propId));
    XMLString::release(&tmpXMLStr);

    tmpXMLStr = XMLString::transcode("value");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    for (unsigned int i = 0; i < nodeList->getLength(); ++i) {
	DOMElement *e = (DOMElement *) nodeList->item(i);

	property->setValue(getTextNode(e));
    }

    return property;
}


char* ComponentInstantiation::getTextNode(DOMElement * _elem)
{
    DOMNodeList *nodeList = _elem->getChildNodes ();

    if (nodeList->getLength () == 0)
    {
	char *str = new char[strlen("Not Specified") + 1];
        strcpy(str, "Not Specified");
	return str;
    }
    else return XMLString::transcode (nodeList->item (0)->getNodeValue ());
}

const char* ComponentInstantiation::getID()
{
    return instantiationId.c_str();
}


const char* ComponentInstantiation::getUsageName()
{
    return usageName.c_str();
}


std::vector <InstantiationProperty*>* ComponentInstantiation::getProperties()
{
    return &properties;
}
XMLCh* ComponentInstantiation::tmpXMLStr = NULL;
