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

#include <iostream>

#include "ossie/FindBy.h"
#define DELPTR(x) if (x!=NULL) delete []x, x=NULL;

FindBy::FindBy(DOMElement* element):
root(element),
ifFindByNamingService(false),
ifFindByStringifiedObjectRef(false),
ifFindByDomainFinder(false)
{
    this->parseElement();
}


FindBy::FindBy(const FindBy& _fb):
root(_fb.root),
ifFindByNamingService(false),
ifFindByStringifiedObjectRef(false),
ifFindByDomainFinder(false)
{
    findByNamingService = _fb.findByNamingService;
    findByStringifiedObjectRef = _fb.findByStringifiedObjectRef;
    findByDomainFinderType = _fb.findByDomainFinderType;
    findByDomainFinderName = _fb.findByDomainFinderName;

    ifFindByNamingService = _fb.ifFindByNamingService;
    ifFindByStringifiedObjectRef = _fb.ifFindByStringifiedObjectRef;
    ifFindByDomainFinder = _fb.ifFindByDomainFinder;
}

FindBy::~FindBy()
{
}


void FindBy::parseElement()
{
    this->parseFindByNamingService(root);
    if (!this->isFindByNamingService()) {
    	this->parseFindByStringifiedObjectRef (root);

    } else if (!this->isFindByStringifiedObjectRef()) {
	this->parseFindByDomainFinder (root);

    } else if (!this->isFindByDomainFinder ()) {
	std::cout << "Did not find method to locate port in FindBy.cpp" << std::endl;
	/// \todo implement exception throwing in  parseElement
	//throw an InvalidProfile here
    }

}


void FindBy::parseFindByDomainFinder(DOMElement* _elem)
{
    tmpXMLStr = XMLString::transcode("domainfinder");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
    	ifFindByDomainFinder = true;
    	DOMElement *elem = (DOMElement* ) nodeList->item (0);
    	tmpXMLStr = XMLString::transcode("type");
    	const XMLCh *finderType = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);
    	findByDomainFinderType = XMLString::transcode(finderType);
    
    	tmpXMLStr = XMLString::transcode("name");
    	const XMLCh *finderName = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);
    	findByDomainFinderName = XMLString::transcode(finderName);
    }
}

void FindBy::parseFindByNamingService(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("namingservice");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
    	ifFindByNamingService = true;
    	DOMElement *elem = (DOMElement *) nodeList->item (0);
    
    	tmpXMLStr = XMLString::transcode("name");
    	const XMLCh *svcName = elem->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);
    	findByNamingService = XMLString::transcode(svcName);
    }
}


void FindBy::parseFindByStringifiedObjectRef(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("stringifiedobjectref");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    {
    	ifFindByStringifiedObjectRef = true;
    	findByStringifiedObjectRef =
    	getTextNode((DOMElement *) nodeList->item (0));
    }
}


char* FindBy::getTextNode(DOMElement* _node)
{
    DOMNodeList *nodeList = _node->getChildNodes ();

    // returned char* must be "deletable" -TP
    if (nodeList->getLength () == 0)
    {
    	char* astr = new char[strlen("Not Specified") +1];
    	strcpy(astr,"Not Specified");
    	return astr;
    }
    else return XMLString::transcode( nodeList->item (0)->getNodeValue() );
}

const char* FindBy::getFindByDomainFinderName()
{
    return findByDomainFinderName.c_str();
}


const char* FindBy::getFindByDomainFinderType()
{
    return findByDomainFinderType.c_str();
}


const char* FindBy::getFindByNamingServiceName()
{
    return findByNamingService.c_str();
}


const char* FindBy::getFindByStringifiedObjectRef()
{
    return findByStringifiedObjectRef.c_str();
}


bool FindBy::isFindByDomainFinder()
{
    return ifFindByDomainFinder;
}


bool FindBy::isFindByNamingService()
{
    return ifFindByNamingService;
}


bool FindBy::isFindByStringifiedObjectRef()
{
    return ifFindByStringifiedObjectRef;
}
XMLCh* FindBy::tmpXMLStr = NULL;
