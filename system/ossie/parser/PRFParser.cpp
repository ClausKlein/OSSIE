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
#include <string>
#include <sstream>

#include "ossie/PRFParser.h"
#include "ossie/PRFSimpleProperty.h"
#include "ossie/PRFSimpleSequenceProperty.h"
#include "ossie/parserErrorHandler.h"

#define DELPTR(x) if (x!=NULL) delete x, x=NULL;
#define DELARRAY(x) if (x!=NULL) delete []x, x=NULL;

PRFParser::PRFParser(const char *_propertyFile):
doc(NULL)
{
    propertyFile = _propertyFile;
    if (propertyFile.length())
	parseFile();
}

PRFParser::~PRFParser()
{

    for (unsigned int i=0; i< allProperties.size(); i++) DELPTR(allProperties[i]);
}


void PRFParser::parseFile ()
{
// Initialize the XML4C2 system
    try
    {
        XMLPlatformUtils::Initialize ();
    }
    catch (const XMLException & toCatch)
    {
        std::cout << "Error during Xerces-c Initialization.\nException message:" << toCatch.getMessage () << std::endl;
        return;
    }

    parser = new XercesDOMParser;
    parserErrorHandler *xmlErrorHandler = new parserErrorHandler();

    parser->setErrorHandler(xmlErrorHandler);
 
    std::string tstr = "./";
    tstr.append(propertyFile);

    const XMLCh *_tmp = XMLString::transcode (tstr.c_str());
    parser->parse(_tmp);

    doc = parser->getDocument();

    if (!doc) {
      std::cout << "Property file not found .. ." << std::endl;
      std::string err = "Property file ";
      err.append(propertyFile);
      err.append(" not found.");
      throw CF::FileException(CF::CFENOENT, err.c_str());
    }

    DOMElement *_root = doc->getDocumentElement();

    if (!_root) {
      std::string err = "Property file dtd file not found.";
      throw CF::FileException(CF::CFENOENT, err.c_str());
    }

    char *str = XMLString::transcode (_root->getNodeName ());

    if (strcmp (str, "properties") != 0)
    {
        //throw wrong xml file passed
    }

    DOMNodeList* nodeList = _root->getChildNodes();

    for (unsigned int i = 0; i < nodeList->getLength (); i++)
    {
        DOMElement* tmpElement = (DOMElement *) nodeList->item (i);
        std::string str = XMLString::transcode(tmpElement->getNodeName ());

        if (str == "simple") addProperty (new PRFSimpleProperty(tmpElement));
	if (str == "simplesequence") addProperty (new PRFSimpleSequenceProperty(tmpElement));

    }

    for (unsigned int i = 0; i < configProperties.size(); i++)
	allProperties.push_back (configProperties[i]);

    for (unsigned int i = 0; i < capacityProperties.size (); i++)
	allProperties.push_back (capacityProperties[i]);

    for (unsigned int i = 0; i < matchingProperties.size (); i++)
	allProperties.push_back (matchingProperties[i]);

    for (unsigned int i = 0; i < execProperties.size (); i++)
	allProperties.push_back (execProperties[i]);

    for (unsigned int i = 0; i < factoryProperties.size (); i++)
	allProperties.push_back (factoryProperties[i]);

    XMLString::release(&str);  
    delete parser;
    XMLPlatformUtils::Terminate();
}


void PRFParser::addProperty(PRFProperty* _sp)
{

    if (_sp->isAllocation ())
    {
        if (_sp->isExternal ())
            capacityProperties.push_back (_sp);
        else
            matchingProperties.push_back (_sp);
    }
    else if (_sp->isConfigure ())
        configProperties.push_back (_sp);
    else if (_sp->isExecParam ())
        execProperties.push_back (_sp);
    else if (_sp->isFactoryParam ())
        factoryProperties.push_back (_sp);
        else delete _sp;    // this is unlikely --TTP
}


std::vector<PRFProperty *> *PRFParser::getProperties ()
{
    return &allProperties;  // i dont like this --TTP
}

