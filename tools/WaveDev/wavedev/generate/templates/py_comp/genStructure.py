#! /usr/bin/env python

## Copyright 2005, 2006, 2007 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE Waveform Developer.
##
## OSSIE Waveform Developer is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## OSSIE Waveform Developer is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE Waveform Developer; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os, shutil
from WaveDev.wavedev.errorMsg import *

class genAll:
  def __init__(self, path, wavedevPath, active_wave):
    if path[len(path)-1] != '/':
        path = path + '/'
    self.path = path
    if len(wavedevPath) > 0 and wavedevPath[len(wavedevPath)-1] != '/':
        wavedevPath = wavedevPath + '/'
    self.wavedevPath = wavedevPath
    self.active_wave = active_wave



  def writeCompMakefile(self,comp,compPath):
    '''
    ##############################################################################
    ## writeCompMakefile - generates the make file for an indivdual component
    ##############################################################################
    '''

    #copy over the readme file
    shutil.copy(self.wavedevPath + 'generate/templates/py_comp/README', compPath)

    if compPath[len(compPath)-1] != '/':
        compPath = compPath + '/'

    output = open(compPath + 'setup.py','w')
    ts = "\
#! /usr/bin/env python\n\
\n\
from distutils.core import setup\n\
import sys\n\
\n\
install_location = '/sdr/'\n\
\n\
if len(sys.argv) != 2:\n\
	sys.exit(1)\n\
\n\
sys.argv.append('--install-lib='+install_location)\n\n"
    output.writelines(ts)

    ts = "setup(name='" + comp.name + "',\n"
    ts = ts + " "*8 + "description='" + comp.name + "',\n"
    ts = ts + " "*8 + "data_files=[\n"
    ts = ts + " "*16 + "(install_location+'bin/" + comp.name + "',['" + comp.name + ".py', 'WorkModule.py']),\n"

    ts = ts + ' '*16 + "(install_location+'xml/" + comp.name + "',\n"
    ts = ts + ' '*24 + "['" + comp.name + ".prf.xml',\n"
    ts = ts + " "*24 + "'" + comp.name + ".scd.xml', \n"
    ts = ts + " "*24 + "'" + comp.name + ".spd.xml'])])\n"
    output.writelines(ts)

    output.close()   #done creating the file





  def writeConfAC(self, genPath, name, aceFlag, wavFlag, installPath):
    '''
    ##############################################################################
    ## writeConfAC - gets called by ComponentFrame.  python component installation
    ## does not need configure.ac files, so it does not really do anything.  still
    ## needs to exist so that an error does not get thrown in ComponetFrame.py.
    ##############################################################################
    '''
    pass




  #-----------------------------------------------------------------------------
  def genCompFiles(self,comp):
      '''
      ##############################################################################
      ## This function generates the cpp and h files for each component:
      ## component.h, component.cpp, main.cpp, port_impl.h, and port_impl.cpp
      ##############################################################################
      '''

      #-------------------------------------------------------------------------
      '''
      ##########################################################################
      ## generate component .py file
      ##########################################################################
      '''
      #TODO: write more of the code for generting .py file based on component class instance
      input_tmpl = open(self.wavedevPath + 'generate/templates/py_comp/_sampleComp.py', 'r')

      #create the main .py file for the component
      output = open(self.path + comp.name + '/' + comp.name + '.py', 'w')

      #add the generic public license to the beginning of the component main .py file
      self.addGPL(output, comp.name)

      for line in input_tmpl.readlines():
          l_out = line.replace('__CLASS_NAME__',comp.name)
          if l_out.find("__PORT_DECL__") != -1:
              self.writePortDecl(output,comp)
              continue
          if l_out.find("__GET_PORT__") != -1:
              self.writeGetPort(output,comp)
              continue
          if l_out.find("__READ_PROPS__") != -1:
              self.writeReadProps(output,comp)
              continue
          if l_out.find("__REL_MAIN_PROCESS_THREADS__") != -1:
              self.writeReleaseMainProcessThreads(output,comp)
              continue
          if l_out.find("__DEACTIVATE_PORTS__") != -1:
              self.writeDeactivatePorts(output,comp)
              continue
          if l_out.find("__DATA_IN_CLASS_DEFS__") != -1:
              self.writeDataInClassDefs(output,comp)
              continue
          if l_out.find("__DATA_OUT_CLASS_DEFS__") != -1:
              self.writeDataOutClassDefs(output,comp)
              continue
          if l_out.find("__TIMING_MESSAGE_DEF__") != -1:
              self.writeTimingMessageDef(output,comp)
              continue

          output.write(l_out)  #if none of the continue statements have been executed

      input_tmpl.close()
      output.close()

      # TODO: figure out this command
      #os.chmod(self.path + comp.name + '/' + comp.name + '.py', os.X_OK | os.R_OK | os.W_OK)
      #-------------------------------------------------------------------------


      #-------------------------------------------------------------------------
      '''
      ##########################################################################
      ## generate WorkModule.py file
      ##########################################################################
      '''
      #TODO: write all the code for the WorkModule based on component class instance
      input_wm = open(self.wavedevPath + 'generate/templates/py_comp/WorkModule.py', 'r')

      #create the WorkModule.py file for the component
      output_wm = open(self.path + comp.name + '/' + 'WorkModule.py', 'w')

      #add the generic public license to the beginning of the generated WorkModule file
      self.addGPL(output_wm, comp.name)

      for line in input_wm.readlines():
         l_out = line.replace('__CLASS_NAME__',comp.name)

         if l_out.find("__SEND_TO_USES_PORTS__") != -1:
             self.writeSendToUsesPorts(output_wm,comp)
             continue
         output_wm.write(l_out)

      input_wm.close()
      output_wm.close()
      #-----------------------------------------------------------------------------
  #----------------------------------------------------------------------------------





  #-----------------------------------------------------------------------------------
  def writePortDecl(self,output,comp):
    """ This function writes the corba declarations of the ports to the init method"""

    inCount = 0
    for p in comp.ports:
        if p.type == "Provides":
            ts = " "*8 + "self.inPort" + str(inCount) + '_servant = dataIn_complexShort_i(self, "' + p.name + '")\n'
            ts = ts + " "*8 + 'self.inPort' + str(inCount) + '_var = self.inPort' + str(inCount) + '_servant._this()\n\n'
            output.write(ts)
            inCount += 1

    outCount = 0
    for p in comp.ports:
        if p.type == "Uses" and p.name != "send_timing_report":
            ts = " "*8 + 'self.outPort' + str(outCount) + '_servant = dataOut_' + p.interface.name + '_i(self, "' + p.name + '")\n'
            ts = ts + " "*8 + 'self.outPort' + str(outCount) + '_var = self.outPort' + str(outCount) + '_servant._this()\n'
            output.write(ts)
            outCount += 1

    if comp.timing:
        ts = "\n"
        ts = ts + " "*8 + "self.timingPort_servant = dataOut_timingStatus_i(self, 'send_timing_report')\n"
        ts = ts + " "*8 + "self.timingPort_var = self.timingPort_servant._this()\n"
        output.write(ts)
  #-------------------------------------------------------------------------------------

  #-------------------------------------------------------------------------------------
  def writeGetPort(self,output,comp):
    inCount = 0
    for p in comp.ports:
        if p.type == "Provides":
            ts = " "*8 + 'if str(id) == "' + p.name + '":\n'
            ts = ts + " "*12 + 'return ' + 'self.inPort' + str(inCount) + '_var\n'
            output.write(ts)
            inCount += 1

    outCount = 0
    for p in comp.ports:
        if p.type == "Uses" and p.name != "send_timing_report":
            ts = " "*8 + 'if str(id) == "' + p.name + '":\n'
            ts = ts + " "*12 + 'return ' + 'self.outPort' + str(outCount) + '_var\n'
            output.write(ts)
            outCount += 1
        elif p.name == "send_timing_report":
            ts = " "*8 + 'if str(id) == "' + p.name + '":\n'
            ts = ts + " "*12 + 'return ' + 'self.timingPort_var\n'
            output.write(ts)
  #-------------------------------------------------------------------------------------


  #-------------------------------------------------------------------------------------
  def writeReadProps(self,output,comp):
    '''write teh code that will read propeties from the prf file'''
    # TODO: test this method

    # check to make sure there are properties
    # TODO: use a more efficient method
    props_present = False
    for p in comp.properties:
        props_present = True

    # if there are properties present, open up a for loop to cycle through them
    if props_present:
        ts = " "*8 + "for property in props:\n"
        output.write(ts)

    for p in comp.properties:
        ts = " "*12 + "if property not in self.propertySet:\n"; output.write(ts)
        ts = " "*16 + "self.propertySet.append(property)\n"; output.write(ts)

        if p.type == "short" or p.type == "ushort":
            tcast = "int("
        elif p.type == "float" or p.type == "double":
            tcast = "float("
        else:
            print "ERROR.  property type not supported in generate/templates/py_comp/genStructure.writeReadProps"
            return

        if p.elementType == "Simple":
            ts = " "*12 + "if property.id == '" +  p.id + "':\n"; output.write(ts)
            ts = " "*16 + "self." + p.name + " = " + tcast + "property.value.value())\n"; output.write(ts)

        elif p.elementType == "SimpleSequence":
            ts = " "*12 + "if property.id == '" +  p.id + "':\n"; output.write(ts)
            ts = " "*16 + "self." + str(p.name) + " = []\n"; output.write(ts)
            ts = " "*16 + "self." + str(p.name) + ".extend(" + tcast + "[val for val in property.values.value()))\n"; output.write(ts)

        else:
            print "Element types other than simple and simple sequence not supported in writeReadProps in generate/templates/py_comp/genStructure.py"
            return
  #-------------------------------------------------------------------------------------


  #-------------------------------------------------------------------------------------
  def writeReleaseMainProcessThreads(self,output,comp):
    #TODO: comment this method
    #TODO: test this method
    outCount = 0
    for p in comp.ports:
        if p.type == "Uses":
            ts = " "*8 + "self.outPort" + str(outCount) + "_servant.releasePort()\n"
            output.write(ts)
            outCount += 1
  #-------------------------------------------------------------------------------------


  #------------------------------------------------------------------------------------
  def writeDeactivatePorts(self,output,comp):
    #TODO: comment this method
    inCount = 0
    for p in comp.ports:
        if p.type == "Provides":
            ts = " "*8 + "iid" + str(inCount) + " = self.poa.reference_to_id(self.inPort" + str(inCount) + "_var)\n"
            output.write(ts)
            inCount += 1

    outCount = 0
    for p in comp.ports:
        if p.type == "Uses" and p.name != "send_timing_report":
            ts = " "*8 + "oid" + str(outCount) + " = self.poa.reference_to_id(self.outPort" + str(outCount) + "_var)\n"
            output.write(ts)
            outCount += 1

    ts = "\n"; output.write(ts)

    inCount = 0
    for p in comp.ports:
        if p.type == "Provides":
            ts = " "*8 + "self.poa.deactivate_object(iid" + str(inCount) + ")\n"
            output.write(ts)
            inCount += 1

    outCount = 0
    for p in comp.ports:
        if p.type == "Uses" and p.name != "send_timing_report":
            ts = " "*8 + "self.poa.deactivate_object(oid" + str(outCount) + ")\n"
            output.write(ts)
            outCount += 1

    if comp.timing:
        ts = "\n"
        ts = ts + " "*8 + "tid = self.poa.reference_to_id(self.timingPort_var)\n"
        ts = ts + " "*8 + "self.poa.deactivate_object(tid)\n"
        output.write(ts)
  #------------------------------------------------------------------------------------


  #------------------------------------------------------------------------------------
  def writeDataInClassDefs(self,output,comp):
    '''Generates the code for the in port class definitions'''

    def_types_written = " "   #keeps track of the interface names that have been written already so that a certain interface (e.g., complexShort) does not get defined more than once

    for p in comp.ports:
        if p.type == "Provides" and def_types_written.find(p.interface.name) == -1:
            ts = "#------------------------------------------------------------------\n"
            ts = ts + "# dataIn_" + p.interface.name + "_i class definition\n"
            ts = ts + "#------------------------------------------------------------------\n"
            ts = ts + "class dataIn_" + p.interface.name + "_i(" + p.interface.nameSpace + "__POA." + p.interface.name + "):\n"
            ts = ts + " "*4 + "def __init__(self, parent, name):\n"
            ts = ts + " "*8 + "self.parent = parent\n"
            ts = ts + " "*8 + "self.name = name\n\n"
            ts = ts + " "*4 + "# WARNING:  I and Q may have to be changed depending on what data you are receiving (e.g., bytesIn for realChar)\n"
            ts = ts + " "*4 + "def pushPacket(self, I, Q):\n"
            ts = ts + " "*8 + "self.parent.work_mod.AddData(I, Q)\n"
            ts = ts + "\n"
            output.write(ts)

            # the following code assumes one timing port name "timingPort"
            if comp.timing == True:
                ts = " "*8 + "if (self.parent.timingPort_servant.active):\n"
                ts = ts + " "*12 + "self.parent.timingPort_servant.send_timing_message(\n"
                ts = ts + " "*18 + "self.parent.naming_service_name, self.name,\n"
                ts = ts + " "*18 + '"pushPacket", "end", len(I))\n'
                output.write(ts)

            def_types_written = def_types_written + p.interface.name
  #------------------------------------------------------------------------------------


  #------------------------------------------------------------------------------------
  def writeDataOutClassDefs(self,output,comp):
    '''generates the code for the out port class definitions'''
    def_types_written = " "    #keeps track of the interface names that have been written already so that a certain interface (e.g., complexShort) does not get defined more than once
    out_port_count = -1

    for u in comp.ports:
        if u.interface.name == "timingStatus":
            # timing status port definition is written somewhere else
            continue

        if u.type == "Uses" and def_types_written.find(u.interface.name) == -1:
            out_port_count = out_port_count + 1

            ts = "#------------------------------------------------------------------\n"
            ts = ts + "# dataOut_" + u.interface.name + "_i class definition\n"
            ts = ts + "#------------------------------------------------------------------\n"
            ts = ts + "class dataOut_" + u.interface.name + "_i(CF__POA.Port):\n"
            output.write(ts)

            #create the __init__ method
            ts = " "*4 + "def __init__(self, parent, name):\n\
        self.parent = parent\n\
        self.outPorts = {}\n\
        self.name = name\n\
        self.active = False\n\
        \n\
        self.data_buffer = []\n\
        self.data_event = threading.Event()\n\
        self.data_buffer_lock = threading.Lock()\n\
        \n\
        self.is_running = True\n\
        self.process_thread = threading.Thread(target = self.Process)\n\
        self.process_thread.start()\n\n"
            output.write(ts)

            #create connectPort method
            ts = " "*4 + "def connectPort(self, connection, connectionId):\n"
            ts = ts + " "*8 + "port = connection._narrow(" + u.interface.nameSpace + "__POA." + u.interface.name + ")\n"
            ts = ts + " "*8 + "self.outPorts[str(connectionId)] = port\n"
            ts = ts + " "*8 + "self.active = True\n\n"
            output.write(ts)

            #create disconnectPort method
            ts = " "*4 + "def disconnectPort(self, connectionId):\n\
        self.outPorts.pop(str(connectionId))\n\
        if len(self.outPorts)==0:\n\
            self.active = False\n\n"
            output.write(ts)

            #create releasePort method
            ts = " "*4 + "def releasePort(self):\n\
        # shut down the Process thread\n\
        self.is_running = False\n\
        self.data_event.set()\n\n"
            output.write(ts)

            #create send_data method
            ts = " "*4 + "# WARNING:  I and Q may have to be changed depending on what data you are receiving (e.g., bytesIn for realChar)\n\
    def send_data(self, I, Q):\n\
        self.data_buffer_lock.acquire()\n\
        self.data_buffer.insert(0, (I,Q))\n\
        self.data_buffer_lock.release()\n\
        self.data_event.set()\n\n"
            output.write(ts)

            #create Process method
            ts = " "*4 + "def Process(self):\n\
        while self.is_running:\n\
            self.data_event.wait()\n\
            while len(self.data_buffer) > 0:\n\
                self.data_buffer_lock.acquire()\n\
                new_data = self.data_buffer.pop()\n\
                self.data_buffer_lock.release()\n\
                \n\
                for port in self.outPorts.values():\n\
                    port.pushPacket(new_data[0], new_data[1])\n\
                \n\
                self.data_event.clear()\n\n"
            output.write(ts)


            def_types_written = def_types_written + u.interface.name
  #------------------------------------------------------------------------------------



  #------------------------------------------------------------------------------------
  def writeTimingMessageDef(self, output,c):
    ts = ""
    if c.timing == True:
        ts = "\n#------------------------------------------------------------------\n"
        ts = ts + "# dataOut_timingStatus_i class definition\n"
        ts = ts + "#------------------------------------------------------------------\n"
        output.write(ts)
        ts = "\n\
class dataOut_timingStatus_i(CF__POA.Port):\n\
    def __init__(self, parent, name):\n\
        self.parent = parent\n\
        self.outPorts = {}\n\
        self.name = name\n\
        self.active = False\n\
        \n\
        self.message_buffer = []\n\
        self.timing_event = threading.Event()\n\
        self.message_buffer_lock = threading.Lock()\n\
        \n\
        self.is_running = True\n\
        self.process_thread = threading.Thread(target = self.Process)\n\
        self.process_thread.start()\n\
        \n\
    def connectPort(self, connection, connectionId):\n\
        port = connection._narrow(customInterfaces__POA.timingStatus)\n\
        self.outPorts[str(connectionId)] = port\n\
        self.active = True\n\
    \n\
    def disconnectPort(self, connectionId):\n\
        self.outPorts.pop(str(connectionId))\n\
        if len(self.outPorts) == 0:\n\
            self.parent.outPort1_active = False\n\
    \n\
    def releasePort(self):\n\
        # shut down the Process thread\n\
        self.is_running = False\n\
        self.timing_event.set()\n\
        \n\
    def send_timing_message(self, component_name, port_name, function_name, description, number_samples):\n\
        tv = time.time()\n\
        tv_sec = int(tv)\n\
        tv_usec = int((tv-tv_sec)*1000000)\n\
        \n\
        tmpmsg = (str(component_name), str(port_name), str(function_name), str(description), tv_sec, tv_usec, number_samples)\n\
        \n\
        self.message_buffer_lock.acquire()\n\
        self.message_buffer.insert(0, tmpmsg)\n\
        self.message_buffer_lock.release()\n\
        \n\
        self.timing_event.set()\n\
    \n\
    def Process(self):\n\
        while self.is_running:\n\
            self.timing_event.wait()\n\
            while len(self.message_buffer) > 0:\n\
                self.message_buffer_lock.acquire()\n\
                newmsg = self.message_buffer.pop()\n\
                self.message_buffer_lock.release()\n\
                \n\
                for port in self.outPorts.values():\n\
                    port.send_timing_event(newmsg[0], newmsg[1], newmsg[2], newmsg[3], newmsg[4], newmsg[5], newmsg[6])\n\
            \n\
            else:\n\
                self.timing_event.clear()\n\n"
    output.write(ts)
  #------------------------------------------------------------------------------------


  #------------------------------------------------------------------------------------
  def writeSendToUsesPorts(self, output, comp):
      outCount = 0
      for p in comp.ports:
          if p.type == "Uses" and p.name != "send_timing_report":
              ts = " "* 16 + "if self." + comp.name + "_ref.outPort" + str(outCount) + "_servant.active:\n"
              ts = ts + " "*20 + "self." + comp.name + "_ref.outPort" + str(outCount) + "_servant.send_data(newI, newQ)\n\n"
              output.write(ts)
              outCount = outCount + 1
  #------------------------------------------------------------------------------------





  def addGPL(self,outFile,name):
      '''Creates a GPL for the component.  The new GPL will have the component
name.  The new GPL is written to the beginning of the outFile'''

      inFile = open(self.wavedevPath + 'generate/gpl_preamble','r')
      outFile.write('#! /usr/bin/env python\n\n')
      outFile.write("'''\n")
      for line in inFile.readlines():
          l_out = line.replace("__COMP_NAME__",name)
          outFile.write(l_out)
      outFile.write("'''\n\n")
      inFile.close()



