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
#include <string>    // using string and string.h is not cool! --tuan
using namespace std;

#ifdef HAVE_STRING_H
#include <string.h>    // void* memcpy(void* des, void* src, size_t n)
#endif
    // it returns the pointer to des

#include "ossie/ComponentAssemblyParser.h"
#include "ossie/parserErrorHandler.h"

/** A definition
* This will ease the task of deleting
* a pointers and assigning it to NULL.
*/
#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

/** Default constructor with initialised profile name
*/
ComponentAssemblyParser::ComponentAssemblyParser(const char *_profileName):
doc(NULL), parser(NULL), IF(false)
{
    // Initialize the XML4C2 system
    try
    {
        XMLPlatformUtils::Initialize();
    }
    catch (const XMLException & toCatch)
    {
        cerr<< "Error during Xerces-c Initialization."<<endl
        <<"Exception message:"
        << toCatch.getMessage ()<<endl;
        return;
    }

    IF=true;
    fileName = _profileName;

    string tstr="./";        // C++ string
    tstr.append(_profileName);

    parser = new XercesDOMParser();
    parserErrorHandler *xmlErrorHandler = new parserErrorHandler();

    parser->setErrorHandler(xmlErrorHandler);
    parser->parse (tstr.c_str());
    
    // getDocument returns a pointer to the root document
    // this pointer is owned by the parser
    // So dont delete "doc"
    doc = parser->getDocument();
    parseIdAndName (doc->getDocumentElement ());
    parseConnections (doc->getDocumentElement ());
}


/** A destructor
* It does a deep clean of all memory allocations
* The pointers need to be deleted are
* fileName, id, name, parser.
* Vector needs to be cleaned is connections
* \Note: Pointer DOMDocument* "doc" is owned by the
* parser.
*/
ComponentAssemblyParser::~ComponentAssemblyParser ()
{

    if (IF)     // Initialization Flag
    {
        //doc->release();  // parser cleans itself
        delete parser;
        XMLPlatformUtils::Terminate();  // now it is safe to call Terminate
    }

// Application_impl.cpp in ossiecf uses these connections :-(
//    for (unsigned int i=0; i < connections.size(); i++)
//    {
//        DELPTR(connections[i]);
//    }
}


char* ComponentAssemblyParser::getTextNode(DOMElement* _root)
{
    DOMNodeList* nodeList = _root->getChildNodes();

    if (nodeList->getLength() == 0)
    {
        char* astr = (char *) new char[strlen("Not Specified") + 1];
	strcpy(astr, "Not Specified");
        return astr;
    }
    else return XMLString::transcode(nodeList->item(0)->getNodeValue());
}


void ComponentAssemblyParser::parseIdAndName(DOMElement * _root)
{

    XMLCh* tmpXMLStr;

    tmpXMLStr = XMLString::transcode("name");
    const XMLCh* _name = _root->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    tmpXMLStr = XMLString::transcode("id");
    const XMLCh* _id = _root->getAttribute(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    // \note XMLString::transcode() returns a pointer to
    // a buffer of chars and expects the caller to clean
    // it up

    name = XMLString::transcode (_name);
    id = XMLString::transcode (_id);
}


void ComponentAssemblyParser::parseConnections(DOMElement * _root)
{
    XMLCh* tmpXMLStr;

    tmpXMLStr = XMLString::transcode("connections");
    DOMNodeList* _connections = _root->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    
    // \remarks Dont do this because it is...leaky!
    // DOMNodeList *_connections =
    // _root->getElementsByTagName (XMLString::transcode ("connections"));

    if( _connections->getLength() > 0)
    {
        DOMElement* _connection = (DOMElement* ) _connections->item (0);

        tmpXMLStr = XMLString::transcode("connectinterface");
        DOMNodeList *_connectionsList = _connection->getElementsByTagName(tmpXMLStr);
        XMLString::release(&tmpXMLStr);

        for (unsigned int i = 0; i < _connectionsList->getLength (); i++)
        this->connections.push_back(new Connection ((DOMElement *)
        _connectionsList->item (i)));
    }
}

/**
 * @return a pointer to a list of Connection
 * i hate this! ~tp
*/
std::vector <Connection*>* ComponentAssemblyParser::getConnections()
{
    return &connections;
}

const char* ComponentAssemblyParser::getFileName()
{
    return fileName.c_str();
}

const char* ComponentAssemblyParser::getID()
{
    return id.c_str();
}

const char* ComponentAssemblyParser::getName()
{
    return name.c_str();
}
