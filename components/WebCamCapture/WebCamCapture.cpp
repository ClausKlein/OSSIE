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


#include <string>
#include <iostream>
#include "WebCamCapture.h"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>




/*from main in spcaview.c*/
const char *videodevice = NULL;
/* default mmap */

	
	int format = VIDEO_PALETTE_JPEG; //VIDEO_PALETTE_YUV420P;
	/******** output screen pointer ***/
	
	unsigned int image_width = IMAGE_WIDTH;
	unsigned int image_height = IMAGE_HEIGHT;
	int owidth = 0;
	int oheight = 0;
	/*********************************/
	/*          Starting Flags       */
//	int i;
	int videoOn = 1;
	int decodeOn =1 ;
	int statOn = 0;
	int audioout = 0;
	int videocomp = 0;
	int channel = 0;
	int norme = 0;
	int autobright = 0;
		
	/*********************************/
	SPCASTATE funct;
	
 
	int bpp = 3;

/*from grab method in spcaview.c*/
  int fd;
	/* default mmap */
	//int i, j, k, nframes = 2000, f, status;
	struct video_mmap vmmap;
	struct video_capability videocap;
	int mmapsize;
	struct video_mbuf videombuf;
	struct video_picture videopict;
	struct video_window videowin;
	struct video_channel videochan;
	struct video_param videoparam;

	
	/******** output screen pointer ***/
	SDL_Surface *pscreen;
	SDL_Event sdlevent;
	/**********************************/
	/*        avi parametres          */
	unsigned char *pFramebuffer;
	int ff;
	int framecount = 0;
	/*********************************/
	/*          Starting Flags       */
	int run = 1;
	int quit = 1;	
	int initAudio = 0; //flag start audio
	int method = 1;
	int streamid ;
	int isVideoChannel = 1;
	int frame_size = 0;
	int len = 0; 
	
	
	/*********************************/
	/* data for SDL_audioin && SDL_audio */
	//SDL_AudioSpec spec, result;
  //SDL_AudioSpec expect;
//  struct Rbuffer RingBuffer;
  int retry = 100;
  int ptread ;
	int ptwrite ;
  int err = 0; 	
	int bytes_per_read =0;
	int testbpp=16;
	/*********************************/
//	RingBuffer.ptread =0;
//  RingBuffer.ptwrite =0;

/**************************/


WebCamCapture_i::WebCamCapture_i(const char *uuid, omni_condition *condition)
  : Resource_impl(uuid), component_running(condition) 
{
    dataOut_0 = new standardInterfaces_i::realChar_u("JPEG_DataOut");


    //Create the thread for the writer's processing function 
    processing_thread = new omni_thread(run, (void *) this);

    //Start the thread containing the writer's processing function 
    processing_thread->start();

}

// Destructor
WebCamCapture_i::~WebCamCapture_i(void)
{   
    delete dataOut_0;
}

// static function for omni thread
void WebCamCapture_i::run( void * data )
{
    ((WebCamCapture_i*)data)->run_loop();
}

CORBA::Object_ptr WebCamCapture_i::getPort( const char* portName ) throw (CORBA::SystemException, CF::PortSupplier::UnknownPort)
{
    DEBUG(3, WebCamCapture, "getPort invoked with port name: " << portName)
    
    CORBA::Object_var p;

    p = dataOut_0->getPort(portName);

    if (!CORBA::is_nil(p))
        return p._retn();

    /*exception*/
    throw CF::PortSupplier::UnknownPort();
}

void WebCamCapture_i::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    DEBUG(3, WebCamCapture, "start invoked")

    		
    isRunning = true; 

}

void WebCamCapture_i::stop() throw (CORBA::SystemException, CF::Resource::StopError) 
{  
    DEBUG(3, WebCamCapture, "stop invoked")
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

void WebCamCapture_i::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    DEBUG(3, WebCamCapture, "releaseObject invoked")
    
    if (audioout) 
    {
		  //SDL_CloseAudioIn(); //stop record 
			printf ("free sound buffer\n");
		}
		printf ("Quiting SDL.\n");
    //printf ("Decoded frames:%d Average decode time: %f\n",framecount, average_decode_time);
		printf ("unmapping\n");
		munmap (pFramebuffer, mmapsize);
	
		printf ("closing\n");
		close (fd);
		printf ("closed\n");

  	printf ("Quiting....\n");
		SDL_Quit ();  
    printf("Done Shutting Down, WebCam\n");
    component_running->signal();
}

