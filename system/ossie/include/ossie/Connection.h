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

#ifndef CONNECTION_H
#define CONNECTION_H

#include "UsesPort.h"
#include "ProvidesPort.h"
#include "ComponentSupportedInterface.h"

class OSSIEPARSER_API Connection
{
public:
    Connection(DOMElement* root);
    Connection(const Connection & _conn); /// \todo Figure out if we really need to use this in the Domain Manager
    ~Connection();

     char*getID() const;
     FindBy* getFindBy() const;
     UsesPort* getUsesPort() const;
     ProvidesPort* getProvidesPort() const;
     ComponentSupportedInterface*getComponentSupportedInterface() const;
     bool isComponentSupportedInterface();
     bool isFindBy();
     bool isProvidesPort();

protected:
    DOMElement* element;
    char* connectionId;
    FindBy* findBy;
    UsesPort* usesPort;
    ProvidesPort* providesPort;
    ComponentSupportedInterface* componentSupportedInterface;
    bool ifUsesPort;
    bool ifProvidesPort;
    bool ifComponentSupportedInterface;
    bool ifFindBy;
    void parseElement();
    void parseID(DOMElement* elem);
    void parseFindBy(DOMElement* elem);
    void parseUsesPort(DOMElement* elem);
    void parseProvidesPort(DOMElement* elem);
    void parseComponentSupportedInterface(DOMElement* elem);

private:
    Connection(); // No default constructor

    static XMLCh* tmpXMLStr;
};
#endif
