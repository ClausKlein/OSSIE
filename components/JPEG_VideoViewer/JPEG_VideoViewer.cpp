/****************************************************************************

Copyright 2006 Virginia Polytechnic Institute and State University

This file is part of the OSSIE JPEG_VideoViewer.

OSSIE JPEG_VideoViewer is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE JPEG_VideoViewer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE JPEG_VideoViewer; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/


#include <string>
#include <iostream>
#include "JPEG_VideoViewer.h"


#define VIDEOMON 1 

unsigned int image_width = IMAGE_WIDTH;
unsigned int image_height = IMAGE_HEIGHT;
int owidth = 0;
int oheight = 0;
int testbpp=16;
int autobright = 0;
int bpp = 3;	
SDL_Surface *pscreen;
int format = VIDEO_PALETTE_JPEG;

JPEG_VideoViewer_i::JPEG_VideoViewer_i(const char *uuid, omni_condition *condition)
  : Resource_impl(uuid), component_running(condition) 
{
    dataIn_0 = new standardInterfaces_i::realChar_p("JPEG_DataIn");


    //Create the thread for the writer's processing function 
    processing_thread = new omni_thread(run, (void *) this);

    //Start the thread containing the writer's processing function 
    processing_thread->start();

}

// Destructor
JPEG_VideoViewer_i::~JPEG_VideoViewer_i(void)
{   
   delete dataIn_0;
}

// static function for omni thread
void JPEG_VideoViewer_i::run( void * data )
{
    ((JPEG_VideoViewer_i*)data)->run_loop();
}

CORBA::Object_ptr JPEG_VideoViewer_i::getPort( const char* portName ) throw (CORBA::SystemException, CF::PortSupplier::UnknownPort)
{
    DEBUG(3, JPEG_VideoViewer, "getPort invoked with port name: " << portName)
    
    CORBA::Object_var p;

    p = dataIn_0->getPort(portName);

    if (!CORBA::is_nil(p))
        return p._retn();

    /*exception*/
    throw CF::PortSupplier::UnknownPort();
}

void JPEG_VideoViewer_i::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    DEBUG(3, JPEG_VideoViewer, "start invoked")
      
      		
    
    isRunning = true; 

}

void JPEG_VideoViewer_i::stop() throw (CORBA::SystemException, CF::Resource::StopError) 
{  
    DEBUG(3, JPEG_VideoViewer, "stop invoked")
    //Uint32 frame_color = NULL;
    //Uint8 r, g, b;

    isRunning = false;
    
    //r = g = b = 0xFF;
/*
    frame_color = SDL_MapRGB(pscreen->format, r, g, b);
    if(SDL_FillRect(pscreen, NULL, frame_color) < 0)
    {
      std::cout << "Error: Could not set frame to NULL" << std::endl;
    }
    SDL_UpdateRect (pscreen, 0, 0, 0, 0);	//update the entire screen
*/
}

void JPEG_VideoViewer_i::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    DEBUG(3, JPEG_VideoViewer, "releaseObject invoked")
    
    if(VIDEOMON)
    {
      SDL_Quit();
    }

    component_running->signal();
}

void JPEG_VideoViewer_i::initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException)
{
    DEBUG(3, JPEG_VideoViewer, "initialize invoked")

    	  
	if(VIDEOMON)
  {
    printf ("Initializing SDL.\n");

    /* Initialize defaults, Video and Audio */
	  if ((SDL_InitSubSystem (SDL_INIT_VIDEO | SDL_INIT_TIMER) == -1)) 
    {
		  printf ("Could not initialize SDL: %s.\n", SDL_GetError ());
		  exit (-1);
	  }
	
	  /* Clean up on exit */
	  atexit (SDL_Quit);
	  if(!owidth || !oheight)
    {
		  owidth	= image_width;
		  oheight	= image_height;
	  }	
	  printf ("SDL initialized.\n");

    printf("Creating Video Frame...\n");
		pscreen =	SDL_SetVideoMode (owidth, oheight, testbpp, SDL_SWSURFACE);
		if (pscreen == NULL) 
    {
		  printf ("Couldn't set %d*%dx%d video mode: %s\n",	owidth, oheight,3 * 8, SDL_GetError ());
		  exit (1);
		}
    SDL_WM_SetCaption ("OSSIE Web Cam Viewer - Recvr", NULL); //videocap.name
    printf("Done Creating Video Frame\n");
  }
}

void JPEG_VideoViewer_i::configure(const CF::Properties& props) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration)
{
    DEBUG(3, JPEG_VideoViewer, "configure invoked")
    
    std::cout << "props length : " << props.length() << std::endl;

    for (unsigned int i = 0; i <props.length(); i++)
    {
        std::cout << "Property id : " << props[i].id << std::endl;

    }
}

void JPEG_VideoViewer_i::run_loop()
{
    DEBUG(3, JPEG_VideoViewer, "run loop invoked")
    int i = 0;
    short N = 0;
    PortTypes::CharSequence *I_in_0(NULL);
    unsigned char * image_data;
   
    while( true )
    {
      dataIn_0->getData(I_in_0);
      N = I_in_0->length();
      image_data = new unsigned char[N];
      for(i = 0; i < N; i++)
      {
        image_data[i] = (unsigned char) (*I_in_0)[i];
      }
      if(VIDEOMON)
      {  
        refresh_screen(image_data,(unsigned char*)(pscreen->pixels),format,image_width,image_height,owidth,oheight,image_width*image_height*bpp,autobright);
			  if (autobright)
        {
			    //printf("AutoBright\n");
          //adjust_bright(&videopict, fd);
        }      
        SDL_UpdateRect (pscreen, 0, 0, 0, 0);	//update the entire screen
      } 

      dataIn_0->bufferEmptied();
      delete [] image_data;
    }
}

    
