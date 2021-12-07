
#include <string>
#include <iostream>
#include "__IncludeFile__.h"

__Class_name__::__Class_name__(const char *uuid, omni_condition *condition) : 
    Resource_impl(uuid), component_running(condition) 
{
    __CONSTRUCTORS__

    //Create the thread for the writer's processing function 
    processing_thread = new omni_thread(Run, (void *) this);

    //Start the thread containing the writer's processing function 
    processing_thread->start();

}

__Class_name__::~__Class_name__(void)
{   
    __PORT_DESTRUCTORS__
    __SIMPLE_SEQUENCE_POINTER_DESTRUCTORS__
}

// Static function for omni thread
void __Class_name__::Run( void * data )
{
    ((__Class_name__*)data)->ProcessData();
}

CORBA::Object_ptr __Class_name__::getPort( const char* portName ) throw (
    CORBA::SystemException, CF::PortSupplier::UnknownPort)
{
    DEBUG(3, __IncludeFile__, "getPort() invoked with " << portName)
    
    CORBA::Object_var p;

__GET_PORT__
}

void __Class_name__::start() throw (CORBA::SystemException, 
    CF::Resource::StartError)
{
    DEBUG(3, __IncludeFile__, "start() invoked")
}

void __Class_name__::stop() throw (CORBA::SystemException, CF::Resource::StopError) 
{  
    DEBUG(3, __IncludeFile__, "stop() invoked")
}

void __Class_name__::releaseObject() throw (CORBA::SystemException,
    CF::LifeCycle::ReleaseError)
{
    DEBUG(3, __IncludeFile__, "releaseObject() invoked")
    
    component_running->signal();
}

void __Class_name__::initialize() throw (CF::LifeCycle::InitializeError,
    CORBA::SystemException)
{
    DEBUG(3, __IncludeFile__, "initialize() invoked")
}

void __Class_name__::configure(const CF::Properties& props)
throw (CORBA::SystemException,
    CF::PropertySet::InvalidConfiguration,
    CF::PropertySet::PartialConfiguration)
{
    DEBUG(3, __IncludeFile__, "configure() invoked")
    
    __READ_PROPS__
}

void __Class_name__::ProcessData()
{
    DEBUG(3, __IncludeFile__, "ProcessData() invoked")

    __PROCESS_DATA_DECLARATIONS__

    __PROCESS_DATA_LOOP__
}

__ACE_SVC_DEF__

