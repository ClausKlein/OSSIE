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
#include <string>

#include "ossie/SPDParser.h"
#include "ossie/SPDImplementation.h"
#include "ossie/parserErrorHandler.h"

#define mdel(x) if (x!=NULL) delete x, x=NULL;
#define sweetd(x) if (x!=NULL) delete []x, x=NULL;

using namespace std;


SPDParser::SPDParser(const char* _SPDFile):
doc(NULL), parser(NULL)
{
	SPDFile = _SPDFile;

	this->parseFile();
}

SPDParser::~SPDParser()
{

	unsigned int i;

	for (i=0; i<authors.size(); i++)
	{
		mdel(authors[i]);
	}

/*
	for (i=0; i<implementations.size(); i++)
	{
		mdel(implementations[i]);
	}
*/

	for (i=0; i<usesDevice.size(); i++)
	{
		mdel(usesDevice[i]);
	}

	authors.clear();
	implementations.clear();
	usesDevice.clear();

}


// \todo implement exception handling parseFile
// \todo implement some sort machanism to notify the SPDParser instance
// if XMLPlatformUtils::Initialize() fail so that it doesnt call
// XMLPlatformUtils::Terminate() in destructor
void SPDParser::parseFile()
{
// Initialize the XML4C2 system

	try
	{
		XMLPlatformUtils::Initialize();
	}
	catch(const XMLException & toCatch)
	{
		//cerr << "Error during Xerces-c Initialization.\n"
		//     << "  Exception message:"
		//     << toCatch.getMessage() << endl;
		return;
	}

	parser = new XercesDOMParser;
	parserErrorHandler *xmlErrorHandler = new parserErrorHandler();

	parser->setErrorHandler(xmlErrorHandler);
 
	string tstr="./";  //Delete this code when rel vs abs file path issue is solved
	tstr.append(SPDFile);

	tmpXMLStr = XMLString::transcode(tstr.c_str());
	parser->parse(tmpXMLStr);
	delete []tmpXMLStr;

	doc = parser->getDocument();

	DOMElement* _root = doc->getDocumentElement();

	char* str = XMLString::transcode(_root->getNodeName());

	if(strcmp(str, "softpkg") != 0)
	{
		//throw wrong xml file passed
	    cout << "Wrong xml file in SPD Parser for " << tstr  << " with root node name " << str << endl;
	}

	sweetd(str);
	this->parseSoftPkgAttributes(_root);
	this->parseSoftPkgTitle(_root);
	this->parseSoftPkgDescription(_root);
	this->parseSoftPkgAuthor(_root);
	this->parsePRFRef(_root);
	this->parseSCDRef(_root);
	this->parseImplementations(_root);
	this->parseUsesDevices(_root);

	// Explicit termination. Still needs some understanding. -TT 07/13/2005
	delete parser;
	XMLPlatformUtils::Terminate();
}


void SPDParser::parseSoftPkgAttributes(DOMElement*  _elem)
{
	tmpXMLStr = XMLString::transcode("id");
	const XMLCh* _tmp = _elem->getAttribute(tmpXMLStr);
	sweetd(tmpXMLStr);
	softPkgID = XMLString::transcode(_tmp);

	tmpXMLStr = XMLString::transcode("name");
	const XMLCh* _tmp1 = _elem->getAttribute(tmpXMLStr);
	sweetd(tmpXMLStr);
	softPkgName = XMLString::transcode(_tmp1);

//	cerr<<softPkgName<<endl;

	tmpXMLStr = XMLString::transcode("type");
	const XMLCh* _tmp2 = _elem->getAttribute(tmpXMLStr);
	sweetd(tmpXMLStr);
	softPkgType = XMLString::transcode(_tmp2);

	tmpXMLStr = XMLString::transcode("version");
	const XMLCh* _tmp3 = _elem->getAttribute(tmpXMLStr);
	sweetd(tmpXMLStr);
	softPkgVersion = XMLString::transcode(_tmp3);
}


void SPDParser::parseSoftPkgTitle(DOMElement*  _elem)
{
	tmpXMLStr = XMLString::transcode("title");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);
	if(nodeList->getLength() != 0)
	{
		DOMElement* _tmpElement =(DOMElement* ) nodeList->item(0);
		softPkgTitle = getTextNode(_tmpElement);
	}
}


void SPDParser::parseSoftPkgDescription(DOMElement*  _elem)
{
	tmpXMLStr = XMLString::transcode("description");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if(nodeList->getLength() != 0)
	{
		DOMElement* _tmpElement =(DOMElement* ) nodeList->item(0);
		softPkgDescription = getTextNode(_tmpElement);
	}
}


void SPDParser::parseSoftPkgAuthor(DOMElement*  _elem)
{
	tmpXMLStr = XMLString::transcode("author");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	int len = nodeList->getLength();
	DOMElement* _tmpElement;

	for(int i = 0; i < len; i++)
	{
		_tmpElement =(DOMElement* ) nodeList->item(i);
		SPDAuthor* spdAuthor = new SPDAuthor(_tmpElement);
	//	spdAuthor->parseElement();
		authors.push_back(spdAuthor);

	}
}


