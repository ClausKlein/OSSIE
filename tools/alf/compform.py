#!/usr/bin/env python

## Copyright 2005, 2006, 2007, 2008 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE ALF Waveform Application Visualization Environment
##
## ALF is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## ALF is distributed in the hope that it will be useful, but WITHOUT ANY
## WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE Waveform Developer; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

'''generates a waveform out of a single component
command line inputs: 
1. component name (in /sdr/xml)
2. directory to put the waveform source code
3. waveform name (optional).  if you do not specify waveform name, 
   name will be componentname_waveform'''

try: # mac
    import XML_gen.application_gen as app_gen
    import ComponentClass
    import WaveformClass
    import importResource
except:    # 0.6.2
    import WaveDev.wavedev.XML_gen.application_gen as app_gen
    import WaveDev.wavedev.ComponentClass as ComponentClass
    import WaveDev.wavedev.WaveformClass as WaveformClass
    import WaveDev.wavedev.importResource as importResource

import sys
import os

class compform:
    def __init__(self, comp_in, compNameAndDir, genPath, waveName):
        self.comp_in = comp_in
        self.complist = None
        self.genPath = genPath
        self.waveName = waveName
        self.wavedevPath = compNameAndDir
        self.compNameAndDir = compNameAndDir

    def create(self):
        self.get_the_resource()
        self.create_complist()
        self.create_files()

    def get_the_resource(self):
        '''gets the component in the form of a ComponentClass object'''

        self.component = importResource.getResource(self.compNameAndDir, 
                                                    self.comp_in, 
                                                    self)
  

    def create_complist(self):
        '''Creates a component list out of the single component 
           for the application_gen function in WaveDev.'''
        active_wave = WaveformClass.Waveform()
        
        self.component.AssemblyController = True
        tmp_device = fake_device()

        self.component.device = tmp_device

        #append the single component to the waveform
        active_wave.components.append(self.component)   
        self.complist = active_wave.components

    def create_files(self):

        # generate the sad file:
        app_gen.genxml(self.complist, self.genPath, self.wavedevPath, self.waveName)  

        # generate the DAS file
        app_gen.genDAS(self.complist, self.genPath, self.wavedevPath, self.waveName)   

class fake_device:
    '''this is available so that my component can be assigned to a device'''
    def __init__(self):
        # using the uuid from default_GPP_node
        self.uuid = "5ba336ee-aaaa-aaaa-aaaa-00123f573a7f"


if __name__ == "__main__":
    '''parse the input arguments, and make function calls to 
       create the waveform'''
 
    #check to make sure all the command line arguments are present
    if len(sys.argv) == 1 or len(sys.argv) == 2 or len(sys.argv) > 4:
        print "i'm going to want a component, an install dir and an optional waveform name"
        sys.exit()

    comp_in = sys.argv[1]   #name of the component that will be used
    genPath = sys.argv[2]   #where the generated XML will go

    #if the user did not specify a waveform name, create one
    if len(sys.argv) == 3:
        waveName = comp_in + "_waveform"
    #if the user did set a waveform name, read it from the command line
    elif len(sys.argv) == 4:
        waveName = sys.argv[3] 

    print "waveform name is " + waveName

    #make the directory to put the XML   
    if os.path.exists(genPath+waveName) == False:   
        os.mkdir(genPath+'/'+waveName)

    comp_in = "/sdr/xml/" + comp_in

    my_compform = compform(comp_in, genPath, waveName)

    my_compform.create()

    app_gen.writeWaveSetuppy(genPath, waveName)   # generates a setup.py file


    

   
