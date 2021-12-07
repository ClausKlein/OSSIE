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

#include <sstream>

#include "ossie/SADComponentInstantiation.h"

#define DELPTR(x) delete x, x=NULL;
#define DELARRAY(x) delete []x, x=NULL;

using namespace std;

SADComponentInstantiation::SADComponentInstantiation(DOMElement * _elem):
ComponentInstantiation(_elem),
ifResourceFactoryRef(false), ifNamingService(false)
{
    this->parseElement();
}


SADComponentInstantiation::~SADComponentInstantiation ()
{

    for (unsigned int i=0; i < factoryProperties.size(); i++)
    {
        DELPTR(factoryProperties[i]);
    }

}


void SADComponentInstantiation::parseElement()
{
    ComponentInstantiation::parseElement();
    parseFindComponent(root);
}


void SADComponentInstantiation::parseFindComponent(DOMElement * _elem)
{
    tmpXMLStr = XMLString::transcode("findcomponent");
    DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);

    if (nodeList->getLength() != 0)
    {
        DOMElement *tmpElement = (DOMElement *) nodeList->item (0);
        tmpXMLStr = XMLString::transcode("componentresourcefactoryref");
        nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
        DELARRAY(tmpXMLStr);

        if (nodeList->getLength () != 0)
        {
            ifResourceFactoryRef = true;

            tmpElement = (DOMElement *) nodeList->item (0);
            
            tmpXMLStr = XMLString::transcode("refid");
            const XMLCh *_tmp = tmpElement->getAttribute(tmpXMLStr);
            DELARRAY(tmpXMLStr);
            resourceFactoryRefId = XMLString::transcode (_tmp);
            tmpXMLStr = XMLString::transcode ("resourcefactoryproperties");
            nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
            DELARRAY(tmpXMLStr);

            if (nodeList->getLength() != 0)
            {
                tmpElement = (DOMElement *) nodeList->item (0);
                tmpXMLStr = XMLString::transcode("simpleref");
                nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
                DELARRAY(tmpXMLStr);

                for (unsigned int i = 0; i < nodeList->getLength(); i++)
                factoryProperties.push_back(parseSimpleRef((DOMElement *) nodeList->item (i)));
            }
        }
        else
        {
            tmpXMLStr = XMLString::transcode("namingservice");
            nodeList = tmpElement->getElementsByTagName(tmpXMLStr);
            DELARRAY(tmpXMLStr);

            if (nodeList->getLength() != 0)
            {
                ifNamingService = true;
                tmpElement = (DOMElement*) nodeList->item(0);
                tmpXMLStr = XMLString::transcode("name");
                const XMLCh *_tmp = tmpElement->getAttribute(tmpXMLStr);
                DELARRAY(tmpXMLStr);
                findByNamingServiceName = XMLString::transcode(_tmp);
            }
        }
    }
}



bool SADComponentInstantiation::isResourceFactoryRef()
{
    return ifResourceFactoryRef;
}


bool SADComponentInstantiation::isNamingService()
{
    return ifNamingService;
}


const char* SADComponentInstantiation::getResourceFactoryRefId()
{
    return resourceFactoryRefId.c_str();
}


const char* SADComponentInstantiation::getFindByNamingServiceName()
{
    return findByNamingServiceName.c_str();
}


std::vector <InstantiationProperty* >* SADComponentInstantiation::getFactoryProperties()
{
    return &factoryProperties;
}

XMLCh* SADComponentInstantiation::tmpXMLStr = NULL;
