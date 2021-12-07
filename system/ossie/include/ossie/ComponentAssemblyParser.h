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

#ifndef COMPONENTASSEMBLYPARSER_H
#define COMPONENTASSEMBLYPARSER_H

#include <vector>
#include <string>

#include "ossie/Connection.h"

class OSSIEPARSER_API ComponentAssemblyParser
{
public:
    ComponentAssemblyParser(const char*);
    virtual ~ComponentAssemblyParser();

    std::vector <Connection*>* getConnections();
    const char* getFileName();
    const char* getID();
    const char* getName();

protected:
    std::string fileName;  // the file name for a given DCD or SAD Profile
    std::string id;        // the id of the root node
    std::string name;      // the name of the root node

    XERCES_CPP_NAMESPACE::DOMDocument* doc;
    std::vector <Connection*> connections;
    void parseIdAndName(DOMElement* _root);
    void parseConnections(DOMElement* _root);
    char* getTextNode(DOMElement* _root);
    //Just keeping a reference so we can delete it at the destructor
    XercesDOMParser* parser;

private:
    ComponentAssemblyParser(); // No default constructor
    ComponentAssemblyParser(const ComponentAssemblyParser&); // No Copying
    bool IF;

};
#endif
