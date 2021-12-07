/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE WebCamCapture.

OSSIE WebCamCapture is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE WebCamCapture is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE WebCamCapture; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/


#ifndef WEBCAMCAPTURE_IMPL_H
#define WEBCAMCAPTURE_IMPL_H

#include <stdlib.h>
#include "ossie/cf.h"
#include "ossie/PortTypes.h"
#include "ossie/Resource_impl.h"
#include "ossie/debug.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <pthread.h>
#include <SDL/SDL.h>
#include <SDL/SDL_thread.h>
#include <SDL/SDL_audio.h>
#include <SDL/SDL_timer.h>
#include <linux/videodev.h> //*/usr/include/linux
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <errno.h>
#include <fcntl.h>
#include <time.h>
#include <sys/time.h>
#include <signal.h>
#include "SDL_audioin.h"

#include "jconfig.h"
#include "utils.h"



#include "standardinterfaces/realChar.h"
#include "standardinterfaces/realChar_u.h"

class WebCamCapture_i : public virtual Resource_impl
{

    public:
        WebCamCapture_i(const char *uuid, omni_condition *sem);
        ~WebCamCapture_i(void);

        static void run( void * data ); // static function for omni thread

        void start() throw (CF::Resource::StartError, CORBA::SystemException);
        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        CORBA::Object_ptr getPort( const char* portName ) throw (CF::PortSupplier::UnknownPort, CORBA::SystemException);

        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        void initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException);
        void configure(const CF::Properties&) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration);

unsigned char *tmp;

    private:
        WebCamCapture_i();
        WebCamCapture_i(WebCamCapture_i&);

        void run_loop(); // main signal processing
   
        omni_condition *component_running;  //for component shutdown
        omni_thread *processing_thread;     //for component writer function
    	

        
        //list components provides and uses ports
        standardInterfaces_i::realChar_u *dataOut_0;

        // algorithm variables
       bool isRunning; 
      unsigned short quality; 
};

#endif

