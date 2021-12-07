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

#ifndef SPDPARSER_H
#define SPDPARSER_H

#include <string>

#include "SPDAuthor.h"
#include "SPDUsesDevice.h"

#include <vector>

using namespace std;

class OSSIEPARSER_API SPDImplementation;

class OSSIEPARSER_API SPDParser
{
protected:
	XERCES_CPP_NAMESPACE::DOMDocument*  doc;

	XercesDOMParser* parser;

	string SPDFile;
	string PRFFile;
	string SCDFile;
	string softPkgID;
	string softPkgName;
	string softPkgType;
	string softPkgVersion;
	string softPkgTitle;
	string softPkgDescription;

	vector <SPDAuthor*> authors;
	vector <SPDImplementation*> implementations;
	vector <SPDUsesDevice*> usesDevice;

	char* getTextNode(DOMElement*  _elem);

	void parseFile();
	void parseSoftPkgAttributes(DOMElement*  _elem);
	void parseSoftPkgTitle(DOMElement*  _elem);
	void parseSoftPkgDescription(DOMElement*  _elem);
	void parseSoftPkgAuthor(DOMElement*  _elem);
	void parsePRFRef(DOMElement*  _elem);
	void parseSCDRef(DOMElement*  _elem);
	void parseImplementations(DOMElement*  _elem);
	void parseUsesDevices(DOMElement*  _elem);

public:
	SPDParser(const char* _SPDFile);
	~SPDParser();

	bool isScaCompliant();
	bool isScaNonCompliant();

	const char* getSoftPkgID();
	const char* getSoftPkgName();
	const char* getSoftPkgType();
	const char* getSoftPkgVersion();
	const char* getSoftPkgTitle();
	const char* getDescription();
	const char* getSPDFile();
	const char* getPRFFile();
	const char* getSCDFile();

	vector <SPDAuthor*>* getAuthors();
	vector <SPDImplementation*>* getImplementations();
	vector <SPDUsesDevice*>* getUsesDevices();

	static char* SCA_COMPLIANT;
	static char* SCA_NON_COMPLIANT;
private:
	//	SPDParser();  //  No default constructor
	SPDParser(const SPDParser & _spdParser); // No copying
	static XMLCh* tmpXMLStr;
};
#endif
