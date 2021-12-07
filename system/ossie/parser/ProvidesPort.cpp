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

#include "ossie/ProvidesPort.h"

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;


ProvidesPort::ProvidesPort(DOMElement * element):
Port(element)
{
    this->parseElement();
}


ProvidesPort::ProvidesPort (const ProvidesPort & _pp)
{
    this->root=_pp.root;
    this->findBy = new FindBy (_pp.root);

    this->ifComponentInstantiationRef = _pp.ifComponentInstantiationRef;
    this->ifDeviceThatLoadedThisComponentRef =
    _pp.ifDeviceThatLoadedThisComponentRef;
    this->ifDeviceUsedByThisComponentRef = _pp.ifDeviceUsedByThisComponentRef;
    this->ifFindBy = _pp.ifFindBy;

    identifier = _pp.identifier;
}

ProvidesPort::~ProvidesPort()
{
}


void ProvidesPort::parseElement()
{
    Port::parseElement();
    parseID(root);
}

void ProvidesPort::parseID(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("providesidentifier");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    identifier = this->getTextNode ((DOMElement *) nodeList->item (0));
}

char* ProvidesPort::getTextNode(DOMElement * _node)
{
    DOMNodeList *nodeList = _node->getChildNodes ();

    if (nodeList->getLength () == 0)
    {
    	char* astr = new char[strlen("Not Specified") +1];
    	strcpy(astr, "Not Specified");
    	return astr;
    }
    else return XMLString::transcode (nodeList->item (0)->getNodeValue ());
}

const char* ProvidesPort::getID()
{
    return identifier.c_str();
}
XMLCh* ProvidesPort::tmpXMLStr = NULL;
