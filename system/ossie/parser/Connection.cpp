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

#include "ossie/Connection.h"
#ifdef HAVE_STRING_H
#include <string.h>
#endif

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;    // this is sweet! --Tuan

Connection::Connection(DOMElement * root):
element(root), connectionId(NULL),
findBy(NULL), usesPort(NULL),
providesPort(NULL), componentSupportedInterface(NULL),
ifUsesPort(false), ifProvidesPort(false),
ifComponentSupportedInterface(false), ifFindBy(false)
{
    this->parseElement();
}

Connection::Connection (const Connection & _conn):
element(_conn.element), connectionId(NULL),
findBy(NULL), usesPort(NULL),
providesPort(NULL), componentSupportedInterface(NULL),
ifUsesPort(false), ifProvidesPort(_conn.ifProvidesPort),
ifComponentSupportedInterface(_conn.ifComponentSupportedInterface),
ifFindBy(_conn.ifFindBy)
{
    if (_conn.usesPort != NULL)
    {
        this->usesPort = new UsesPort (*(_conn.usesPort));
        this->ifUsesPort=true;
    }
    if (_conn.providesPort != NULL)
    this->providesPort = new ProvidesPort (*(_conn.providesPort));
    if (_conn.componentSupportedInterface != NULL)
    this->componentSupportedInterface = new ComponentSupportedInterface
    (*(_conn.componentSupportedInterface));

    if (_conn.findBy != NULL)
    this->findBy = new FindBy (*(_conn.findBy));

    connectionId = new char[strlen(_conn.connectionId) + 1];
    strcpy(connectionId, _conn.connectionId);

//    this->connectionId = new char[strlen (_conn.connectionId) + 1];
//    strcpy (connectionId, _conn.connectionId);
}

Connection::~Connection()
{
    DELARRAY(connectionId);
    DELPTR(findBy);
    DELPTR(usesPort);
    DELPTR(providesPort);
    DELPTR(componentSupportedInterface);
}


// \todo implement exception handling for parseElement
void Connection::parseElement()
{
    DOMNodeList *nodeList = element->getChildNodes();

    if (nodeList->getLength () < 2)
    {
	std::cout << "Invalid connection xml in SAD" << std::endl;
	///\todo throw exception
        //Invalid Profile Exception
        //Invalid XML -Connection must specify a destination component
    }

    parseID(element);
    parseUsesPort(element);
    parseProvidesPort(element);

    if (!isProvidesPort())
    {
        parseComponentSupportedInterface(element);

        if (!isComponentSupportedInterface())
        {
            DOMElement* _tmpElement = NULL;
            for (unsigned int i = 0; i < nodeList->getLength(); i++)
            {
                _tmpElement = (DOMElement *) nodeList->item (i);

                const XMLCh* _tagname = _tmpElement->getTagName();
                char* _name = XMLString::transcode(_tagname);

                if (strcmp (_name, "findby") == 0)
                {
                    delete []_name;
                    break;
                }
                delete []_name,_name=NULL;
            }

            parseFindBy (_tmpElement);

            if (!isFindBy())
            {
		std::cout << "Invalid connection xml 2" << std::endl;
		///\todo throw exception from here
                //Invalid Profile Exception
                //Invalid XML connection format
            }
        }
    }
}


void Connection::parseID(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("id");
    const XMLCh* _tmp = _elem->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    connectionId = XMLString::transcode (_tmp);
}


// \todo implement exception handling parseUsesPort
void Connection::parseUsesPort(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("usesport");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () == 0) return;
    //Throws exception InvalidProfile

    DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);
    DELARRAY(usesPort);
    usesPort = new UsesPort (_tmpElement);
    ifUsesPort = true;
}


// \todo implement exception handling parseProvidesPort
void Connection::parseProvidesPort(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("providesport");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () == 0) return;
    //Throws exception InvalidProfile

    DOMElement* _tmpElement = (DOMElement *) nodeList->item (0);
    DELARRAY(providesPort);
    providesPort = new ProvidesPort (_tmpElement);
    ifProvidesPort = true;
}


// \todo implement exception handling parseComponentSupportedInterface
void Connection::parseComponentSupportedInterface(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("componentsupportedinterface");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () == 0) return;
    //Throws exception InvalidProfile

    DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);
    componentSupportedInterface = new ComponentSupportedInterface (_tmpElement);
    ifComponentSupportedInterface = true;
}


// \todo implement exception handling parseFindBy
void Connection::parseFindBy(DOMElement * _elem)
{
    DELARRAY(findBy);
    findBy = new FindBy(_elem);
    ifFindBy = true;

//Throws exception InvalidProfile
}


char* Connection::getID() const
{
    return connectionId;
}


UsesPort* Connection::getUsesPort() const
{
    return usesPort;
}


ProvidesPort* Connection::getProvidesPort() const
{
    return providesPort;
}


ComponentSupportedInterface* Connection::getComponentSupportedInterface() const
{
    return componentSupportedInterface;
}


FindBy* Connection::getFindBy() const
{
    return findBy;
}


bool Connection::isProvidesPort()
{
    return ifProvidesPort;
}


bool Connection::isComponentSupportedInterface()
{
    return ifComponentSupportedInterface;
}


bool Connection::isFindBy()
{
    return ifFindBy;
}

XMLCh* Connection::tmpXMLStr=NULL;
