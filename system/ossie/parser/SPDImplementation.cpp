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


#include "ossie/SPDImplementation.h"
#include "ossie/SPDParser.h"

#define mdel(x) if (x!=NULL) delete x, x=NULL;
#define sweetd(x) if (x!=NULL) delete []x, x=NULL;



SPDImplementation::SPDImplementation(DOMElement * _elem):
element(_elem)
{

	this->parseElement ();
}


SPDImplementation::~SPDImplementation ()
{

	for (unsigned int i=0; i<processorsName.size(); i++)
	{
		sweetd(processorsName[i]);
	}

	for (unsigned int i=0; i<usesDevice.size(); i++)
	{
		mdel(usesDevice[i]);
	}

}

void SPDImplementation::parseElement()
{
	this->parseID (element);
	this->parsePRFRef (element);
	this->parseCode (element);
	this->parseCompiler (element);
	this->parsePrgLanguage (element);
	this->parseHumanLanguage (element);
	this->parseRuntime (element);
	this->parseOperatingSystems (element);
	this->parseProcessors (element);
	this->parseSoftwareDependencies (element);
	this->parsePropertyDependencies (element);
	this->parseUsesDevices (element);
}


void SPDImplementation::parseID (DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("id");
	const XMLCh *_tmp = _elem->getAttribute(tmpXMLStr);
	sweetd(tmpXMLStr);
	implementationID = XMLString::transcode (_tmp);
}


void SPDImplementation::parsePRFRef(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("propertyfile");
	DOMNodeList *nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);
		tmpXMLStr = XMLString::transcode("localfile");
		nodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
		sweetd(tmpXMLStr);
		_tmpElement = (DOMElement *) nodeList->item (0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		PRFFile = XMLString::transcode(_tmp);
	}
}


void SPDImplementation::parseCode(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("code");
	DOMNodeList *nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);
	DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);

	tmpXMLStr = XMLString::transcode("type");
	const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
	sweetd(tmpXMLStr);

	char* str = XMLString::transcode (_tmp);
	setCodeType (str);
	XMLString::release(&str);

	tmpXMLStr = XMLString::transcode("localfile");
	nodeList = _tmpElement->getElementsByTagName (tmpXMLStr);
	sweetd(tmpXMLStr);
	_tmpElement = (DOMElement *) nodeList->item (0);

	tmpXMLStr = XMLString::transcode("name");
	const XMLCh *_tmp2 = _tmpElement->getAttribute (tmpXMLStr);
	sweetd(tmpXMLStr);
	codeFile = XMLString::transcode (_tmp2);

	tmpXMLStr = XMLString::transcode("entrypoint");
	nodeList = _elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	entryPoint = getTextNode ((DOMElement *) nodeList->item (0));
}


// \todo implement exception handling
void SPDImplementation::setCodeType(char *_ct)
{
    if (strcmp (_ct, "KernelModule") == 0)
	codeType = CF::LoadableDevice::KERNEL_MODULE;
    else if (strcmp (_ct, "SharedLibrary") == 0)
	codeType = CF::LoadableDevice::SHARED_LIBRARY;
    else if (strcmp (_ct, "Executable") == 0)
	codeType = CF::LoadableDevice::EXECUTABLE;
    else if (strcmp (_ct, "Driver") == 0)
	codeType = CF::LoadableDevice::DRIVER;
    else
	{
	    //String msg = "[SPDImplementation:setCodeType] wrong code type passed. ";
	    //msg += " Type received is '" + ct + "'";
	    //throw new SCA.CF.InvalidProfile(msg);
	}
}


void SPDImplementation::parseCompiler(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("compiler");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		compilerName = XMLString::transcode (_tmp);

		tmpXMLStr = XMLString::transcode("version");
		const XMLCh* _tmp1 = _tmpElement->getAttribute(tmpXMLStr);
		XMLString::release(&tmpXMLStr);
		compilerVersion = XMLString::transcode(_tmp1);
	}
}


void SPDImplementation::parsePrgLanguage(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("programminglanguage");
	DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		prgLanguageName = XMLString::transcode (_tmp);

		tmpXMLStr = XMLString::transcode("version");
		const XMLCh *_tmp1 = _tmpElement->getAttribute(tmpXMLStr);
		XMLString::release(&tmpXMLStr);
		prgLanguageVersion = XMLString::transcode (_tmp1);
	}
}


void SPDImplementation::parseHumanLanguage(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("humanLanguage");
	DOMNodeList *nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);

		tmpXMLStr=(XMLString::transcode("name"));
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		humanLanguageName = XMLString::transcode (_tmp);
	}
}