/*
char* PRFParser::toString()
{
// FIXME PJB test conversion to iostreams

//  char tmp;
//char *str = new char[2 * MAX_PRF_BUF];
    ostringstream str;

    PRFProperty *simpleProperty;

    simpleProperty = getConfigureProperties ();

    if (simpleProperty->size () > 0)
    {
//    strcpy (str, "\n   CONFIGURATION Properties are:\n");
        str << "\n  CONFIGURATION Properties are:\n";
    }

    {
        for (unsigned int i = 0; i < simpleProperty->size (); i++)
        {
//      str = strcat (str, "\n   PRFSimpleProperty[");
// #ifndef LINUX            //FIXME PJB
// str = strcat (str, itoa (i, &tmp, 10));
// #endif
// str = strcat (str, "]");
// str = strcat (str, (*simpleProperty)[i]->getID ());
            str << "\n   PRFSimpleProperty[" << i << "]" << (*simpleProperty)[i]->getID();
        }
    }

    simpleProperty = getCapacityProperties ();

//  if (simpleProperty->size () > 0)
//    {
//      if (strlen (str) > 0)
//    str = strcat (str, "\n   ALLOCATION Properties are:\n");
//      else
//    strcpy (str, "\n   ALLOCATION Properties are:\n");
//    }

    str << "\n   ALLOCATION Properties are:\n";

    {
        for (unsigned int i = 0; i < simpleProperty->size (); i++)
        {
//      str = strcat (str, "\n   PRFSimpleProperty[");
//#ifndef LINUX            //FIXME PJB
//      str = strcat (str, itoa (i, &tmp, 10));
//#endif
//      str = strcat (str, "]");
//      str = strcat (str, (*simpleProperty)[i]->getID ());

            str << "\n   PRFSimpleProperty[" << i << "]" << (*simpleProperty)[i]->getID ();
        }
    }

    simpleProperty = getMatchingProperties ();

    if (simpleProperty->size () > 0)
    {
//      if (strlen (str) > 0)
//    str = strcat (str, "\n   Matching Properties are:\n");
//      else
//    strcpy (str, "\n   Matching Properties are:\n");

        str << "\n   Matching Properties are:\n";
    }

    {
        for (unsigned i = 0; i < simpleProperty->size (); i++)
        {
//      str = strcat (str, "\n   PRFSimpleProperty[");
//#ifndef LINUX            //FIXME PJB
//      str = strcat (str, itoa (i, &tmp, 10));
//#endif
//      str = strcat (str, "]");
//      str = strcat (str, (*simpleProperty)[i]->getID ());

            str << "\n   PRFSimpleProperty[" << i << "]" << (*simpleProperty)[i]->getID ();
        }
    }

    simpleProperty = getExecParamProperties ();

    if (simpleProperty->size () > 0)
    {
//      if (strlen (str) > 0)
//    str = strcat (str, "\n   EXECUTION Properties are:\n");
//      else
//    strcpy (str, "\n   EXECUTION Properties are:\n");

        str << "\n   EXECUTION Properties are:\n";
    }

    {
        for (unsigned int i = 0; i < simpleProperty->size (); i++)
        {
//      str = strcat (str, "\n   PRFSimpleProperty[");
//#ifndef LINUX            //FIXME PJB
//      str = strcat (str, itoa (i, &tmp, 10));
//#endif
//      str = strcat (str, "]");
//      str = strcat (str, (*simpleProperty)[i]->getID ());

            str << "\n   PRFSimpleProperty[" << i << "]" << (*simpleProperty)[i]->getID ();
        }
    }

    simpleProperty = getFactoryParamProperties ();

    if (simpleProperty->size () > 0)
    {
//      if (strlen (str) > 0)
//    str = strcat (str, "\n   FACTORY Properties are:\n");
//      else
//    strcpy (str, "\n   FACTORY Properties are:\n");

        str << "\n   FACTORY Properties are:\n";
    }

    {
        for (unsigned int i = 0; i < simpleProperty->size (); i++)
        {
//      str = strcat (str, "\n   PRFSimpleProperty[");
//#ifndef LINUX            // FIXME PJB
//      str = strcat (str, itoa (i, &tmp, 10));
//#endif
//      str = strcat (str, "]");
//      str = strcat (str, (*simpleProperty)[i]->getID ());

            str << "\n   PRFSimpleProperty[" << i << "]" << (*simpleProperty)[i]->getID ();
        }
    }

// Extract output string and convert to char*

    string s = str.str();
    char *sp = new char[s.length()+1];
    strcpy(sp, s.c_str());;

    return sp;
}
*/

std::vector <PRFProperty *> *PRFParser::getConfigureProperties()
{
    return &configProperties;
}


std::vector <PRFProperty *> *PRFParser::getCapacityProperties()
{
    return &capacityProperties;
}


std::vector <PRFProperty *> *PRFParser::getMatchingProperties()
{
    return &matchingProperties;
}


std::vector <PRFProperty *> *PRFParser::getExecParamProperties()
{
    return &execProperties;
}


std::vector <PRFProperty *> *PRFParser::getFactoryParamProperties()
{
    return &factoryProperties;
}

// initialisation
XMLCh* PRFParser::tmpXMLStr = NULL;
