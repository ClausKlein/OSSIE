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

#ifndef PRFSIMPLEPROPERTY_H
#define PRFSIMPLEPROPERTY_H

#include <vector>
#include <string>

#include "ossieparser.h"
#include "cf.h"
#include "ossie/PRFProperty.h"

#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/util/XMLString.hpp>

XERCES_CPP_NAMESPACE_USE;

class OSSIEPARSER_API PRFSimpleProperty : public PRFProperty
{
public:
    PRFSimpleProperty(DOMElement * _elem);
    virtual ~PRFSimpleProperty();

private:
    PRFSimpleProperty();
    PRFSimpleProperty(const PRFSimpleProperty &);

    void extract_strings_from_element(DOMElement *elem, std::vector<std::string> &values);

    DOMElement* root;

};
#endif
