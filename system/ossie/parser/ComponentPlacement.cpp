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
#include "ossie/ComponentPlacement.h"

using namespace std;

#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

ComponentPlacement::ComponentPlacement (DOMElement * _element, DOMDocument * _doc) : doc(_doc), root(_element)
{
    if ((_element != NULL))
    {
            char *_tmp = XMLString::transcode(_element->getNodeName());
        if (strcmp (_tmp, "componentplacement") != 0)
            {
        //Invalid Profile
            cerr<<"Invalid profile cannot parse the \"componentplacement\" tag" << endl;
        }
        delete []_tmp;
    }
    this->parseElement();
}


/** default destructor
 * \remarks Since we dont really own the pointers doc and root,
 * we neither assign them to NULL nor delete them.  This is not
 * thread safe!
 */
ComponentPlacement::~ComponentPlacement()
{
    for (unsigned int i=0; i < instantiations.size(); i++)
    {
        delete instantiations[i];
    }
}



void ComponentPlacement::parseElement()
{
    this->parseFileRef(root);
}


// \todo implement exception handling for parserFileRef
void ComponentPlacement::parseFileRef (DOMElement * _elem)
{

    tmpXMLStr    = XMLString::transcode("componentfileref");
    DOMNodeList* nodeList    = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    DOMElement* elem    = (DOMElement*) nodeList->item (0);

    tmpXMLStr    = XMLString::transcode("refid");
    const XMLCh *refId = elem->getAttribute(tmpXMLStr);
    _fileRefId = XMLString::transcode(refId);
    DELARRAY(tmpXMLStr);

    elem = doc->getElementById(refId);

    if (elem == NULL)
    {
        //Invalid Profile
        cerr<<"Invalid profile cannot parse the refid in componentplacement"<<endl; 
    }
    else extractFileRef(elem);
}

ComponentInstantiation*
ComponentPlacement::getInstantiationById (const char *_id)
{
    for (unsigned int i = 0; i < instantiations.size(); i++)
    {
        if (strcmp (instantiations[i]->getID (), _id) == 0)
        return instantiations[i];
    }

    return NULL;
}


//\todo implement extractFileRef and exception handling
void ComponentPlacement::extractFileRef(DOMElement * _elem)
{
} //throws SCA.CF.InvalidProfile


const char* ComponentPlacement::getSPDFile()
{
    return SPDFile.c_str();
}


const char *ComponentPlacement::getFileRefId()
{
    return _fileRefId.c_str();
}

std::vector <ComponentInstantiation*>*
ComponentPlacement::getInstantiations()
{
    return &instantiations;
}
XMLCh* ComponentPlacement::tmpXMLStr = NULL;
