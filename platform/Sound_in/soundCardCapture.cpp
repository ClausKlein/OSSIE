/**************************************************************************** 
Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE Sound_out Device.

OSSIE Sound_out Device is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE Sound_out Device is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE Sound_out Device; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/

/** \file
    The soundCardCapture.cpp file contains definitions for the SoundCardCapture_i
    class implementation.
*/

#include <iostream>
#include "soundCardCapture.h"

// Initializing constructor
SoundCardCapture_i::SoundCardCapture_i(char *uuid, char *label, char *profile, omni_condition *condition) 
  : Device_impl(uuid, label, profile), component_running(condition), isRunning(false)
{
    DEBUG(3, SoundCardCapture, "constructor invoked")

    // Create Port for output sound
    dataOut = new standardInterfaces_i::complexShort_u("complexShortOut");

    // Start the capture_sound thread
    processing_thread = new omni_thread(run, (void *) this);
    processing_thread->start();
}

// Default destructor
SoundCardCapture_i::~SoundCardCapture_i()
{

}

// static function for omni thread
void SoundCardCapture_i::run( void * data )
{
    ((SoundCardCapture_i*) data)->capture_sound();
}

void SoundCardCapture_i::start() 
throw (CF::Resource::StartError, CORBA::SystemException)
{
    DEBUG(3, SoundCardCapture, "start() invoked")

    isRunning = true;
}

void SoundCardCapture_i::stop()
throw (CF::Resource::StopError, CORBA::SystemException)

{
    DEBUG(3, SoundCardCapture, "stop() invoked")

    isRunning = false;
}

CORBA::Object_ptr SoundCardCapture_i::getPort(const char* portName) 
throw(CF::PortSupplier::UnknownPort, CORBA::SystemException)

{
    DEBUG(3, SoundCardCapture, "getPort() invoked with: " << portName)

    CORBA::Object_var u;

    u = dataOut->getPort(portName);

    if (!CORBA::is_nil(u))
    return u._retn();

    /// Port name not found; throw exception
    throw CF::PortSupplier::UnknownPort();

}

void SoundCardCapture_i::initialize() 
throw (CF::LifeCycle::InitializeError, CORBA::SystemException)

{
    DEBUG(3, SoundCardCapture, "initialize() invoked")

    snd_pcm_stream_t stream = SND_PCM_STREAM_CAPTURE;
    char *pcm_name = "plughw:0,0";
    int rc;

    if ((rc = snd_pcm_open(&pcm_handle, pcm_name, stream, 0)) < 0) {
        DEBUG(1, SoundCardCapture, "Failed to open pcm device " << pcm_name)
        if (rc == -EBUSY) 
            DEBUG(1, SoundCardCapture, "Sound device in use.")
        
        //throw(CF::LifeCycle::InitializeError());
    }

    DEBUG(1, SoundCardCapture, "Initialize (capture) exit")
}

