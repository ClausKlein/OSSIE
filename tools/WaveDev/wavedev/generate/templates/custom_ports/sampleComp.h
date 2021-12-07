
#ifndef __CLASS_DEF__
#define __CLASS_DEF__

#include <stdlib.h>

#include "ossie/cf.h"
__ACE_INCLUDES__

#include "ossie/Resource_impl.h"

class __Class_name__;
#include "port_impl.h"

class __Class_name__ : public Resource_impl__ACE_INHERIT__
{

    __FRIEND_DECL__

    public:
        __Class_name__(const char *uuid, omni_condition *con, const char *);

        ~__Class_name__(void);

        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        CORBA::Object_ptr getPort( const char* _id ) throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

	void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);

        void configure(const CF::Properties&) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration);

        __ACE_SVC_DECL__

    private:
        // For component shutdown
        omni_condition *component_running;

    	__PORT_DECL__

};
#endif
