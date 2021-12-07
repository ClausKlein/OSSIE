
#include <iostream>

#include "__IncludeFile__.h"

#include "port_impl.h"

__Class_name__::__Class_name__(const char *uuid, omni_condition *con, const char *label) : Resource_impl(uuid)
{
    component_running = con;

__PORT_INST__
}


__Class_name__::~__Class_name__(void)
{
__DEL_PORT__
}

CORBA::Object_ptr __Class_name__::getPort( const char* _id ) throw (CORBA::SystemException, CF::PortSupplier::UnknownPort)
{
__GET_PORT__
}

void __Class_name__::start() throw (CORBA::SystemException, CF::Resource::StartError)
{

}

void __Class_name__::stop() throw (CORBA::SystemException, CF::Resource::StopError) {  }

void __Class_name__::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    // Clear the component running condition so main shuts down everything
    component_alive = false;
    component_running->signal();
}

void __Class_name__::initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException)
{

}

void __Class_name__::configure(const CF::Properties& props) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration)
{
    PropertySet_impl::configure(props);
}


__ACE_SVC_DEF__

