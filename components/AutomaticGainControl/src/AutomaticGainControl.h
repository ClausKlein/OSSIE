/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE AutomaticGainControl.

OSSIE AutomaticGainControl is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE AutomaticGainControl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE AutomaticGainControl; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/


#ifndef AUTOMATICGAINCONTROL_IMPL_H
#define AUTOMATICGAINCONTROL_IMPL_H

#include <stdlib.h>
#include "ossie/cf.h"
#include "ossie/Resource_impl.h"
#include "ossie/PortTypes.h"
#include "ossie/debug.h"

#include "standardinterfaces/complexShort.h"
#include "standardinterfaces/complexShort_u.h"
#include "standardinterfaces/complexShort_p.h"

#include "sigproc/SigProc.h"

/// \brief
///
class AutomaticGainControl_i : public virtual Resource_impl
{

    public:
        /// initializing constructor
        AutomaticGainControl_i(const char *uuid, omni_condition *sem);

        /// destructor
        ~AutomaticGainControl_i(void);

        ///
        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        ///
        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        /// static function for omni thread
        static void run(void *data);

        ///
        CORBA::Object_ptr getPort( const char* portName ) throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

        ///
        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        ///
        void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);

        ///
        void configure(const CF::Properties&) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration);


    private:
        /// disallow default constructor
        AutomaticGainControl_i();

        /// disallow copy constructor
        AutomaticGainControl_i(AutomaticGainControl_i&);
        
        /// main signal processing method
        void run_loop();
        
        /// for component shutdown
        omni_condition *component_running;

        /// for component writer function
        omni_thread *processing_thread;

        /// for asynchronous configure() invocation
        omni_mutex accessPrivateData;
    	
        // ----- list components provides and uses ports -----
        
        /// output data port, \ref port_data_out "data_out"
        standardInterfaces_i::complexShort_u *dataOut_0;

        /// input data port, \ref port_data_in "data_in"
        standardInterfaces_i::complexShort_p *dataIn_0;

        // ----- algorithm variables -----
        
        /// low energy threshold
        float energy_lo;

        /// high energy threshold
        float energy_hi;

        /// attack time constant
        float k_attack;

        /// release time constant
        float k_release;

        /// maximum allowable gain
        float g_max;

        /// minimum allowable gain
        float g_min;
        
        /// Received signal strength level above which data will be passed
        float rssi_pass;

        /// Counter used for sending packets once RSSI has dropped below threshold
        short rssi_pass_packet_counter;
        
};
#endif
