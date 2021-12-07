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

#include <string>
#include <iostream>
#include <math.h>
//#include "ossie/cf.h"
#include "am_demod.h"
//#include "ossie/PortTypes.h"
/*Data type will change for the next three statements based on standardInterfaces selected in OWD*/
//#include "standardinterfaces/complexShort.h"	
/*new hidden uses port imp. (output)*/	
//#include "standardinterfaces/complexShort_u.h"	
/*new hidden provides port imp. (input)*/	
//#include "standardinterfaces/complexShort_p.h"		

//#include "ossie/Resource_impl.h"

am_demod_i::am_demod_i(const char *uuid, omni_condition *condition) : Resource_impl(uuid), component_running(condition)
{

	/*Depending on component type, there may be 0,1 or multiple Uses Ports*/
	dataOut = new standardInterfaces_i::complexShort_u("Out_to_sound_card");	//Create Port for output 
	
	/*Depending on component type, there may be 0,1 or multiple Provides Ports*/
	dataIn = new standardInterfaces_i::complexShort_p("Rx_In_from_USRP_or_Decimator");		//Create Port for input

	processing_thread = new omni_thread(process_data, (void *) this);		//Create the thread for the writer's processing function

	processing_thread->start();							//Start the thread containing the writer's processing function

}

CORBA::Object_ptr am_demod_i::getPort(const char* portName) throw (CORBA::SystemException, CF::PortSupplier::UnknownPort)
{
        std::cout << "am_demod getPort called with : " << portName << std::endl;

	CORBA::Object_var p;

	p = dataOut->getPort(portName);
	
	if (!CORBA::is_nil(p))
	return p._retn();

	p = dataIn->getPort(portName);

	if (!CORBA::is_nil(p))
	return p._retn();

	/*Exception*/
	throw CF::PortSupplier::UnknownPort();
}

void am_demod_i::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
	std::cout << "start called on am_demod" << std::endl;
}

void am_demod_i::stop() throw (CORBA::SystemException, CF::Resource::StopError) 
{  
	std::cout << "stop called on am_demod" << std::endl;
}

void am_demod_i::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
	std::cout << "releaseObject called on am_demod" << std::endl;
	
	component_running->signal();
}

void am_demod_i::initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException)
{
	std::cout << "initialize called on am_demod" << std::endl;
}

void am_demod_i::configure(const CF::Properties& props) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration)
{
// 	cout << "configure called on am_demod" << endl;
// 	
// 	cout << "props length : " << props.length() << endl;
// 
// 	for (unsigned int i = 0; i <props.length(); i++)
// 	{
// 		cout << "Property id : " << props[i].id << endl;
// 		
// 		if (strcmp(props[i].id, "DCE:bf56efe7-1186-4823-bd0e-bd5497cdca8c") == 0)
// 		{
// 			props[i].value >>= *simple_ptr;
// 			simple_value = *simple_ptr;
// 		}
// 
// 		if (strcmp(props[i].id, "DCE:79738aed-9a9b-4332-9b44-5c4ec5745a40") == 0)
// 		{
// 			
// 			props[i].value >>= simplesequence_ptr;
// 			simplesequencelength = simplesequence_ptr->length();
// 			cout << "simplesequence has length : " << simplesequencelength << endl;
// 			
// 			delete []simplesequence_ptr;
// 			simplesequence_ptr = new CORBA::ShortSeq(simplesequencelength);
// 			for (unsigned int i = 0; i < simplesequencelength; i++)
// 			{
// 				simplesequence_ptr[i] = (*simplesequence_ptr)[i];
// 			}
// 			
// 		}
// 	}
}

void process_data(void *data)
{
	std::cout << "am_demod process_data thread started" << std::endl;

	am_demod_i *channel = (am_demod_i *) data;

	PortTypes::ShortSequence I_out, Q_out;
	signed int maxval=0, volgain=1,packetcount=0;
	long int demodsignal;
	
	while(1)
	{
		//cout<<"maxval="<<maxval<<" volgain="<<volgain<<endl;
		PortTypes::ShortSequence *I_in(NULL), *Q_in(NULL);
		channel->dataIn->getData(I_in, Q_in);
		I_out.length(I_in->length());
		Q_out.length(Q_in->length());
		/*Insert Code here to do work*/
		for (unsigned int i=0;i<I_in->length();i++)
		{
			demodsignal=((*I_in)[i]*(*I_in)[i] + (*Q_in)[i]*(*Q_in)[i]);
			
			//I_out[i]=((*I_in)[i] + (*Q_in)[i]);
			I_out[i]=(sqrt(demodsignal));

			if (maxval<I_out[i])
			{
				maxval=I_out[i];
			};
			I_out[i]=I_out[i]*volgain;
			Q_out[i]=I_out[i];
		};
		//Pseudo auto gain
		packetcount++;
		if (packetcount>2)
		{
		volgain=30000/maxval;
		packetcount=0;
		}
		
		//cout<<"maxval="<<maxval<<" volgain="<<volgain<<endl;
			
		channel->dataIn->bufferEmptied();
		channel->dataOut->pushPacket(I_out, Q_out);
	}
}





