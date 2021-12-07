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

#include "ossie/SADParser.h"
#include <iostream>
using namespace std;

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

/** Default constructor
* default constructor with initialised SAD file
*/
SADParser::SADParser (const char* _SADFile):ComponentAssemblyParser(_SADFile)
{
    this->initializeSAD();
    this->parseFile();
}

/** Destructor
* Deep clean all vectors and pointers
*/
SADParser::~SADParser ()
{
// \remarks dont delete assemblyControllerInstantiation here, it causes seg fault! --Tuan
//    if (assemblyControllerInstantiation != NULL) delete assemblyControllerInstantiation;
    unsigned int i;
    //\remarks deep clean hostCollocations
    for (i=0; i < hostCollocations.size(); i++)
    {
        DELPTR(hostCollocations[i]);
    }

    //\remarks deep clean externalPorts
    for (i=0; i < externalPorts.size(); i++)
    {
        DELPTR(externalPorts[i]);
    }

    //\remarks deep clean components
    for (i=0; i<components.size(); i++)
    {
        DELPTR(components[i]);
    }
}


// \todo {implement exception handling}
void SADParser::initializeSAD()
{
    // use doc from base class
    const XMLCh* tmp = doc->getDocumentElement ()->getNodeName ();
    char* str = XMLString::transcode (tmp);
    if (strcmp (str, "softwareassembly") != 0)
    {
        //Invalid Profile;
        cerr<<"Cannot parse Software Assembly Descriptor xml file"<<endl;
    }

    delete []str;
    assemblyControllerInstantiation = NULL;
}

void SADParser::parseFile()
{
    // \remarks getDocumentElement returns a pointer
    // to a DOMElement for direct access.
    // Please do not delete _elem
    DOMElement* _elem = doc->getDocumentElement ();

    parseComponents(_elem);
    parseHostCollocation(_elem);
    parseAssemblyController(_elem);
    parseExternalPorts(_elem);
}

void SADParser::parseComponents(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("partitioning");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    DOMElement* _tmpElement = (DOMElement*) nodeList->item (0);
    components = parseComponentPlacement(_tmpElement);
}

void SADParser::parseHostCollocation(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("hostcollocation");
    DOMNodeList* nodeList = _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    
    DOMElement* element;
    char* id;
    char* name;
    
    std::vector <SADComponentPlacement* > collocatedComponents;

    const XMLCh* _id;
    const XMLCh* _name;

    for (unsigned int i = 0; i < nodeList->getLength (); i++)
    {
        element = (DOMElement* ) nodeList->item (i);

        _id = element->getAttribute (XMLString::transcode ("id"));    // dont delete _id and _name
        _name = element->getAttribute (XMLString::transcode ("name"));

        name = XMLString::transcode (_name);
        id = XMLString::transcode (_id);

        collocatedComponents = parseComponentPlacement (element);
        hostCollocations.push_back (new SADHostCollocation (id, name, collocatedComponents));
        DELARRAY(name);
        DELARRAY(id);
    }
}


std::vector <SADComponentPlacement*>
SADParser::parseComponentPlacement(DOMElement* _elem)
{
    DOMNodeList* nodeList = _elem->getChildNodes();
    DOMElement* _tmpElement;
    std::vector <SADComponentPlacement*> tmpComponents;

    for (unsigned int i = 0; i < nodeList->getLength (); i++)
    {
        _tmpElement = (DOMElement* ) nodeList->item (i);
        char* tmpStr = XMLString::transcode (_tmpElement->getTagName ());

        if (strcmp (tmpStr, "componentplacement") == 0)
            tmpComponents.push_back (new SADComponentPlacement (_tmpElement, doc));

        delete []tmpStr;
    }

    return tmpComponents;
}


// \todo investigate parseAssemblyController
void SADParser::parseAssemblyController (DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("assemblycontroller");
    DOMNodeList* nodeList = _elem->getElementsByTagName (tmpXMLStr);
    DOMElement* _tmpElement = (DOMElement* ) nodeList->item (0);
    DELARRAY(tmpXMLStr);

    if (_tmpElement != NULL)
    {
        tmpXMLStr = XMLString::transcode("componentinstantiationref");
        nodeList = _tmpElement->getElementsByTagName (tmpXMLStr);
        DELARRAY(tmpXMLStr);
        _tmpElement = (DOMElement* ) nodeList->item (0);

        tmpXMLStr = XMLString::transcode("refid");
        const XMLCh* _refid = _tmpElement->getAttribute(tmpXMLStr);
        DELARRAY(tmpXMLStr);
        char* controllerRefId = XMLString::transcode(_refid);
	assemblyControllerRefId = controllerRefId;

        for (unsigned int i = 0; i < components.size(); i++)
        {
            assemblyControllerInstantiation = components[i]->getSADInstantiationById(controllerRefId);

            if (assemblyControllerInstantiation != NULL)
            {
                delete []controllerRefId;
                return;
            }
        }

        std::vector <SADComponentPlacement*> sadComponents;

        if (assemblyControllerInstantiation == NULL)
        {
            for (unsigned int i = 0; i < hostCollocations.size (); i++)
            {
                sadComponents = hostCollocations[i]->getComponents ();
                for (unsigned int j = 0; j < sadComponents.size (); j++)
                {
                    assemblyControllerInstantiation =
                    sadComponents[j]->getSADInstantiationById(controllerRefId);
                    if (assemblyControllerInstantiation != NULL) return;
                } // for
            } // for
        } // if (assemblyController...)
    }
    else // _tmpElement == NULL
    {
    // this is a question ?? //
    //Invalid Profile
    }
}


void SADParser::parseExternalPorts(DOMElement*  _elem)
{
    tmpXMLStr = XMLString::transcode("externalports");
    DOMNodeList* nodeList =    _elem->getElementsByTagName(tmpXMLStr);
    DELARRAY(tmpXMLStr);
    DOMElement* _tmpElement;

    if (nodeList->getLength() != 0)
    {
        _tmpElement = (DOMElement* ) nodeList->item (0);
        tmpXMLStr = XMLString::transcode("port");
        nodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
        DELARRAY(tmpXMLStr);

        for (unsigned int i = 0; i < nodeList->getLength(); i++)
        {
            _tmpElement = (DOMElement* ) nodeList->item (i);
            externalPorts.push_back(new ExternalPort (_tmpElement));
        }
    }
}


const char* SADParser::getSADFilename()
{
    return fileName.c_str();
}

const char* SADParser::getAssemblyControllerRefId()
{
    return assemblyControllerRefId.c_str();
}

SADComponentInstantiation* SADParser::getAssemblyController()
{
    return assemblyControllerInstantiation;
}


std::vector <SADComponentPlacement*>*
SADParser::getComponents()
{
    return &components;
}


std::vector <SADHostCollocation*>*
SADParser::getHostCollocations()
{
    return &hostCollocations;
}


std::vector <ExternalPort*>*
SADParser::getExternalPorts()
{
    return &externalPorts;
}

XMLCh* SADParser::tmpXMLStr = NULL;
