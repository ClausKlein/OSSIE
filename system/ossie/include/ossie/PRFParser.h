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

#ifndef PRFPARSER_H
#define PRFPARSER_H

#include "PRFProperty.h"


class OSSIEPARSER_API PRFParser
{
public:
    PRFParser(const char *_propertyFile);
    ~PRFParser();
    std::vector <PRFProperty *> *getProperties();
    std::vector <PRFProperty *> *getConfigureProperties();
    std::vector <PRFProperty *> *getCapacityProperties();
    std::vector <PRFProperty *> *getMatchingProperties();
    std::vector <PRFProperty *> *getExecParamProperties();
    std::vector <PRFProperty *> *getFactoryParamProperties();

protected:
    void parseFile();
    void parseSimple(DOMElement* _elem);
    void parseSimpleSequence(DOMElement* _elem);
    void parseStruct(DOMElement* _elem);
    void parseStructSequence(DOMElement* _elem);
    void addProperty(PRFProperty* _sp);

private:
    PRFParser(); // No default constructor
    PRFParser(PRFParser &); // No copying

    std::string propertyFile;

    XERCES_CPP_NAMESPACE::DOMDocument *doc;
    XercesDOMParser *parser;

    std::vector<PRFProperty *> configProperties;
    std::vector<PRFProperty *> capacityProperties;
    std::vector<PRFProperty *> matchingProperties;
    std::vector<PRFProperty *> execProperties;
    std::vector<PRFProperty *> factoryProperties;
    std::vector<PRFProperty *> allProperties;

    static XMLCh* tmpXMLStr;
};
#endif
