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
on the architecture of the CRC's SCA Reference Implementation (SCARI)
see: http://www.crc.ca/en/html/rmsc/home/sdr/projects/scari

*********************************************************************************/

#include "ossie/ComponentSupportedInterface.h"
#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

/**default constructor
*/
ComponentSupportedInterface::ComponentSupportedInterface():
root(NULL), identifier(NULL),
componentInstantiationRefId(NULL),
ifComponentInstantiationRef(false),
ifFindBy(false),
theFindBy(NULL)
{}

/** default constructor
*/
ComponentSupportedInterface::ComponentSupportedInterface(DOMElement*_element):
root(_element), identifier(NULL),
componentInstantiationRefId(NULL),
ifComponentInstantiationRef(false),
ifFindBy(false),
theFindBy(NULL)
{
    this->parseElement();
}


ComponentSupportedInterface::
ComponentSupportedInterface(const ComponentSupportedInterface & _csi):
root(_csi.root), identifier(NULL),
componentInstantiationRefId(NULL),
ifComponentInstantiationRef(false),
ifFindBy(false),
theFindBy(NULL)
{

    this->identifier = new char[strlen (_csi.identifier) + 1];
    strcpy (identifier, _csi.identifier);

    this->componentInstantiationRefId =
    new char[strlen (_csi.componentInstantiationRefId) + 1];
    strcpy (componentInstantiationRefId, _csi.componentInstantiationRefId);

    this->ifComponentInstantiationRef = _csi.ifComponentInstantiationRef;
    this->ifFindBy = _csi.ifFindBy;

    if (_csi.theFindBy != NULL) this->theFindBy = new FindBy (_csi.root);
}


ComponentSupportedInterface::~ComponentSupportedInterface ()
{
    DELPTR(theFindBy);
    DELARRAY(componentInstantiationRefId);
    DELARRAY(identifier);
}


void ComponentSupportedInterface::parseElement()
{
    parseID(root);
    parseComponentInstantiationRef(root);
}


void ComponentSupportedInterface::parseID (DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("supportedidentifier");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
    	identifier = getTextNode((DOMElement *) nodeList->item (0));
    }
}

void ComponentSupportedInterface::parseComponentInstantiationRef
(DOMElement* _elem)
{
    tmpXMLStr = XMLString::transcode ("componentinstantiationref"); 
    DOMNodeList *nodeList =_elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    {
    	ifComponentInstantiationRef = true;
    	DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);

    	tmpXMLStr = XMLString::transcode("refid");
    	const XMLCh *_tmp =_tmpElement->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);
    	componentInstantiationRefId = XMLString::transcode (_tmp);
    }
}


char* ComponentSupportedInterface::getTextNode(DOMElement * _elem)
{
    DOMNodeList *nodeList = _elem->getChildNodes();

    if (nodeList->getLength () == 0)
    {
    	char* astr = new char[strlen("Not Specified") +1];
    	strcpy(astr,"Not Specified");
    	return astr;
    }
    else return XMLString::transcode(nodeList->item (0)->getNodeValue ());
}


bool ComponentSupportedInterface::isComponentInstantiationRef()
{
    return ifComponentInstantiationRef;
}


bool ComponentSupportedInterface::isFindBy()
{
    return ifFindBy;
}


char* ComponentSupportedInterface::getID() const
{
    return identifier;
}


char* ComponentSupportedInterface::getComponentInstantiationRefId() const
{
    return componentInstantiationRefId;
}


FindBy* ComponentSupportedInterface::getFindBy() const
{
    return theFindBy;
}
XMLCh* ComponentSupportedInterface::tmpXMLStr = NULL;
