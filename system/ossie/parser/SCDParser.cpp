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

#include <string>
#include <iostream>

#include "ossie/SCDParser.h"
#include "ossie/parserErrorHandler.h"

using namespace std;

#define sweetd(x) if (x!=NULL) delete []x, x=NULL;
#define mdel(x) if (x!=NULL) delete x, x=NULL;

using namespace std;

SCDParser::SCDParser(const char *_SCDFile):
doc(NULL), parser(NULL)
{
    SCDFile = _SCDFile;

    parseFile();
}


SCDParser::~SCDParser ()
{
	if (parser!=NULL)
	{
		delete parser;
		XMLPlatformUtils::Terminate();
	}

}


// \todo implement exception handling parseFile()
void SCDParser::parseFile()
{
// Initialize the XML4C2 system
    try
    {
        XMLPlatformUtils::Initialize();
    }
    catch (const XMLException & toCatch)
    {
        cerr<<"Error during Xerces-c Initialization.\nException message:"<< toCatch.getMessage () << endl;
        return;
    }

	parser = new XercesDOMParser;
	// parser->setValidationScheme( Val_Always );
	parserErrorHandler *xmlErrorHandler = new parserErrorHandler();

	parser->setErrorHandler(xmlErrorHandler);
  
	string tstr = "./";
	tstr.append(SCDFile);

	const XMLCh *_tmp = XMLString::transcode (tstr.c_str());
	parser->parse(_tmp);
	doc = parser->getDocument();

	DOMElement *_root = doc->getDocumentElement();

	const XMLCh *theStr = _root->getNodeName();

	char *str = XMLString::transcode(theStr);

	if (strcmp (str, "softwarecomponent") != 0)
	{
		//throw wrong xml file passed
	}

	parseComponentType(_root);
	parsePRFRef(_root);
}


void SCDParser::parseComponentType(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("componenttype");
	DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);
		componentType = getTextNode (_tmpElement);
	}
}


void SCDParser::parsePRFRef(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("propertyfile");
	DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength() != 0)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item(0);
		tmpXMLStr = XMLString::transcode("localfile");
		nodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
		sweetd(tmpXMLStr);

		_tmpElement = (DOMElement *) nodeList->item(0);
		tmpXMLStr = XMLString::transcode("name");
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		PRFFile = XMLString::transcode (_tmp);
	}
}


bool SCDParser::isDevice()
{
    if (componentType == "device")
        return true;
    else
        return false;
}


bool SCDParser::isResource()
{
    if (componentType == "resource")
        return true;
    else
        return false;
}


bool SCDParser::isApplication()
{
    if (componentType == "application")
        return true;
    else
        return false;
}


bool SCDParser::isDomainManager()
{
    if (componentType == "domainmanager")
        return true;
    else
        return false;
}


bool SCDParser::isDeviceManager()
{
    if (componentType == "devicemanager")
        return true;
    else
        return false;
}


bool SCDParser::isService()
{
    if ((componentType == "logger") ||
        (componentType == "filemanager") ||
        (componentType == "filesystem"))
    {
        return true;
    }
    else
        return false;
}


bool SCDParser::isConfigurable()
{
    if ((componentType == "resource") ||
        (componentType == "application") ||
        (componentType == "devicemanager") ||
        (isDevice ()) || (isDomainManager ()))
    {
        return true;
    }
    else
        return false;
}


char* SCDParser::getTextNode(DOMElement * _elem)
{
	DOMNodeList *nodeList = _elem->getChildNodes ();

	if (nodeList->getLength () == 0)
	{
		const char* configStr = "NotSpecified";
		char* tmpStr = new char[strlen(configStr)+1];
		strcpy(tmpStr, configStr);

		return tmpStr;
	}
	else
	{
		return XMLString::transcode (nodeList->item (0)->getNodeValue ());
	}
}


const char* SCDParser::toString()
{
    string str;

    str = "ComponentType = ";
    str += getComponentType();
    str += "\nPropertyFile = ";
    str += getPRFFile();
    str += "\n";

    return str.c_str();
}


const char* SCDParser::getComponentType()
{
    return componentType.c_str();
}


const char* SCDParser::getPRFFile()
{
    return PRFFile.c_str();
}

// initialisation
XMLCh* SCDParser::tmpXMLStr = NULL;
