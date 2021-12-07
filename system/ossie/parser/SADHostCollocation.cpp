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

#include "ossie/SADHostCollocation.h"

SADHostCollocation::SADHostCollocation():
id(NULL), name(NULL)
{}


SADHostCollocation::SADHostCollocation(char *_id, char *_name,
std::vector <
SADComponentPlacement *
>_collocatedComponents)
{
    this->id = new char[strlen(_id) +1];
    strcpy(this->id, _id);
    this->name = new char[strlen(_name) +1];
    strcpy(this->name, _name);


    std::vector <SADComponentPlacement*>::iterator beg =
    _collocatedComponents.begin ();
    std::vector <SADComponentPlacement*>::iterator end =
    _collocatedComponents.end ();

    collocatedComponents.assign(beg, end);
}


SADHostCollocation::~SADHostCollocation ()
{
    if (id!=NULL) delete []id;
    if (name!=NULL) delete []name;
//    collocatedComponents.clear();    // we dont own collocatedComponents so dont delete it
// call .clear() is unnecessary because it just empties the vector
}


char* SADHostCollocation::getID() const
{
    return id;
}


char* SADHostCollocation::getName () const
{
    return name;
}


std::vector < SADComponentPlacement * >SADHostCollocation::getComponents () const
{
    return collocatedComponents;
}
