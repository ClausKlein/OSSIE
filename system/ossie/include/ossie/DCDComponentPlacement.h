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

#ifndef DCDCOMPONENTPLACEMENT_H
#define DCDCOMPONENTPLACEMENT_H

#include <string>

#include "DMDParser.h"
#include "ComponentPlacement.h"
#include "DCDComponentInstantiation.h"

class OSSIEPARSER_API DCDComponentPlacement:public ComponentPlacement
{
public:
    DCDComponentPlacement(DOMElement*  _elem, XERCES_CPP_NAMESPACE::DOMDocument*  _doc);
    ~DCDComponentPlacement();

    const char* getDMDFile();
    const char* getDeployOnDeviceID();
    const char* getCompositePartOfDeviceID();
    const char* getDPDFile();
    
    const char* getFileRefId();
    const char* getInstantiationId();
    const char* getUsageName();

    bool isDeployOn();
    bool isCompositePartOf();
    bool isDomainManager();

protected:
    void parseElement();
    void extractFileRef(DOMElement*  _elem);
    void parseDeployOnDevice(DOMElement*  _elem);
    void parseCompositePartOfDevice(DOMElement*  _elem);
    void parseDPDFileName(DOMElement*  _elem);
    void parseInstantiations(DOMElement*  _elem);

private:
    DCDComponentPlacement(); // No default constructor
    DCDComponentPlacement(const DCDComponentPlacement & _dcdCP); // No copying

    bool ifDeployOn;
    bool ifCompositePartOf;
    bool ifDomainManager;
    std::string _instantiationId;
    std::string _usageName;

    std::string DMDFile;
    std::string deployOnDeviceID;
    std::string compositePartOfDeviceID;
    std::string DPDFile;

    static XMLCh* tmpXMLStr;
};
#endif
