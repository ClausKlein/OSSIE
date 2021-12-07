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

#ifndef SADCOMPONENTPLACEMENT_H
#define SADCOMPONENTPLACEMENT_H

#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/util/XMLString.hpp>

#include "ComponentPlacement.h"
#include "SADComponentInstantiation.h"

class OSSIEPARSER_API SADComponentPlacement:public ComponentPlacement
{
public:
    SADComponentPlacement(DOMElement*  _elem, XERCES_CPP_NAMESPACE::DOMDocument*  _doc);
    virtual ~SADComponentPlacement();

    char* toString();

    std::vector <SADComponentInstantiation*>* getSADInstantiations();
    SADComponentInstantiation* getSADInstantiationById(char* _id) const;

protected:
    std::vector <SADComponentInstantiation*> sadComp;
    void parseElement();
    void parseFileRef(DOMElement*  _elem);
    void extractFileRef(DOMElement*  _elem);
    void parseInstantiations(DOMElement*  _elem);

private:
    SADComponentPlacement(); // No default constructor
    SADComponentPlacement(SADComponentPlacement &); // No copy constructor


    static XMLCh* tmpXMLStr;
};
#endif
