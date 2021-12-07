/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE Sound_out Device.

OSSIE Sound_out Device is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE Sound_out Device is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE Sound_out Device; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


****************************************************************************/

/** \file 
    The Sound_out.h file contains declarations for the SoundCardPlayback_i
    class.
*/



#ifndef TEMPLATE_COMPONENT_IMPL_H
#define TEMPLATE_COMPONENT_IMPL_H

#include <stdlib.h>
#include "ossie/cf.h"
#include "ossie/PortTypes.h"
#include "ossie/Device_impl.h"
#include "ossie/Resource_impl.h"
#include "ossie/debug.h"

#include "standardinterfaces/complexShort.h"
#include "standardinterfaces/complexShort_u.h"

#include <alsa/asoundlib.h>

/// Main sound card device (capture) definition
class SoundCardCapture_i : public virtual Device_impl 
{
    public:
        /// Initializing constructor
        SoundCardCapture_i(char *uuid, char* label, char* profile, omni_condition *condition);

        /// Default destructor
        ~SoundCardCapture_i();

        /// Sets isRunning to True (start)
        void start() 
            throw (CF::Resource::StartError, CORBA::SystemException);

        /// static function for omni thread
        static void run( void * data );

        /// Sets isRunning to False (pause)
        void stop() 
            throw (CF::Resource::StopError, CORBA::SystemException);

        /// Returns CORBA object pointer to port
        CORBA::Object_ptr getPort(const char* portName) 
            throw(CF::PortSupplier::UnknownPort, CORBA::SystemException);

        /// Checks if sound card device (capture) is already in use
        void initialize() 
            throw (CF::LifeCycle::InitializeError, CORBA::SystemException);

        /// Sets the following properties (currently NOT read from .prf.xml)
        ///   - Access mode
        ///   - Format
        ///   - Number of channels
        ///   - Sampling rate
        ///   - Period size
        ///   - Buffer size
        ///   - Hardware parameters
        void configure(const CF::Properties &props) 
            throw (CORBA::SystemException, 
                   CF::PropertySet::InvalidConfiguration, 
                   CF::PropertySet::PartialConfiguration);

        ///
        void releaseObject() 
            throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

    private:
        /// Disallow default constructor
        SoundCardCapture_i();

        /// Disallow copy constructor
        SoundCardCapture_i(SoundCardCapture_i&);

        /// main processing loop for capturing sound
        void capture_sound();

        omni_condition *component_running; ///< for component shutdown
        omni_thread *processing_thread;    ///< for component writer function

        CORBA::UShort *simple_ptr;
        CORBA::UShort simple_value;
        unsigned int simplesequencelength;
        CORBA::ShortSeq *simplesequence_ptr;
        //simplesequence_ptr = new short[simplesequencelength];

        /// Port: output sound samples
        standardInterfaces_i::complexShort_u *dataOut;
 
        // --- Sound capture variables ---
        snd_pcm_t *pcm_handle;         ///< 
        snd_pcm_uframes_t periodsize;  ///< 
        unsigned int length;           ///< 

        // Until I look at omni_condition... -TT
        bool isRunning;  ///< starts/stops loop in capture_sound()
  
};
#endif

