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

#include <iostream>

#include <ossie/prop_helpers.h>
#include "ossie/PRFSimpleSequenceProperty.h"
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

PRFSimpleSequenceProperty::PRFSimpleSequenceProperty (DOMElement * _elem) : PRFProperty(_elem)
{
    std::cout << "Parsing simple sequence" << std::endl;

    extract_strings_from_element(_elem, value);

    // The sequences should be freed when the datatype goes away
    if (isBoolean()) {
	dataType->value <<= ossieSupport::strings_to_boolean_sequence(value);
    } else if (isChar()) {
	dataType->value <<= ossieSupport::strings_to_char_sequence(value);
    } else if (isDouble()) {
	dataType->value <<= ossieSupport::strings_to_double_sequence(value);
    } else if (isFloat()) {
	dataType->value <<= ossieSupport::strings_to_float_sequence(value);
    } else if (isShort()) {
	dataType->value <<= ossieSupport::strings_to_short_sequence(value);
    } else if (isLong()) {
	dataType->value <<= ossieSupport::strings_to_long_sequence(value);
    } else if (isOctet()) {
	dataType->value <<= ossieSupport::strings_to_octet_sequence(value);
    } else if (isUShort()) {
	dataType->value <<= ossieSupport::strings_to_unsigned_short_sequence(value);
    } else if (isULong()) {
	dataType->value <<= ossieSupport::strings_to_unsigned_long_sequence(value);
    } else if (isULongLong()) {
	dataType->value <<= ossieSupport::strings_to_unsigned_long_long_sequence(value); // by RADMOR
    } else if (isString()) {
	dataType->value <<= ossieSupport::strings_to_string_sequence(value);
	}
}


PRFSimpleSequenceProperty::~PRFSimpleSequenceProperty()
{

}

void PRFSimpleSequenceProperty::extract_strings_from_element(DOMElement *elem, std::vector<std::string> &value)
{
    XMLCh *tmpXMLStr = XMLString::transcode("value");
    DOMNodeList* nodeList = elem->getElementsByTagName(tmpXMLStr);
    XMLString::release(&tmpXMLStr);
    
    for (unsigned int i = 0; i < nodeList->getLength (); ++i) {
	DOMElement* tmpElement = (DOMElement*) nodeList->item(i);
	
	std::string str = getTextNode(tmpElement);
	value.push_back(str);
    }
}