void WebCamCapture_i::initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException)
{
  DEBUG(3, WebCamCapture, "initialize invoked")

  int f = 0;
  int bpp = 3;

  //isRunning = false;
  std::cout << "initialize called on WebCam" << std::endl;

  printf ("Initializing SDL.\n");
	
	/* Initialize defaults, Video and Audio */
	if ((SDL_Init (SDL_INIT_VIDEO | SDL_INIT_TIMER) == -1)) 
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
	/* validate parameters */
//	printf ("bpp %d format %d\n", bpp, format);

	if (videodevice == NULL || *videodevice == 0) 
  {
			videodevice = "/dev/video0";
	}
	printf ("Using video device %s.\n", videodevice);
	printf ("Initializing v4l.\n");
		
	//v4l init
	if ((fd = open (videodevice, O_RDWR)) == -1) 
  {
			perror ("ERROR opening V4L interface \n");
			exit (1);
	}
	printf("**************** PROBING CAMERA *********************\n");
	/*Get Video Device Capabilities*/
  if (ioctl (fd, VIDIOCGCAP, &videocap) == -1) 
  {
	  printf ("wrong device\n");
		exit (1);
	}
		
	printf("Camera found: %s \n",videocap.name);
	printf("Camera Type: %d \n", videocap.type);

 /*Get Video Device Video Channel*/
	if (ioctl (fd, VIDIOCGCHAN, &videochan) == -1) 
  {
	  printf ("Hmm did not support Video_channel\n");
		isVideoChannel = 0;
	}
	if (isVideoChannel)
  {
	  videochan.norm = norme;
		videochan.channel = channel;
    /*Set Video Channel and Norm by channel*/
		if (ioctl (fd, VIDIOCSCHAN, &videochan) == -1) 
    {
		  printf ("ERROR setting channel and norme \n");
			exit (1);
		}
	  /************ just to be sure *************/
    /*Not sure if this is doing what he thinks...should check to see if the Channel and Norm got set correctly. */
	  if (ioctl (fd, VIDIOCGCHAN, &videochan) == -1) 
    {
	    printf ("wrong device\n");
		  exit (1);
	  }
	  printf("Bridge found: %s \n",videochan.name);
	  streamid = getStreamId (videochan.name); //find out what type of camera
	
    /*Logitech QuickCam Communicate STX is a JPEG camera*/  
	  if (streamid >= 0)
    {
	    printf("StreamId: %s Camera\n",Plist[streamid].name);
		  /* look a spca5xx webcam try to set the video param struct */
		  spcaPrintParam (fd,&videoparam);
	  } 
    else 
    {
	    printf("StreamId: %d Unknow Camera\n",streamid);
	  } 
	  /* test jpeg capability if not and jpeg ask without raw data 
			set default format to YUVP */
	  if ((format == VIDEO_PALETTE_RAW_JPEG || format == VIDEO_PALETTE_JPEG )&& streamid != JPEG && videoOn) 
    {
	    printf ("Camera unable to stream in JPEG mode switch to YUV420P\n");
		  format = VIDEO_PALETTE_YUV420P;
	  }
	  if(probeSize(videochan.name,&image_width,&image_height) < 0)
		  printf("unable to probe size !!\n");
	}
	printf("*****************************************************\n");
	/* Init grab method mmap */
		
	printf(" grabbing method default MMAP asked \n");
	// MMAP VIDEO acquisition
	memset (&videombuf, 0, sizeof (videombuf));
	if (ioctl (fd, VIDIOCGMBUF, &videombuf) < 0) {
	  perror (" init VIDIOCGMBUF FAILED\n");
	}
	printf ("VIDIOCGMBUF size %d  frames %d  offets[0]=%d offsets[1]=%d\n", videombuf.size, videombuf.frames, videombuf.offsets[0], videombuf.offsets[1]);
			
			pFramebuffer = (unsigned char *) mmap (0, videombuf.size,	PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
			mmapsize = videombuf.size;
			vmmap.height = image_height;
			vmmap.width = image_width;
			vmmap.format = format;
			for (f = 0; f < videombuf.frames; f++) 
      {
				vmmap.frame = f;
				if (ioctl (fd, VIDIOCMCAPTURE, &vmmap)) 
        {
					perror ("cmcapture");
				}
			}
			
      vmmap.frame = 0;
			
				 
			frame_size = image_width * image_height;
		
		/* struct video_picture VIDIOCGPICT VIDIOCSPICT */
		if (ioctl (fd, VIDIOCGPICT, &videopict) < 0) {
			perror ("Couldnt get videopict params with VIDIOCGPICT\n");
		}
			
		videopict.palette = format;
		videopict.depth = bpp * 8;
		//videopict.brightness = INIT_BRIGHT;
		sleep (1);
    /*Set Video Picture Param.*/
		setVideoPict (&videopict, fd);
    
    /*
	   * Initialize the display 
    */
    if ( decodeOn && videoOn )
		{	/* Display data */
      printf("Creating Video Frame...\n");
		  pscreen =	SDL_SetVideoMode (owidth, oheight, testbpp, SDL_SWSURFACE);
		  if (pscreen == NULL) 
      {
			  printf ("Couldn't set %d*%dx%d video mode: %s\n",	owidth, oheight,3 * 8, SDL_GetError ());
			  exit (1);
		  }
      SDL_WM_SetCaption ("OSSIE Web Cam Monitor - Live", NULL); //videocap.name
      printf("Done Creating Video Frame\n");
    }

}

void WebCamCapture_i::configure(const CF::Properties& props) throw (CORBA::SystemException, CF::PropertySet::InvalidConfiguration, CF::PropertySet::PartialConfiguration)
{
    DEBUG(3, WebCamCapture, "configure invoked")
    
    std::cout << "props length : " << props.length() << std::endl;

    for (unsigned int i = 0; i <props.length(); i++)
    {
        std::cout << "Property id : " << props[i].id << std::endl;

        if (strcmp(props[i].id, "DCE:3dd2928a-c369-11db-8bd5-000129227a88") == 0)
        {
            CORBA::Short n;
            props[i].value >>= n;
            quality = n;
            std::cout << "WebCam: Quality (1 - 5): " << quality << std::endl;
            spcaSetQuality(fd, &videoparam, (unsigned char)quality);
        }

    }
}

void WebCamCapture_i::run_loop()
{
    DEBUG(3, WebCamCapture, "run loop invoked")

    PortTypes::CharSequence I_out;
    short N;
    
    tmp = NULL;
    int	i = 0;
    int status;


    while( true )
    {
      N = frame_size;
      I_out.length(N);
      if(isRunning)
      {
        tmp = (unsigned char*)malloc (frame_size);
        //std::cout << "Running...Frame Size: " << frame_size << std::endl; 
        memset(tmp,0x00,frame_size);
        //intime = SDL_GetTicks ();
			  //pictime = intime - delaytime;
			  //delaytime = intime;
			  /* Try to synchronize sound with frame rate */
		  	if (initAudio && i > 9)
        {
				  initAudio = 0;
				  //	SDL_PauseAudioIn(0); // start record
			  }
			  /* compute bytes sound */
			  //if (pictime < 100) 
        //{
			  // bytes_per_read =((AUDIO_SAMPLERATE / 1000) * 2 * pictime);
			  //}
			  //i++;
        ff = vmmap.frame;
        if (ioctl (fd, VIDIOCSYNC, &ff) < 0)
        {
          perror ("cvsync err\n");
        }
        vmmap.frame = ff;
        memcpy (tmp, pFramebuffer +	videombuf.offsets[vmmap.frame],	frame_size);
			  if ((status = ioctl (fd, VIDIOCMCAPTURE, &vmmap)) < 0) 
        {
          //std::cout << "VIDEOCMCAPTURE" << std::endl;
				  perror ("cmcapture");
				  printf (">>cmcapture err %d\n", status);
			  }
        vmmap.frame =	(vmmap.frame + 1) % videombuf.frames;
				 
		    //	synctime = SDL_GetTicks ();
			  /*here the frame is in tmp ready to used */

        //Send WebCam->tmp (unsigned char*) out to packetizer 

        /*This just updates the OSSIE WebCam Monitor - Live*/
        //if ( decodeOn && videoOn && (i > 10))
			 // {	
          //std::cout << "Update OSSIE WebCam Monitor - Live" << std::endl;
          refresh_screen(tmp,(unsigned char*)(pscreen->pixels),format,image_width,image_height,owidth,oheight,image_width*image_height*bpp,autobright);
			    if (autobright)
          {
			      // printf("AutoBright\n");
            adjust_bright(&videopict, fd);
          }
          //decodetime = SDL_GetTicks ();
          SDL_UpdateRect (pscreen, 0, 0, 0, 0);	//update the entire screen		
       // }  
        //else 
       // {
			    //decodetime = SDL_GetTicks ();
			 // }
      int y = 0;
      for(y = 0; y < N; y++)
      {
        I_out[y] = tmp[y];
      }
      //std::cout << "Data Transmitted length: " << N << std::endl;

      dataOut_0->pushPacket(I_out);
      free(tmp);
      //usleep(400000);
      }
      else
      {
             
      }
    }
}

    