void SoundCardCapture_i::configure(const CF::Properties &props) 
throw (CORBA::SystemException, 
       CF::PropertySet::InvalidConfiguration, 
       CF::PropertySet::PartialConfiguration)
{
    DEBUG(3, SoundCardCapture, "configure() invoked. Number of props = " 
              << props.length()  
             )

    // read properties from .prf
    unsigned int rate(16000); // default sampling rate
    
    for (unsigned int i=0; i<props.length(); i++)
    {
        DEBUG(3, SoundCardCapture, "configure property id : " << props[i].id)

        if (strcmp(props[i].id, "DCE:ee0260bc-735a-4df5-bd71-726576ba8fbf")==0)
        {
            CORBA::Short n;
            props[i].value >>= n;
            rate = n;
            DEBUG(3, SoundCardCapture, "sample rate: " << rate << " Hz")
        }
        else
        {
            DEBUG(1, SoundCardCapture, "ERROR: unkown configure() property id " << props[i].id)
            throw(CF::PropertySet::InvalidConfiguration());
        }
    }


    snd_pcm_hw_params_t *hwparams;
    int rc;

    snd_pcm_hw_params_alloca(&hwparams);

    if (snd_pcm_hw_params_any(pcm_handle, hwparams)) {
        DEBUG(1, SoundCardCapture, "Can not configure this PCM device.")
        throw(CF::PropertySet::InvalidConfiguration());
    }

    if (snd_pcm_hw_params_set_access(pcm_handle, hwparams, SND_PCM_ACCESS_RW_INTERLEAVED) < 0) {
        DEBUG(1, SoundCardCapture, "Error setting access mode.")
        throw(CF::PropertySet::InvalidConfiguration());
    }

    if (snd_pcm_hw_params_set_format(pcm_handle, hwparams, SND_PCM_FORMAT_S16_LE) < 0) {
        DEBUG(1, SoundCardCapture, "Error setting format.")
        throw(CF::PropertySet::InvalidConfiguration());
    }

    // Set number of channels to two for stereo
    if (snd_pcm_hw_params_set_channels(pcm_handle, hwparams, 2) < 0) {
        DEBUG(1, SoundCardCapture, "Error setting number of channels.")
        throw(CF::PropertySet::InvalidConfiguration());
    }

    // Set the sampling rate (best effort)
    unsigned int exact_rate = rate;
    if (snd_pcm_hw_params_set_rate_near(pcm_handle, hwparams, &exact_rate, 0) < 0) {
        DEBUG(1, SoundCardCapture, "Error setting rate.")
        throw(CF::PropertySet::InvalidConfiguration());
    }
    if (rate != exact_rate) {
        DEBUG(1, SoundCardCapture, "The rate " << rate 
                  << " is not supported by your hardware. Using " 
                  << exact_rate << " instead.")
    }

    // Set up period size
    periodsize = 512;
    snd_pcm_uframes_t exactperiodsize = periodsize;
    rc = snd_pcm_hw_params_set_period_size_near(pcm_handle, hwparams, &exactperiodsize, 0);
    if (rc < 0) {
        DEBUG(1, SoundCardCapture, "Error setting period size" << snd_strerror(rc))
        throw(CF::PropertySet::InvalidConfiguration());
    }
    if (periodsize != exactperiodsize) {
        DEBUG(1, SoundCardCapture, "Period size set to " << exactperiodsize 
                  << " not the requested " << periodsize 
                 )
        periodsize = exactperiodsize;
    }

    // Set the buffer size
    snd_pcm_uframes_t buffersize = 8 * periodsize;
    if ((rc = snd_pcm_hw_params_set_buffer_size_near(pcm_handle, hwparams, &buffersize)) < 0) {
        DEBUG(1, SoundCardCapture, "Error setting buffer size, " << snd_strerror(rc))
        throw(CF::PropertySet::InvalidConfiguration());
    }

    // Get the buffer size
    snd_pcm_uframes_t periods = 0;
    if ((rc = snd_pcm_hw_params_get_buffer_size(hwparams, &periods)) < 0) {
        DEBUG(1, SoundCardCapture, "Error getting the buffer size " << snd_strerror(rc))
        throw(CF::PropertySet::InvalidConfiguration());
    }
    DEBUG(3, SoundCardCapture, "Buffer size " << periods)

    // Apply HW settings
    if (snd_pcm_hw_params(pcm_handle, hwparams) < 0) {
        DEBUG(1, SoundCardCapture, "Error setting HW params.")
        throw(CF::PropertySet::InvalidConfiguration());
    }

    // set up capture buffer
//    length = periods * 2 * 8;
//    DEBUG(3, SoundCardCapture, "Capture buffer length = " << length)
//    capture_buffer = new short[length];

}

void SoundCardCapture_i::releaseObject()
throw (CF::LifeCycle::ReleaseError, CORBA::SystemException)
{
    DEBUG(3, SoundCardCapture, "releaseObject() invoked")

    component_running->signal();
}

void SoundCardCapture_i::capture_sound()
{
    DEBUG(3, SoundCardCapture, "capture_sound() invoked")
    PortTypes::ShortSequence L_out, R_out;

    const int buf_size = 512;
    
    short buf[buf_size]; 

    int buf_length = buf_size / 2;

    L_out.length(buf_length);
    R_out.length(buf_length);
   
    int rc;

    while(1)
    {
        if (isRunning) {
            if ((rc = snd_pcm_readi(pcm_handle, buf, buf_length)) < 0) {

                if (rc == -EPIPE) {
                    std::cerr << "Sound card overrun occured." << std::endl;
                    snd_pcm_prepare(pcm_handle);
                }
                else { 
                    std::cerr << "Sound read error, " << snd_strerror(rc)
                              << std::endl;
                } 
            }
            else if (rc == buf_length) {
                for (int i = 0; i < buf_length; i++) {
                    L_out[i] = buf[i*2];
                    R_out[i] = buf[i*2+1];
                }
                dataOut->pushPacket(L_out, R_out);
            }
            else {
                // Less than requested amount of data received or other error.
                // Can output shorter buffer or just err.
                std::cerr << "Sound card underrun occured" << std::endl;
            }
    
        }
        else {
            // Sit and wait if the device is stopped. Need to figure out
            // something instead of polling...  -TT
            usleep(1000);
        }
    }
}

