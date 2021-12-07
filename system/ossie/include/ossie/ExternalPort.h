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

#ifndef EXTERNALPORT_H
#define EXTERNALPORT_H

#include <string>

#include "ossieparser.h"

#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/util/XMLString.hpp>

XERCES_CPP_NAMESPACE_USE
#define MAX_BUFFER  4096
class OSSIEPARSER_API ExternalPort
{
protected:
    DOMElement* root;
    std::string usesIdentifier;
    std::string providesIdentifier;
    std::string supportedIdentifier;
    std::string componentInstantiationRefId;

    bool ifUsesIdentifier;
    bool ifProvidesIdentifier;
    bool ifSupportedIdentifier;
    void parseElement();
    void parseUsesIdentifier(DOMElement * _elem);
    void parseProvidesIdentifier(DOMElement * _elem);
    void parseSupportedIdentifier(DOMElement * _elem);
    void parseComponentInstantiationRefId(DOMElement * _elem);

public:
    ExternalPort(DOMElement * _elem);
    ~ExternalPort();

    bool isUsesIdentifier();
    bool isProvidesIdentifier();
    bool isSupportedIdentifier();
    const char* getUsesIdentifier();
    const char* getProvidesIdentifier();
    const char* getSupportedIdentifier();
    const char* getComponentInstantiationRefId();
    char* getTextNode(DOMElement * _elem);
    char* toString();

private:
    ExternalPort(); // No default constructor
    ExternalPort(const ExternalPort & _EP); // No copying

    static XMLCh* tmpXMLStr;
};
#endif
