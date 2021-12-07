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

#include "ossie/UsesPort.h"

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

UsesPort::UsesPort(DOMElement * _root):
Port(_root)
{
    this->parseElement();
}


// copy constructor
UsesPort::UsesPort(const UsesPort & _up):
Port(_up.root),
identifier(NULL)
{
    this->root = _up.root;
    this->findBy = new FindBy (_up.root);

    this->ifComponentInstantiationRef = _up.ifComponentInstantiationRef;
    this->ifDeviceThatLoadedThisComponentRef =
    _up.ifDeviceThatLoadedThisComponentRef;
    this->ifDeviceUsedByThisComponentRef = _up.ifDeviceUsedByThisComponentRef;
    this->ifFindBy = _up.ifFindBy;

    identifier = _up.identifier;
}

UsesPort::~UsesPort()
{
}


void UsesPort::parseElement()
{
    Port::parseElement();    // call the base class first
    this->parseID(root);
}


void UsesPort::parseID(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("usesidentifier");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    identifier = this->getTextNode((DOMElement *) nodeList->item (0));
}


char* UsesPort::getTextNode(DOMElement * _node)
{
    DOMNodeList* nodeList = _node->getChildNodes();

    if (nodeList->getLength () == 0)
    {
        char* astr = new char[strlen("Not Specified") +1];
        strcpy(astr, "Not Specified");
        return astr;
    }
    else return XMLString::transcode(nodeList->item (0)->getNodeValue ());
}

const char* UsesPort::getID()
{
    return identifier.c_str();
}
XMLCh* UsesPort::tmpXMLStr = NULL;
