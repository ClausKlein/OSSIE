
#ifndef __CLASS_DEF__
#define __CLASS_DEF__

#include <stdlib.h>
#include "ossie/cf.h"
#include "ossie/PortTypes.h"
#include "ossie/Resource_impl.h"
#include "ossie/debug.h"

__ACE_INCLUDES__

__SI_BASES__
__USES_SI__
__PROVIDES_SI__

/** \brief
 *
 *
 */
class __Class_name__ : public virtual Resource_impl__ACE_INHERIT__
{
  public:
    /// Initializing constructor
    __Class_name__(const char *uuid, omni_condition *sem);

    /// Destructor
    ~__Class_name__(void);

    /// Static function for omni thread
    static void Run( void * data );

    ///
    void start() throw (CF::Resource::StartError, CORBA::SystemException);

    ///
    void stop() throw (CF::Resource::StopError, CORBA::SystemException);

    ///
    CORBA::Object_ptr getPort( const char* portName )
        throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

    ///
    void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

    ///
    void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);

    /// Configures properties read from .prf.xml
    void configure(const CF::Properties&)
        throw (CORBA::SystemException,
            CF::PropertySet::InvalidConfiguration,
            CF::PropertySet::PartialConfiguration);

    __ACE_SVC_DECL__

  private:
    /// Disallow default constructor
    __Class_name__();

    /// Disallow copy constructor
    __Class_name__(__Class_name__&);

    /// Main signal processing method
    void ProcessData();
   
    omni_condition *component_running;  ///< for component shutdown
    omni_thread *processing_thread;     ///< for component writer function
    	
    __CORBA_SIMPLE_PROP_DECL__

    __CORBA_SIMPLE_SEQUENCE_PROP_DECL__
    
    // list components provides and uses ports
    __PORT_DECL__
    
};
#endif
