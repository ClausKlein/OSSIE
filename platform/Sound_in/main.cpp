/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE Sound_out Device.

OSSIE Sound_out Device is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE Sound_out Device is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE Sound_out Device; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


****************************************************************************/

#include <iostream>
#include "ossie/ossieSupport.h"

#include "soundCardCapture.h"

using namespace std;
using namespace standardInterfaces;  // For standard OSSIE interface classes


int main(int argc, char* argv[])

{
    ossieDebugLevel = 3;

    ossieSupport::ORB *orb = new ossieSupport::ORB;
    omni_mutex component_running_mutex;
    omni_condition *component_running = new omni_condition(&component_running_mutex);

    if (argc != 4) {
	cout << argv[0] << " <identifier> <usage name> <software profile>" << endl;
	exit (-1);
    }

    char *uuid = argv[1];
    char *label = argv[2];
    char *profile = argv[3]; 

    cout << "Identifier - " << uuid 
         << "  Label - " << label 
         << "  Profile - " << profile 
         << endl;

    SoundCardCapture_i* soundCardCapture_servant;
    CF::Device_var soundCardCapture_var;

    // Create the Sound Card Capture device servant and object reference

    soundCardCapture_servant = new SoundCardCapture_i(uuid, label, profile, component_running);
    soundCardCapture_var = soundCardCapture_servant->_this();

    string objName = "DomainName1/";
    objName += label;

    orb->bind_object_to_name((CORBA::Object_ptr) soundCardCapture_var, objName.c_str());

    // This bit is ORB specific
    // omniorb is threaded and the servants are running at this point
    // so we block on the condition
    // The releaseObject method clear the condition and the component exits

    component_running->wait();
    orb->unbind_name(label);
    orb->orb->shutdown(0);


}
