/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE am_demod.

OSSIE am_demod is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE am_demod is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE am_demod; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/


#ifndef am_demod_IMPL_H
#define am_demod_IMPL_H

#include <stdlib.h>
#include "ossie/cf.h"

#include "ossie/PortTypes.h"
/*Data type will change for the next three statements based on standardInterfaces selected in OWD*/
#include "standardinterfaces/complexShort.h"	
/*new hidden uses port imp. (output)*/	
#include "standardinterfaces/complexShort_u.h"	
/*new hidden provides port imp. (input)*/	
#include "standardinterfaces/complexShort_p.h"		

#include "ossie/Resource_impl.h"
class am_demod_i;

void process_data(void *data);

class am_demod_i : public virtual Resource_impl
{
    friend class dataOut_i;
    friend class dataIn_i;
    friend void process_data(void *data);

    public:
        am_demod_i(const char *uuid, omni_condition *sem);

        void start() throw (CF::Resource::StartError, CORBA::SystemException);
        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        CORBA::Object_ptr getPort( const char* portName ) throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

	void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);
        void configure(const CF::Properties&) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration);

    private:
	am_demod_i();
	am_demod_i(am_demod_i&);

        omni_condition *component_running;	//for component shutdown
	omni_thread *processing_thread;		//for component writer function

	CORBA::UShort *simple_ptr;
	CORBA::UShort simple_value;
	unsigned int simplesequencelength;
	CORBA::ShortSeq *simplesequence_ptr;
	//simplesequence_ptr = new short[simplesequencelength];
	
	
	/*List all of components uses ports*/
	/*depending on component type, there may be 0,1, or multiple Uses Ports*/
	standardInterfaces_i::complexShort_u *dataOut;

	/*List all of components provides ports*/
	/*depending on component type, there may be 0,1, or multiple Provides Ports*/
	standardInterfaces_i::complexShort_p *dataIn;
        
};
#endif
