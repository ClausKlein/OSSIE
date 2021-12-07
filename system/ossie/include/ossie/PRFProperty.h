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

#ifndef PRFPROPERTY_H
#define PRFPROPERTY_H

#include <vector>
#include <string>

#include "ossieparser.h"
#include "cf.h"

#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/util/XMLString.hpp>

XERCES_CPP_NAMESPACE_USE;

#define MAX_PRF_BUF 4096

class OSSIEPARSER_API PRFProperty
{
public:
    PRFProperty(DOMElement * _elem);
    virtual ~PRFProperty();

    bool isBoolean();
    bool isChar();
    bool isDouble();
    bool isFloat();
    bool isShort();
    bool isUShort();
    bool isLong();
    bool isObjref();
    bool isOctet();
    bool isString();
    bool isULong();
    bool isULongLong(); // by RADMOR
    bool isUshort();
    bool isReadOnly();
    bool isReadWrite();
    bool isWriteOnly();
    bool isAllocation();
    bool isConfigure();
    bool isTest();
    bool isExecParam();
    bool isFactoryParam();
    bool isEqual();
    bool isNotEqual();
    bool isGreaterThan();
    bool isLessThan();
    bool isGreaterThanOrEqual();
    bool isLessThanOrEqual();
    bool isExternal();

    const char* getPropType();
    const char* getID();
    const char* getType();
    const char* getName();
    const char* getMode();
    std::vector <std::string> getValue();
    const char* getAction();

    CF::DataType* getDataType() const;
    std::vector <std::string> getKinds();


protected:
    char* getTextNode(DOMElement * _elem);

    CF::DataType* dataType;
    std::vector<std::string> value;


private:
    PRFProperty();
    PRFProperty(const PRFProperty & _prfSimpleProp); // No copying

    void parseElement();
    void parseKind(DOMElement * _elem);
    void parseAction (DOMElement * _elem);

    DOMElement* root;

    std::string prop_type;
    std::string id;
    std::string type;
    std::string name;
    std::string mode;
    std::string action;
    std::vector <std::string> simpleKinds;

    static XMLCh*    tmpXMLStr;

};
#endif
