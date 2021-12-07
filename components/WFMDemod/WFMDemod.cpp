/****************************************************************************

Copyright 2007 Virginia Polytechnic Institute and State University

This file is part of the OSSIE WFMDemod.

OSSIE WFMDemod is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE WFMDemod is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE WFMDemod; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/


#include <string>
#include <iostream>
#include "WFMDemod.h"
#include <math.h>

WFMDemod_i::WFMDemod_i(const char *uuid, omni_condition *condition) : 
    Resource_impl(uuid), component_running(condition) 
{
    dataOut_0 = new standardInterfaces_i::complexShort_u("dataOut");
    dataIn_0 = new standardInterfaces_i::complexShort_p("dataIn");

    //Create the thread for the writer's processing function 
    processing_thread = new omni_thread(Run, (void *) this);

    //Start the thread containing the writer's processing function 
    processing_thread->start();

}

WFMDemod_i::~WFMDemod_i(void)
{   
    delete dataOut_0;
    delete dataIn_0;
}

// Static function for omni thread
void WFMDemod_i::Run( void * data )
{
    ((WFMDemod_i*)data)->ProcessData();
}

CORBA::Object_ptr WFMDemod_i::getPort( const char* portName ) throw (
    CORBA::SystemException, CF::PortSupplier::UnknownPort)
{
    DEBUG(3, WFMDemod, "getPort() invoked with " << portName)
    
    CORBA::Object_var p;

    p = dataOut_0->getPort(portName);

    if (!CORBA::is_nil(p))
        return p._retn();

    p = dataIn_0->getPort(portName);

    if (!CORBA::is_nil(p))
        return p._retn();

    /*exception*/
    throw CF::PortSupplier::UnknownPort();
}

void WFMDemod_i::start() throw (CORBA::SystemException, 
    CF::Resource::StartError)
{
    DEBUG(3, WFMDemod, "start() invoked")
}

void WFMDemod_i::stop() throw (CORBA::SystemException, CF::Resource::StopError) 
{  
    DEBUG(3, WFMDemod, "stop() invoked")
}

void WFMDemod_i::releaseObject() throw (CORBA::SystemException,
    CF::LifeCycle::ReleaseError)
{
    DEBUG(3, WFMDemod, "releaseObject() invoked")
    
    component_running->signal();
}

void WFMDemod_i::initialize() throw (CF::LifeCycle::InitializeError,
    CORBA::SystemException)
{
    DEBUG(3, WFMDemod, "initialize() invoked")
}

void WFMDemod_i::configure(const CF::Properties& props)
throw (CORBA::SystemException,
    CF::PropertySet::InvalidConfiguration,
    CF::PropertySet::PartialConfiguration)
{
    DEBUG(3, WFMDemod, "configure() invoked")
    
    std::cout << "props length : " << props.length() << std::endl;

    for (unsigned int i = 0; i <props.length(); i++)
    {
        std::cout << "Property id : " << props[i].id << std::endl;

    }
}

void WFMDemod_i::ProcessData()
{
    DEBUG(3, WFMDemod, "ProcessData() invoked")

    PortTypes::ShortSequence I_out_0, Q_out_0;


    PortTypes::ShortSequence *I_in_0(NULL), *Q_in_0(NULL);
    CORBA::UShort I_in_0_length, Q_in_0_length;

    int I1, I2, Q1, Q2;

    while(1)
    {
        dataIn_0->getData(I_in_0, Q_in_0);

        I_in_0_length = I_in_0->length();
        Q_in_0_length = Q_in_0->length();

        I_out_0.length(I_in_0_length); //must define length of output
        Q_out_0.length(Q_in_0_length); //must define length of output

        /*insert code here to do work*/
        for (unsigned int i(0); i < I_in_0_length; ++i) {
            int I0((*I_in_0)[i]), Q0((*Q_in_0)[i]);

        DEBUG(10, WFMDemod, "Normalized: I_in = " << I0 << ", Q_in = " << Q0 << ", mag = " << sqrt(I0*I0 + Q0*Q0));

#if 1
        // Calculate output from Lyon's Fig 13-61(b)
	I_out_0[i] = ((I1 * (Q0 - Q2)) >> 10) - ((Q1 * (I0 - I2)) >> 10);
#else
	// Brute force FM demod
        I_out_0[i] = atan2((I0*I1 + Q0*Q1), (I1*Q0 - I0*Q1)) * 5000;
#endif
        Q_out_0[i] = I_out_0[i];

        // Update delay terms;
        I2 = I1;
        I1 = I0;
        Q2 = Q1;
        Q1 = Q0;


	}

        dataIn_0->bufferEmptied();
        dataOut_0->pushPacket(I_out_0, Q_out_0);
    }
}


