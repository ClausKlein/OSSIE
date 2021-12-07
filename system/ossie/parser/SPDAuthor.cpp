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
on the architecture of the CRC's SCA Reference Implementation (SCARI)
see: http://www.crc.ca/en/html/rmsc/home/sdr/projects/scari

*********************************************************************************/

#include "ossie/SPDAuthor.h"
#define mdel(x) if (x!=NULL) delete []x, x=NULL;

SPDAuthor::SPDAuthor():
authorElement(NULL),
authorCompany(NULL),
authorWebPage(NULL),
authorName(NULL)
{}


SPDAuthor::SPDAuthor(DOMElement* _elem):
authorElement(_elem),
authorCompany(NULL),
authorWebPage(NULL),
authorName(NULL)
{
	this->parseElement();
}


SPDAuthor::SPDAuthor (const SPDAuthor & _spda):
authorElement(_spda.authorElement),
authorCompany(NULL),
authorWebPage(NULL),
authorName(NULL)
{
	this->parseElement();
}


SPDAuthor::~SPDAuthor()
{
// \note dont delete DOMElement pointer, we dont own it
//	delete this->authorElement;
//	this->authorElement->release();
	mdel(authorCompany);
	mdel(authorWebPage);
	mdel(authorName);
}


char* SPDAuthor::getAuthorName() const
{
	return authorName;
}


char* SPDAuthor::getAuthorCompany() const
{
	return authorCompany;
}


char* SPDAuthor::getAuthorWebPage() const
{
	return authorWebPage;
}


void SPDAuthor::parseElement()
{
	parseSoftPkgAuthor(authorElement);
}


void SPDAuthor::parseSoftPkgAuthor (DOMElement * _authorElement)
{
	DOMNodeList* nodeList = _authorElement->getChildNodes();
	DOMNode* node;

	if (nodeList->getLength () != 0)
	{
		for (int i = 0; i < (int) nodeList->getLength (); i++)
		{
			node = nodeList->item(i);

			char *tmpXMLStr;
			if (node->getNodeType() == DOMNode::ELEMENT_NODE)
			{
				tmpXMLStr = XMLString::transcode (node->getNodeName ());
				if (strcmp(tmpXMLStr, "name") == 0)
				{
					authorName = getTextNode ((DOMElement *) node);
				}
				XMLString::release(&tmpXMLStr);
			}
			else if (node->getNodeType() == DOMNode::ELEMENT_NODE)
			{
				tmpXMLStr = XMLString::transcode (node->getNodeName ());
				if (strcmp(tmpXMLStr, "company") == 0)
				{
					authorCompany = getTextNode ((DOMElement *) node);
				}
				XMLString::release(&tmpXMLStr);
			}
			else if (node->getNodeType() == DOMNode::ELEMENT_NODE)
			{
				tmpXMLStr = XMLString::transcode (node->getNodeName ());
				if (strcmp(tmpXMLStr, "webpage") == 0)
				{
					authorWebPage = getTextNode ((DOMElement *) node);
				}
				XMLString::release(&tmpXMLStr);
			}
			else
			{
			}
/*
			if ((node->getNodeType () == DOMNode::ELEMENT_NODE) &&
				(strcmp (XMLString::transcode (node->getNodeName ()), "name") == 0))
			{
				authorName = getTextNode ((DOMElement *) node);
			}
			else if ((node->getNodeType () == DOMNode::ELEMENT_NODE) &&
				(strcmp(XMLString::transcode (node->getNodeName ()),
				"company") == 0))
			{
				authorCompany = getTextNode ((DOMElement *) node);
			}
	      		else if ((node->getNodeType () == DOMNode::ELEMENT_NODE) &&
				(strcmp(XMLString::transcode (node->getNodeName ()),
				"webpage") == 0))
			{
				authorWebPage = getTextNode ((DOMElement *) node);
			}
	   		else
			{
			}
*/
		}
	}
}


char* SPDAuthor::getTextNode(DOMElement * _elem)
{
	DOMNodeList *nodeList = _elem->getChildNodes();

	if (nodeList->getLength () == 0)
	{
		char* astr = new char[strlen("Not Specified") +1];	// dont worry, the compiler will optimize const string
		strcpy(astr, "Not Specified");
		return astr;
	}
	else return XMLString::transcode(nodeList->item (0)->getNodeValue());
}


char* SPDAuthor::toString()
{
	char* str = new char[MAX_SPD_BUF];

	if (authorName != NULL && strcmp (authorName, "") != 0)
	{
	str = strcpy (str, "\n AuthorName=");
	str = strcat (str, getAuthorName ());
	str = strcat (str, "\n AuthorCompany=");
	str = strcat (str, getAuthorCompany ());
	str = strcat (str, "\n AuthorWebPage=");
	str = strcat (str, getAuthorWebPage ());
	}
	else
	str = strcpy (str, "\n There are no author property ");

	return str;
}
