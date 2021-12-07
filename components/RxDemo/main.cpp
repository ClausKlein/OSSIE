/****************************************************************************

Copyright 2007 Virginia Polytechnic Institute and State University

This file is part of the OSSIE RxDemo.

OSSIE RxDemo is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE RxDemo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE RxDemo; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/

#include <iostream>
#include "ossie/ossieSupport.h"
#include "ossie/debug.h"

#include "RxDemo.h"

using namespace std;
using namespace standardInterfaces;  // For standard OSSIE interface classes


int main(int argc, char* argv[])
{
    ossieDebugLevel = 0;
    ossieSupport::ORB *orb = new ossieSupport::ORB;
    omni_mutex component_running_mutex;
    omni_condition *component_running = new omni_condition(&component_running_mutex);

    /*if (argc != 3) {
        cout << argv[0] << " <id> <usage name> " << endl;
        exit (-1);
    }*/

    char *uuid = argv[1];
    char *label = argv[2];

    cout << "Identifier - " << uuid << "  Label - " << label << endl;

    RxDemo_i* rxdemo_servant;
    CF::Resource_var rxdemo_var;

    // Create the rxdemo component servant and object reference

    rxdemo_servant = new RxDemo_i(uuid, component_running);
    rxdemo_var = rxdemo_servant->_this();

    orb->bind_object_to_name((CORBA::Object_ptr) rxdemo_var, label);

    // This bit is ORB specific
    // omniorb is threaded and the servants are running at this point
    // so we block on the condition
    // The releaseObject method clear the condition and the component exits

    component_running->wait();
    orb->unbind_name(label);
    orb->orb->shutdown(0);

}
