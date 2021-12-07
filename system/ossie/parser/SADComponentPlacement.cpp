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

#include "ossie/SADComponentPlacement.h"

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

SADComponentPlacement::SADComponentPlacement(DOMElement*  _elem, DOMDocument*  _doc) : ComponentPlacement(_elem, _doc)
{
    this->parseElement();

    for(unsigned int i = 0; i < instantiations.size(); i++)
    sadComp.push_back((SADComponentInstantiation* ) instantiations[i]);
}


SADComponentPlacement::~SADComponentPlacement()
{
//    for (unsigned int i=0; i<sadComp.)
    for (unsigned int i=0; i < instantiations.size(); i++)
    {
        DELPTR(instantiations[i]);
    }
}

void SADComponentPlacement::parseElement()
{
    this->parseFileRef(root);
    this->parseInstantiations(root);
}


// \todo implement exception handling for parserFileRef
void SADComponentPlacement::parseFileRef(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("componentfileref");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    DOMElement* elem =(DOMElement* ) nodeList->item(0);

    tmpXMLStr = XMLString::transcode("refid");
    const XMLCh* refId = elem->getAttribute(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    elem = doc->getElementById(refId);

    if(elem == NULL)
    {
//Invalid Profile
	std::cout << "Invalid profile in SADComponentPlacement" << std::endl;
    }

    this->extractFileRef(elem);
}


// \todo implement exception handling for extractFileRef
void SADComponentPlacement::extractFileRef(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("type");
    const XMLCh* _tmp = _elem->getAttribute(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    char* fileType = XMLString::transcode(_tmp);

    tmpXMLStr = XMLString::transcode("localfile");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    _elem =(DOMElement* ) nodeList->item(0);

    const XMLCh* _tmp1 = _elem->getAttribute(XMLString::transcode("name"));
    SPDFile = XMLString::transcode(_tmp1);    // SPDFile is in ComponentPlacement base class

    delete []fileType;
}


void SADComponentPlacement::parseInstantiations(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("componentinstantiation");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if(nodeList->getLength() > 0)
    {
        DOMElement* tmpElement;
        for(unsigned int i = 0; i < nodeList->getLength(); i++)
        {
            tmpElement =(DOMElement* ) nodeList->item(i);
            SADComponentInstantiation* SADInstance =
            new SADComponentInstantiation(tmpElement);
            instantiations.push_back((ComponentInstantiation* ) SADInstance);
        }
    }
}


std::vector <SADComponentInstantiation*> *SADComponentPlacement::getSADInstantiations()
{
    return &sadComp;
}


SADComponentInstantiation* SADComponentPlacement::getSADInstantiationById(char* _id) const
{
    for(unsigned int i = 0; i < instantiations.size(); i++)
    {
        if(strcmp(instantiations[i]->getID(), _id) == 0)
        return (SADComponentInstantiation* ) instantiations[i];
    }

    return NULL;
}


// \todo implement toString()
char* SADComponentPlacement::toString()
{
    return NULL;
}

XMLCh* SADComponentPlacement::tmpXMLStr = NULL;