void SPDImplementation::parseRuntime(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("runtime");
	DOMNodeList *nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () != 0)
	{

		DOMElement *_tmpElement = (DOMElement *) nodeList->item (0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		runtimeName = XMLString::transcode (_tmp);

		tmpXMLStr = XMLString::transcode("version");
		const XMLCh *_tmp1 = _tmpElement->getAttribute(tmpXMLStr);
		XMLString::release(&tmpXMLStr);
		runtimeVersion = XMLString::transcode (_tmp1);
	}
}


void SPDImplementation::parseOperatingSystems (DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("os");
	DOMNodeList *nodeList = _elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	if (nodeList->getLength () > 0)
	{
//              osAttributes = new char*[lenofOS];

//              for(int i = 0; i < lenofOS; i++)
//                      osAttributes[i] = new char[2];

		DOMElement *_tmpElement;

		_tmpElement = (DOMElement *) nodeList->item (0);

		tmpXMLStr = XMLString::transcode("name");
		const XMLCh *_tmp = _tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		os.setOSName(XMLString::transcode (_tmp));

		tmpXMLStr = XMLString::transcode("version");
		const XMLCh *_tmp1 =_tmpElement->getAttribute(tmpXMLStr);
		sweetd(tmpXMLStr);
		os.setOSVersion(XMLString::transcode (_tmp1));
	}
}


void SPDImplementation::parseProcessors (DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("processor");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	int len = nodeList->getLength ();
	if (len > 0)
	{
		DOMElement *_tmpElement;
		const XMLCh *_tmp;

		for (int i = 0; i < len; i++)
		{
			_tmpElement = (DOMElement *) nodeList->item (i);

			tmpXMLStr = XMLString::transcode("name");
			_tmp = _tmpElement->getAttribute (tmpXMLStr);
			XMLString::release(&tmpXMLStr);

			char *str = XMLString::transcode (_tmp);
			processorsName.push_back (str);
		}
	}
}


void SPDImplementation::parseSoftwareDependencies(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("softpkgref");
	DOMNodeList* nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	DOMNodeList* _tmpNodeList;

	unsigned int lenofSoftDep = nodeList->getLength();

	if (lenofSoftDep > 0)
	{
	    std::cout << "Add code to parse SW dependencies" << std::endl;
///\todo Rewrite the parser SW dependencies code
#if 0
		DOMElement *_tmpElement;
		softDep = new char *[lenofSoftDep];


		{
		for (int i = 0; i < lenofSoftDep; i++) {
			_tmpElement = (DOMElement *) nodeList->item (i);
			tmpXMLStr = XMLString::transcode("localfile");
			_tmpNodeList = _tmpElement->getElementsByTagName(tmpXMLStr);
			sweetd(tmpXMLStr);
			_tmpElement = (DOMElement *) _tmpNodeList->item (0);

			tmpXMLStr = XMLString::transcode("name");

			// Because of this bug -TT
			softDep[SOFTWARE_SPD_NAME] = XMLString::transcode(_tmpElement->getAttribute(tmpXMLStr));
			sweetd(tmpXMLStr);

//                      _tmpElement = (DOMElement*) _tmpElement->getNextSibling();
			_tmpElement = (DOMElement *) _tmpNodeList->item (1);

			if (_tmpElement != NULL)
			{
				tmpXMLStr = XMLString::transcode("refid");
				const XMLCh *tmp2 = _tmpElement->getAttribute (XMLString::transcode ("refid"));
				softDep[SOFTWARE_IMPL_REF] = XMLString::transcode (tmp2);
			}
			else softDep[SOFTWARE_IMPL_REF] = NULL;
		} // for
		}

#endif
	}
}


void SPDImplementation::parsePropertyDependencies(DOMElement * _elem)
{
	std::vector <DOMNode*> _list;
	tmpXMLStr = XMLString::transcode("dependency");
	DOMNodeList *nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	unsigned int len;
	DOMElement *_tmpElement;

	for (unsigned int i = 0; i < nodeList->getLength (); i++)
	{
		tmpXMLStr = XMLString::transcode("propertyref");
		DOMNodeList *childNodeList =
		((DOMElement *) nodeList->item (i))->getElementsByTagName(tmpXMLStr);
		sweetd(tmpXMLStr);
		len = childNodeList->getLength();

		if (len > 0)
		{
			for (unsigned int i = 0; i < len; i++)
			_list.push_back (childNodeList->item (i));
		}
	}

	len = _list.size();

	const XMLCh *_tmp;
	const XMLCh *_tmp2;
	char *_id;
	char *_val;

	if (len > 0)
	{
		propDep.length (len);
		for (unsigned int i = 0; i < len; i++)
		{
			_tmpElement = (DOMElement *) _list[i];

			tmpXMLStr = XMLString::transcode("refid");
			_tmp = _tmpElement->getAttribute(tmpXMLStr);
			sweetd(tmpXMLStr);
			_id = XMLString::transcode (_tmp);

			propDep[i].id = CORBA::string_dup(_id);

			tmpXMLStr = XMLString::transcode("value");
			_tmp2 = _tmpElement->getAttribute(tmpXMLStr);
			_val = XMLString::transcode(_tmp2);

			propDep[i].value <<= _val;
		}
	}
}


