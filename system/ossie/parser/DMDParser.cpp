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
#include <string>

#include "ossie/DMDParser.h"
#include "ossie/parserErrorHandler.h"

#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

using namespace std;

DMDParser::DMDParser(const char* _DMDFile)
{
    DMDFile = _DMDFile;

    parseFile();
}


DMDParser::~DMDParser ()
{

}


void DMDParser::parseFile()
{
    // Initialize the XML4C2 system

    try
    {
        XMLPlatformUtils::Initialize ();
    } catch (const XMLException & toCatch)
    {
        cerr<<"Error during Xerces-c Initialization."<<endl
        <<"Exception message:" << toCatch.getMessage ()<<endl;
        return;
    }

    parser = new XercesDOMParser;
    parserErrorHandler *xmlErrorHandler = new parserErrorHandler();
    parser->setErrorHandler(xmlErrorHandler);

    //string tstr=".";
    //tstr.append(DMDFile);

    XMLCh* _tmp = XMLString::transcode(DMDFile.c_str());
    parser->parse(_tmp);
    XMLString::release(&_tmp);
    doc = parser->getDocument();

    DOMElement *_root = doc->getDocumentElement ();

    char* str = XMLString::transcode (_root->getNodeName ());

    if (strcmp (str, "domainmanagerconfiguration") != 0)
    {
        //throw wrong xml file passed
	cout << "Bad xml file in DMDParser " << DMDFile << " with str = " << str << endl; 
        return;
    }

    XMLString::release(&str);

    tmpXMLStr = XMLString::transcode ("id"); 
    const XMLCh *_id = _root->getAttribute (tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    tmpXMLStr = XMLString::transcode("name");
    const XMLCh *_name = _root->getAttribute (tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    _dmdId = XMLString::transcode (_id);
    _dmdName = XMLString::transcode (_name);
    parseDomainManagerSoftPkg (_root);

    // Explicit termination. Need to figure out why this
    // behaves differently from calling within the destructor. -TT
    delete parser;
    XMLPlatformUtils::Terminate();
}    


void DMDParser::parseDomainManagerSoftPkg(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("domainmanagersoftpkg");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);

    if (nodeList->getLength () != 0)
    {
        DOMElement *tmpElement = (DOMElement *) nodeList->item (0);
        tmpXMLStr = XMLString::transcode("localfile");
        nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        tmpElement = (DOMElement *) nodeList->item (0);

        tmpXMLStr = XMLString::transcode("name");
        const XMLCh *_tmp = tmpElement->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        domainManagerSoftPkg = XMLString::transcode (_tmp);
    }
}


const char* DMDParser::toString()
{
    char *str = new char[MAX_DMD_BUF];

    str = strcpy (str, "\n  domainManagerSoftPkg=");
    str = strcat (str, getDomainManagerSoftPkg ());

    return str;
}


const char* DMDParser::getDomainManagerSoftPkg()
{
    return domainManagerSoftPkg.c_str();
}

XMLCh* DMDParser::tmpXMLStr  = NULL;
