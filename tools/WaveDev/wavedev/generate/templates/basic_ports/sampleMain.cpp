#include <iostream>
#include "ossie/ossieSupport.h"

#include "__IncludeFile__.h"


int main(int argc, char* argv[])

{
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

    __Class_name__* __CLASS_VAR___servant;
    CF::Resource_var __CLASS_VAR___var;

    // Create the __CLASS_VAR__ component servant and object reference

    __CLASS_VAR___servant = new __Class_name__(uuid, component_running);
    __CLASS_VAR___var = __CLASS_VAR___servant->_this();
    __CLASS_VAR_ACE___servant->activate();

    orb->bind_object_to_name((CORBA::Object_ptr) __CLASS_VAR___var, label);

    // This bit is ORB specific
    // omniorb is threaded and the servants are running at this point
    // so we block on the condition
    // The releaseObject method clear the condition and the component exits

    component_running->wait();
    orb->unbind_name(label);
    orb->orb->shutdown(0);

}