void SPDParser::parsePRFRef(DOMElement*  _elem)
{
	DOMElement* _tmpElement;
	tmpXMLStr = XMLString::transcode("propertyfile");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if(nodeList->getLength() != 0)
	{
		_tmpElement =(DOMElement* ) nodeList->item(0);
		tmpXMLStr = XMLString::transcode("localfile");
		nodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
		sweetd(tmpXMLStr);
		_tmpElement =(DOMElement* ) nodeList->item(0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh* _tmp =_tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		this->PRFFile = XMLString::transcode(_tmp);
	}
}


void SPDParser::parseSCDRef(DOMElement*  _elem)
{
	tmpXMLStr = XMLString::transcode("descriptor");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if(nodeList->getLength() != 0)
	{
		DOMElement* _tmpElement =(DOMElement* ) nodeList->item(0);
		tmpXMLStr = XMLString::transcode("localfile");
		nodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
		sweetd(tmpXMLStr);
		_tmpElement =(DOMElement* ) nodeList->item(0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh* _tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		this->SCDFile = XMLString::transcode(_tmp);
	}
}


void SPDParser::parseImplementations(DOMElement*  _elem)
{
	XMLCh* tmpXMLstr;
	tmpXMLstr = XMLString::transcode("implementation");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLstr);
	XMLString::release(&tmpXMLstr);

	int len = nodeList->getLength();
	DOMElement* _tmpElement;

	for(int i = 0; i < len; i++)
	{
		_tmpElement =(DOMElement*) nodeList->item(i);
		implementations.push_back(new SPDImplementation(_tmpElement));
	}
}


void SPDParser::parseUsesDevices(DOMElement*  _elem)
{
	tmpXMLStr = XMLString::transcode("usesdevice");
	DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if(nodeList->getLength() != 0)
	{
		DOMElement* _tmpElement;
		int len, j;
		const XMLCh* _tmp,* _tmp1,* val;
		CF::Properties propRef;
		char* _val;

		for(unsigned int i = 0; i < nodeList->getLength(); i++)
		{
			_tmpElement =(DOMElement* ) nodeList->item(i);
			tmpXMLStr = XMLString::transcode("id");
			_tmp = _tmpElement->getAttribute(tmpXMLStr);
			sweetd(tmpXMLStr);
			char* _id = XMLString::transcode(_tmp);

			tmpXMLStr = XMLString::transcode("type");
			_tmp1 = _tmpElement->getAttribute(tmpXMLStr);
			sweetd(tmpXMLStr);
			char* _type = XMLString::transcode(_tmp1);

			
			tmpXMLStr = XMLString::transcode("propertyref");
			DOMNodeList* childNodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
			len = childNodeList->getLength();

			propRef.length(len);

			for(j = 0; j < len; j++)
			{
				_tmpElement =(DOMElement* ) childNodeList->item(j);

				tmpXMLStr = XMLString::transcode("refid");
				_tmp = _tmpElement->getAttribute(tmpXMLStr);
				sweetd(tmpXMLStr);

				_id = XMLString::transcode(_tmp);

				propRef[j].id = CORBA::string_dup(_id);

				tmpXMLStr = XMLString::transcode("value");
				val = _tmpElement->getAttribute(tmpXMLStr);
				sweetd(tmpXMLStr);
				_val = XMLString::transcode(val);
				propRef[j].value <<= _val;
			}

			usesDevice.push_back(new SPDUsesDevice(_id, _type, propRef));
		}
	}
}


char* SPDParser::getTextNode(DOMElement*  _elem)
{
	DOMNodeList* nodeList = _elem->getChildNodes();

	if(nodeList->getLength() == 0)
	{
		char* astr = new char[strlen("Not Specified") +1];
		strcpy(astr,"Not Specified");
		return astr;
	}
	else return XMLString::transcode(nodeList->item(0)->getNodeValue());
}


bool SPDParser::isScaCompliant()
{
	if(softPkgType == SPDParser::SCA_COMPLIANT) return true;
	else return false;
}


bool SPDParser::isScaNonCompliant()
{
	if(softPkgType == SPDParser::SCA_NON_COMPLIANT) return true;
	else return false;
}


const char* SPDParser::getSoftPkgID()
{
	return softPkgID.c_str();
}


const char* SPDParser::getSoftPkgName()
{
	return softPkgName.c_str();
}


const char* SPDParser::getSoftPkgType()
{
	return softPkgType.c_str();
}


const char* SPDParser::getSoftPkgVersion()
{
	return softPkgVersion.c_str();
}


const char* SPDParser::getSoftPkgTitle()
{
	return softPkgTitle.c_str();
}


const char* SPDParser::getDescription()
{
	return softPkgDescription.c_str();
}


const char* SPDParser::getSPDFile()
{
	return SPDFile.c_str();
}


const char* SPDParser::getPRFFile()
{
	return PRFFile.c_str();
}


const char* SPDParser::getSCDFile()
{
	return SCDFile.c_str();
}


vector <SPDAuthor*>* SPDParser::getAuthors()
{
	return &authors;
}


vector <SPDImplementation*>* SPDParser::getImplementations()
{
	return &implementations;
}


vector <SPDUsesDevice*>* SPDParser::getUsesDevices()
{
	return &usesDevice;
}

XMLCh* SPDParser::tmpXMLStr = NULL;
char* SPDParser::SCA_COMPLIANT = "sca_compliant";
char* SPDParser::SCA_NON_COMPLIANT = "sca_non_compliant";
