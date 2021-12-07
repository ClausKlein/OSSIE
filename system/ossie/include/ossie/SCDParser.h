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

#ifndef SCDPARSER_H
#define SCDPARSER_H

#include <string>

#include "ossieparser.h"

#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/util/XMLString.hpp>

  using namespace std;

XERCES_CPP_NAMESPACE_USE
#define MAX_BUFFER  4096
class OSSIEPARSER_API SCDParser
{
private:
  SCDParser();  // No default Constructor
  SCDParser(SCDParser &); // No copying

	XERCES_CPP_NAMESPACE::DOMDocument* doc;
	XercesDOMParser* parser;
	string componentType;
	string SCDFile;
	string PRFFile;
	char* getTextNode(DOMElement * _elem);

	static XMLCh* tmpXMLStr;

protected:
	void parseFile();
	void parseComponentType(DOMElement * _elem);
	void parsePRFRef(DOMElement * _elem);

public:
	SCDParser(const char *_SCDFile);
	~SCDParser();

	const char* getComponentType();
	const char* getPRFFile();
	bool isDevice();
	bool isResource();
	bool isApplication();
	bool isDomainManager();
	bool isDeviceManager();
	bool isService();
	bool isConfigurable();
	const char* toString();
};
#endif
