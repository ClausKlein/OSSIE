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

#include "ossie/PRFSimpleProperty.h"
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

PRFProperty::PRFProperty (DOMElement * _elem) : dataType(NULL), root(_elem) 
{
    this->dataType = new CF::DataType();
    this->parseElement();
}


PRFProperty::~PRFProperty()
{

    delete dataType;
}


void PRFProperty::parseElement()
{
    tmpXMLStr = XMLString::transcode("id");
    const XMLCh *_tmp = root->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    id = XMLString::transcode (_tmp);

    dataType->id = CORBA::string_dup(id.c_str());

    tmpXMLStr = XMLString::transcode("type");
    const XMLCh *_tmp1 = root->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    type = XMLString::transcode(_tmp1);

    tmpXMLStr = XMLString::transcode("name");
    const XMLCh *_tmp2 = root->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    name = XMLString::transcode(_tmp2);

    tmpXMLStr = XMLString::transcode("mode");
    const XMLCh *_tmp3 = root->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    mode = XMLString::transcode(_tmp3);

    parseKind(root);
    parseAction(root);
}

void PRFProperty::parseKind(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("kind");
    DOMNodeList *nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    char *str = new char[strlen("configure") + 1];
    strcpy(str, "configure");
    simpleKinds.push_back(str);
    
    //simpleKinds.push_back("configure");    // this causes seg fault if we delete it

    if (nodeList->getLength () != 0)
    {
        simpleKinds.pop_back();

        const XMLCh *_tmp;

        for (unsigned int i = 0; i < nodeList->getLength(); i++)
        {
            DOMElement *tmpElement = (DOMElement*) nodeList->item(i);
    
            tmpXMLStr = XMLString::transcode("kindtype");
            _tmp = tmpElement->getAttribute(tmpXMLStr);
            XMLString::release(&tmpXMLStr);
            simpleKinds.push_back(XMLString::transcode(_tmp));
        }
    }
}

void PRFProperty::parseAction(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("action");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    {
        DOMElement *tmpElement = (DOMElement*) nodeList->item (0);

        tmpXMLStr = XMLString::transcode("type");
        const XMLCh *_tmp = tmpElement->getAttribute(tmpXMLStr);
        XMLString::release(&tmpXMLStr);
        action = XMLString::transcode (_tmp);
    }
}

bool PRFProperty::isAllocation()
{
    for (unsigned int i = 0; i < simpleKinds.size (); i++)
    {
        if (simpleKinds[i] == "allocation")
            return true;
    }

    return false;
}

bool PRFProperty::isConfigure()
{
    for (unsigned int i = 0; i < simpleKinds.size (); i++)
    {
        if (simpleKinds[i] == "configure")
            return true;
    }

    return false;
}

bool PRFProperty::isTest()
{
    for (unsigned int i = 0; i < simpleKinds.size (); i++)
    {
        if (simpleKinds[i] == "test")
            return true;
    }

    return false;
}

bool PRFProperty::isExecParam()
{
    for (unsigned int i = 0; i < simpleKinds.size (); i++)
    {
        if (simpleKinds[i] == "execparam")
            return true;
    }

    return false;
}

bool PRFProperty::isFactoryParam()
{
    for (unsigned int i = 0; i < simpleKinds.size (); i++)
    {
        if (simpleKinds[i] == "factoryparam")
            return true;
    }

    return false;
}

char* PRFProperty::getTextNode(DOMElement * _elem)
{
    DOMNodeList *nodeList = _elem->getChildNodes ();

    if (nodeList->getLength () == 0)
    {
	char *str = new char[strlen("Not Specified") + 1];
	strcpy(str, "Not Specified");
        return str; // btw, it is "Not Specified" according the SCA specs
    }
    else
    {
        return XMLString::transcode(nodeList->item (0)->getNodeValue ());
    }
}

const char* PRFProperty::getID()
{
    return id.c_str();
}

const char* PRFProperty::getType()
{
    return type.c_str();
}

const char* PRFProperty::getName()
{
    return name.c_str();
}

const char* PRFProperty::getMode()
{
    return mode.c_str();
}

std::vector<std::string> PRFProperty::getValue()
{
    return value;
}

const char* PRFProperty::getAction()
{
    return action.c_str();
}

CF::DataType* PRFProperty::getDataType() const
{
    return dataType;
}

// \remarks this is not cool! returning a copy of pointers
std::vector <std::string> PRFProperty::getKinds()
{
    return simpleKinds;
}

bool PRFProperty::isBoolean()
{
    return (type == "boolean");
}

bool PRFProperty::isChar()
{
    return (type == "char");
}

bool PRFProperty::isDouble()
{
    return (type == "double");
}

bool PRFProperty::isFloat()
{
    return (type == "float");
}

bool PRFProperty::isShort()
{
    return (type == "short");
}

bool PRFProperty::isUShort()
{
    return (type == "ushort");
}

bool PRFProperty::isLong()
{
    return (type == "long");
}

bool PRFProperty::isObjref()
{
    return (type == "objref");
}

bool PRFProperty::isOctet()
{
    return (type == "octet");
}

bool PRFProperty::isString()
{
    return (type == "string");
}

bool PRFProperty::isULong()
{
    return (type == "ulong");
}

// by RADMOR
bool PRFProperty::isULongLong()
{
    return (type == "ulonglong");
}

bool PRFProperty::isUshort()
{
    return (type == "ushort");
}

bool PRFProperty::isReadOnly()
{
    return (type == "readonly");
}

bool PRFProperty::isReadWrite()
{
    return (type == "readwrite");
}

bool PRFProperty::isWriteOnly()
{
    return (type == "writeonly");
}

bool PRFProperty::isEqual()
{
    return (action == "eq");
}

bool PRFProperty::isNotEqual()
{
    return (action == "ne");
}


bool PRFProperty::isGreaterThan()
{
    return (action == "gt");
}

bool PRFProperty::isLessThan()
{
    return (action == "lt");
}

bool PRFProperty::isGreaterThanOrEqual()
{
    return (action == "ge");
}


bool PRFProperty::isLessThanOrEqual()
{
    return (action == "le");
}

bool PRFProperty::isExternal()
{
    return (action == "external");
}

// initialise tmpXMLStr
XMLCh* PRFProperty::tmpXMLStr = NULL;
