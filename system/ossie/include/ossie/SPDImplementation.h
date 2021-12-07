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

#ifndef SPDIMPLEMENTATION_H
#define SPDIMPLEMENTATION_H

#include <vector>
#include <string>

#include "SPDUsesDevice.h"


class OSSIEPARSER_API SPDParser;

#define MAX_STR_LEN 128

class OSAttributes
{
 public:
  //  OSAttributes();
  //OSAttributes(OSAttributes &);
  //~OSAttributes();

  void setOSName(char * _name) { osName = _name; };
  void setOSVersion(char *_version) { osVersion = _version; };
  const char* getOSName() { return osName.c_str(); };
  const char* getOSVersion() { return osVersion.c_str(); };

 private:
  std::string osName;
  std::string osVersion;
};

class OSSIEPARSER_API SPDImplementation
{
private:
  SPDImplementation(); // No default constructor
  SPDImplementation(const SPDImplementation & _spdi); // No copying

	DOMElement* element;
	CF::Properties propDep;
	CF::LoadableDevice::LoadType codeType;

	std::string implementationID;
	std::string PRFFile;
	std::string codeFile;
	std::string entryPoint;
	std::string compilerName;
	std::string compilerVersion;
	std::string prgLanguageName;
	std::string prgLanguageVersion;
	std::string humanLanguageName;
	std::string runtimeVersion;
	std::string runtimeName;
	OSAttributes os;
	char ** softDep;

	std::vector < char* >processorsName;
	std::vector < SPDUsesDevice*  >usesDevice;

	char* getTextNode(DOMElement*  _elem);
	static XMLCh* tmpXMLStr;

protected:
	void parseElement();
	void parseID(DOMElement*  _elem);
	void parsePRFRef(DOMElement*  _elem);
	void parseCode(DOMElement*  _elem);
	void parseCompiler(DOMElement*  _elem);
	void parsePrgLanguage(DOMElement*  _elem);
	void parseHumanLanguage(DOMElement*  _elem);
	void parseRuntime(DOMElement*  _elem);
	void parseOperatingSystems(DOMElement*  _elem);
	void parseProcessors(DOMElement*  _elem);
	void parseSoftwareDependencies(DOMElement*  _elem);
	void parsePropertyDependencies(DOMElement*  _elem);
	void parseUsesDevices(DOMElement*  _elem);

public:
	SPDImplementation(DOMElement*  _elem);
	~SPDImplementation();

	const char* getID();
	const char* getPRFFile();
	const char* getCodeFile();
	const char* getEntryPoint();
	const char* getCompilerName();
	const char* getCompilerVersion();
	const char* getPrgLanguageName();
	const char* getPrgLanguageVersion();
	const char* getHumanLanguageName();
	const char* getRuntimeName();
	const char* getRuntimeVersion();
	OSAttributes getOperatingSystem();
	char ** getSoftwareDependencies();
	char* toString();


	void setCodeType(char* _ct);

	std::vector <SPDUsesDevice*> *getUsesDevices();
	std::vector <char*> getProcessors() const;
	CF::Properties getPropertyDependencies() const;
	CF::LoadableDevice::LoadType getCodeType() const;

	static int OS_NAME;
	static int OS_VERSION;
	static int SOFTWARE_SPD_NAME;
	static int SOFTWARE_IMPL_REF;
};
#endif
