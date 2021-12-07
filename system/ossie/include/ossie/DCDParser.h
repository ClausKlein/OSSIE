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

#ifndef DCDPARSER_H
#define DCDPARSER_H

#include <string>
#include <vector>

#include "ossieparser.h"

#include "ComponentAssemblyParser.h"
#include "DCDComponentPlacement.h"

#define MAX_DCD_BUF 255

class OSSIEPARSER_API componentFile
{
 public:
    componentFile(const char *id, const char *fileName);
    // Default copy constructor and destructor will work

    const char* fileName();
    const char* id();
 
 private:
    std::string _fileName;
    std::string _id;
};


class OSSIEPARSER_API componentPlacement
{
 public:
    componentPlacement(const char *refid, const char *id, const char* usageName);
    
    const char *refId();
    const char *id();
    const char *usageName();

 private:
    std::string _refId;
    std::string _id;
    std::string _usageName;
};




class OSSIEPARSER_API DCDParser:public ComponentAssemblyParser
{
public:
    DCDParser(const char* _DCDFile);
    virtual ~DCDParser();

    const char* getDCDFilename();
    const char* getDeviceManagerSoftPkg();
    const char* getDomainManagerName();
    const char* getDomainManagerIOR();
    
    DCDComponentPlacement* getDomainManagerComponent() const;

    std::vector <DCDComponentPlacement*>* getDeployOnComponents();
    std::vector <componentFile> getComponentFiles();
    std::vector <componentPlacement> getComponentPlacements();

    const char *getFileNameFromRefId(const char *refid);
    char* toString();

protected:
    std::string deviceManagerSoftPkg;
    std::string domainManagerName;
    std::string domainManagerIOR;
    
    DCDComponentPlacement* domainManagerComponent;
    std::vector <DCDComponentPlacement*> deployOnComponents;

    void initializeDCD();
    void parseFile();
    void parseDeviceManagerSoftPkg(DOMElement*  _elem);
    void parseComponentPlacement(DOMElement*  _elem);
    void parseLocalComponents(DOMElement*  _elem);
    void parseDomainManager(DOMElement*  _elem);

private:
    DCDParser(); // No default constructor
    DCDParser(const DCDParser & _dcdP); // Don't allow copying
    static XMLCh* tmpXMLStr;

    std::vector<componentFile> componentFiles;
    std::vector<componentPlacement> componentPlacements;
};
#endif
