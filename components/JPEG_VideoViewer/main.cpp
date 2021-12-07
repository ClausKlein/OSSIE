/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE JPEG_VideoViewer.

OSSIE JPEG_VideoViewer is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE JPEG_VideoViewer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE JPEG_VideoViewer; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/

#include <iostream>
#include "ossie/ossieSupport.h"

#include "JPEG_VideoViewer.h"

using namespace standardInterfaces;  // For standard OSSIE interface classes


int main(int argc, char* argv[])

{
    ossieDebugLevel = 3;

    ossieSupport::ORB *orb = new ossieSupport::ORB;
    omni_mutex component_running_mutex;
    omni_condition *component_running = new omni_condition(&component_running_mutex);

    if (argc != 3) {
	std::cout << argv[0] << " <id> <usage name> " << std::endl;
	exit (-1);
    }

    char *uuid = argv[1];
    char *label = argv[2];

    std::cout << "Identifier - " << uuid << "  Label - " << label << std::endl;

    JPEG_VideoViewer_i* jpeg_videoviewer_servant;
    CF::Resource_var jpeg_videoviewer_var;

    // Create the jpeg_videoviewer component servant and object reference

    jpeg_videoviewer_servant = new JPEG_VideoViewer_i(uuid, component_running);
    jpeg_videoviewer_var = jpeg_videoviewer_servant->_this();

    orb->bind_object_to_name((CORBA::Object_ptr) jpeg_videoviewer_var, label);

    // This bit is ORB specific
    // omniorb is threaded and the servants are running at this point
    // so we block on the condition
    // The releaseObject method clear the condition and the component exits

    component_running->wait();
    orb->unbind_name(label);
    orb->orb->shutdown(0);

}
