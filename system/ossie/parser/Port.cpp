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
// last updated: 03/11/05
// coder: tuan pham
// optimise constructors and fix transcode leaks

#include <iostream>

#ifdef HAVE_STRING_H
#include <string.h>
#endif

#include "ossie/Port.h"

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

///\todo Figure out why this is used because it probably does not work
Port::Port():
root(NULL), findBy(NULL),
ifComponentInstantiationRef(false),
ifDeviceThatLoadedThisComponentRef(false),
ifDeviceUsedByThisComponentRef(false),
ifFindBy(false)
{}

Port::Port (DOMElement* element):
root(element), findBy(NULL),
ifComponentInstantiationRef(false),
ifDeviceThatLoadedThisComponentRef(false),
ifDeviceUsedByThisComponentRef(false),
ifFindBy(false)
{
    this->parseElement();
}

// copy constructor
// deep copy
Port::Port (const Port &aPort):
root(aPort.root), findBy(NULL),
ifComponentInstantiationRef(aPort.ifComponentInstantiationRef),
ifDeviceThatLoadedThisComponentRef(aPort.ifDeviceThatLoadedThisComponentRef),
ifDeviceUsedByThisComponentRef(aPort.ifDeviceUsedByThisComponentRef),
ifFindBy(aPort.ifFindBy)
{
    std::cout << "In Port copy constructor" << std::endl;

    this->findBy = new FindBy (aPort.root);

    componentInstantiationRefId = aPort.componentInstantiationRefId;

    deviceThatLoadedThisComponentRefId =aPort.deviceThatLoadedThisComponentRefId;

    deviceUsedByThisComponentRefId = aPort.deviceUsedByThisComponentRefId;

    deviceUsedByThisComponentRefUsesRefId = aPort.deviceUsedByThisComponentRefUsesRefId;
}


Port::~Port()
{
//    it is safer to let the parser
// or whoever passes the DOMElement calls release() --Tuan
//    root->release();
    
    DELPTR(findBy);
}


void Port::parseElement()
{
    parsePort(root);
}


// \todo implement exception handling for parsePort
void Port::parsePort (DOMElement * _elem)
{
    parseComponentInstantiationRef (_elem);

    if (!ifComponentInstantiationRef) {
        parseDeviceThatLoadedThisComponentRef (_elem);

	if (!ifDeviceThatLoadedThisComponentRef) {
	    parseDeviceUsedByThisComponentRef (_elem);

 
	    if (!ifDeviceUsedByThisComponentRef) {
		parseFindBy (_elem);

		if (!ifFindBy) {
		    std::cout << "Invalid connection type" << std::endl;
		    ///\todo Throw exception
		    // string msg = "[Port:parsePort] Invalid XML port";
		    // throw new InvalidProfile( msg );
		}
	    }
	}
    }
}


void Port::parseComponentInstantiationRef(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("componentinstantiationref");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
        DOMElement *elem = (DOMElement *) nodeList->item(0);

        tmpXMLStr = XMLString::transcode("refid");
        const XMLCh *refId = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);

        this->componentInstantiationRefId = XMLString::transcode(refId);
        this->ifComponentInstantiationRef = true;
    }
}


void Port::parseDeviceThatLoadedThisComponentRef (DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("devicethatloadedthiscomponentref");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    {
        DOMElement *elem = (DOMElement*) nodeList->item (0);

        tmpXMLStr = XMLString::transcode("refid");
        const XMLCh* refId = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);

        this->deviceThatLoadedThisComponentRefId = XMLString::transcode(refId);
        this->ifDeviceThatLoadedThisComponentRef = true;
    }
}


void Port::parseFindBy(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("findby");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    {
        DOMElement *elem = (DOMElement *) nodeList->item (0);

        this->findBy = new FindBy(elem);
        this->ifFindBy = true;
    }
}


void Port::parseDeviceUsedByThisComponentRef(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("deviceusedbythiscomponentref");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
        DOMElement* elem = (DOMElement*) nodeList->item(0);

        tmpXMLStr = XMLString::transcode("refid");
        const XMLCh *refId = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);
        tmpXMLStr = XMLString::transcode("usesrefid");
        const XMLCh *refUsesId = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);

        this->deviceUsedByThisComponentRefId = XMLString::transcode(refId);
        this->deviceUsedByThisComponentRefUsesRefId =XMLString::transcode(refUsesId);
        this->ifDeviceUsedByThisComponentRef = true;
    }
}

XMLCh* Port::tmpXMLStr = NULL;