void SPDImplementation::parseUsesDevices(DOMElement * _elem)
{
	tmpXMLStr = XMLString::transcode("usesdevice");
	DOMNodeList *nodeList =	_elem->getElementsByTagName(tmpXMLStr);
	sweetd(tmpXMLStr);

	int len = nodeList->getLength();

	int lenn;
	const XMLCh *_tmp;
	const XMLCh *_tmp2;
	char *_id, *_val;

	char* id;
	char* type;

	for (int i = 0; i < len; i++)
	{
		DOMElement *_tmpElement = (DOMElement *) nodeList->item (i);
		tmpXMLStr = XMLString::transcode("id");
		id = XMLString::transcode(_tmpElement->getAttribute(tmpXMLStr));
		sweetd(tmpXMLStr);

		tmpXMLStr = XMLString::transcode("type");
		type = XMLString::transcode (_tmpElement->getAttribute(tmpXMLStr));
		sweetd(tmpXMLStr);

		tmpXMLStr = XMLString::transcode("propertyref");
		DOMNodeList *childNodeList =_tmpElement->getElementsByTagName(tmpXMLStr);
		sweetd(tmpXMLStr);
		lenn = childNodeList->getLength();
		CF::Properties propRef;

		for (int j = 0; j < lenn; j++)
		{
			_tmpElement = (DOMElement *) childNodeList->item (j);

			tmpXMLStr = XMLString::transcode("refid");
			_tmp = _tmpElement->getAttribute(tmpXMLStr);
			sweetd(tmpXMLStr);
			_id = XMLString::transcode (_tmp);

			propRef[j].id = CORBA::string_dup (_id);

			tmpXMLStr = XMLString::transcode("value");
			_tmp2 = _tmpElement->getAttribute(tmpXMLStr);
			_val = XMLString::transcode(_tmp2);
			sweetd(tmpXMLStr);

			propRef[j].value <<= _val;
		}

		usesDevice.push_back(new SPDUsesDevice (id, type, propRef));
	}
}


char* SPDImplementation::getTextNode(DOMElement * _elem)
{
	DOMNodeList* nodeList = _elem->getChildNodes();

	if (nodeList->getLength() == 0)
	{
		char* astr = new char[strlen("Not Specified") +1];
		strcpy(astr,"Not Specified");
		return astr;
	}
	else return XMLString::transcode(nodeList->item (0)->getNodeValue());
}


const char* SPDImplementation::getID()
{
	return implementationID.c_str();
}


const char* SPDImplementation::getPRFFile()
{
	return PRFFile.c_str();
}


const char* SPDImplementation::getCodeFile()
{
	return codeFile.c_str();
}


const char* SPDImplementation::getEntryPoint()
{
	return entryPoint.c_str();
}


const char* SPDImplementation::getCompilerName()
{
	return compilerName.c_str();
}


const char* SPDImplementation::getCompilerVersion()
{
	return compilerVersion.c_str();
}


const char* SPDImplementation::getPrgLanguageName()
{
	return prgLanguageName.c_str();
}


const char* SPDImplementation::getPrgLanguageVersion()
{
	return prgLanguageVersion.c_str();
}


const char* SPDImplementation::getHumanLanguageName()
{
	return humanLanguageName.c_str();
}


const char* SPDImplementation::getRuntimeName()
{
	return runtimeName.c_str();
}


const char* SPDImplementation::getRuntimeVersion()
{
	return runtimeVersion.c_str();
}


OSAttributes  SPDImplementation::getOperatingSystem()
{
	return os;
}


char ** SPDImplementation::getSoftwareDependencies()
{
	return softDep;
}


std::vector <char*>
SPDImplementation::getProcessors() const
{
	return processorsName;
}


std::vector <SPDUsesDevice*>* SPDImplementation::getUsesDevices()
{
	return &usesDevice;
}


CF::Properties SPDImplementation::getPropertyDependencies() const
{
	return propDep;
}


CF::LoadableDevice::LoadType SPDImplementation::getCodeType () const
{
	return codeType;
}


int SPDImplementation::OS_NAME = 0;
int SPDImplementation::OS_VERSION = 1;
int SPDImplementation::SOFTWARE_SPD_NAME = 0;
int SPDImplementation::SOFTWARE_IMPL_REF = 1;

XMLCh* SPDImplementation::tmpXMLStr = NULL;
