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

import sys, os, shutil
from WaveDev.wavedev.errorMsg import *

class genAll:
  def __init__(self, path, wavedevPath, node):
    if path[len(path)-1] != '/':
        path = path + '/'
    self.path = path
    if wavedevPath[len(wavedevPath)-1] != '/':
        wavedevPath = wavedevPath + '/'
    self.wavedevPath = wavedevPath
    self.path = path
    self.node = node

  ##############################################################################
  ## genDirs - this function generates the directory structure for the generated
  ##           code for the waveform; puts required files in main folder
  ##############################################################################
  def genDirs(self):
    if os.path.exists(self.path) == False:
       errorMsg(self,"Node already exists - exiting")
       exit(1)

    if os.path.exists(self.path+self.node.name) == False:
        os.mkdir(self.path + self.node.name)

    shutil.copy(self.wavedevPath + 'generate/reconf',self.path + self.node.name)
    os.chmod(self.path + self.node.name + '/reconf', 0755)

  ##############################################################################
  ## writeMakefiles - generates the make file for the waveform and then calls
  ##                  writeCompMakefile for each seperate component
  ##############################################################################
  def writeMakefile(self):
    output = open(self.path + self.node.name + '/Makefile.am','w')

    Flags = ["-Wall"]
    self.info2str(output,"AM_CXXFLAGS = ",Flags,1)

    tstr = "ossieName = " + self.node.name + '\n\n'
    output.write(tstr)

    tstr = "waveformdir = $(prefix)/nodes/$(ossieName)\n"
    output.write(tstr)

    waveform_data = []
    waveform_data.append("DeviceManager.dcd.xml")
    waveform_data.append("DeviceManager.spd.xml")
    waveform_data.append("DeviceManager.scd.xml")
    waveform_data.append("DeviceManager.prf.xml")

    self.info2str(output,"dist_waveform_DATA = ", waveform_data,1)

    output.close()

  def info2str(self, outfile, staticStr, mylist, extraLine=0,wrapFlag=False):
    tstr = staticStr
    mycount = 0
    wrap = False
    if len(mylist) > 5 or wrapFlag == True:
	wrap = True

    for x in mylist:
      tstr = tstr + x + " "
      mycount += 1
      if mycount%2 == 0 and wrap and mylist.index(x) != len(mylist)-1:
        tstr = tstr + "\\\n"

    tstr = tstr + "\n"
    for x in range(extraLine):
      tstr = tstr + "\n"

    outfile.write(tstr)

  ##############################################################################
  ## genConfigureACFiles - calls writeConfAC for appropriate locations
  ##############################################################################
  def genConfigureACFiles(self,installPath="/sdr/sca"):
    if installPath[-1] == '/':
        installPath = installPath[0:-1]

    tmpPath = self.path + self.node.name + '/'
    self.writeConfAC(tmpPath,self.node.name,False,False,installPath)

  ##############################################################################
  ## writeConfAC - generates configure.ac files for autoconf
  ##############################################################################
  def writeConfAC(self, genPath, name, aceFlag, wavFlag, installPath):
     if genPath[len(genPath)-1] != '/':
        genPath = genPath + '/'

     output = open(genPath + 'configure.ac','w')
     tstr = "AC_INIT(" + name + ", 0.5.0)\n\n"
     tstr += "AM_INIT_AUTOMAKE\n\n"
     tstr += 'AC_PREFIX_DEFAULT("' + installPath + '")\n\n'
     tstr += "AC_PROG_INSTALL\n"
     tstr += "INSTALL_DATA=\"/usr/bin/install -c -m 644\"\n"
     tstr += "AC_SUBST(INSTALL_DATA)\n\n"
     tstr += "AC_CONFIG_FILES(Makefile)\n\n"
     tstr += "AC_OUTPUT\n"
     output.write(tstr)
     output.close()

  ##############################################################################
  ## This function generates the cpp and h files for each component:
  ## component.h, component.cpp, main.cpp, port_impl.h, and port_impl.cpp
  ##############################################################################
  def genCompFiles(self,comp):
      #for x in self.active_wave.components:
        # generate the .h files for each component
        inputH = open(self.wavedevPath + 'generate/sampleComp.h','r')
        outputH = open(self.path + comp.name + "/" + comp.name + ".h",'w')
        self.addGPL(outputH,comp.name)
        for line in inputH.readlines():
          l_out = line.replace("__CLASS_DEF__",comp.name.upper()+"_IMPL_H")
          l_out = l_out.replace("__Class_name__",comp.name+"_i")
          if l_out.find("__PORT_DECL__") != -1:
              self.writePortDecl(outputH,comp)
              continue
          if l_out.find("__ACE_INCLUDES__") != -1:
              if comp.ace == True:
                  l_out = '#include "ace/Task.h"\n'
              else:
                  continue
          if l_out.find("__ACE_INHERIT__") != -1:
              if comp.ace == True:
                  l_out = l_out.replace("__ACE_INHERIT__",", public ACE_Task<ACE_MT_SYNCH>")
              else:
                  l_out = l_out.replace("__ACE_INHERIT__","")
          if l_out.find("__ACE_SVC_DECL__") != -1:
              if comp.ace == True:
                  l_out = l_out.replace("__ACE_SVC_DECL__",'int svc(void);\n        size_t queue_size;')
              else:
                  continue
          if l_out.find("__FRIEND_DECL__") != -1:
              l_out = l_out.replace("__FRIEND_DECL__","")
              self.writeFriendDecl(outputH,comp)
              continue

          outputH.write(l_out)

        inputH.close()
        outputH.close()

        # generate the .cpp files for each component
        inputCPP = open(self.wavedevPath + 'generate/sampleComp.cpp','r')
        outputCPP = open(self.path + comp.name + "/" + comp.name + ".cpp",'w')
        self.addGPL(outputCPP,comp.name)
        for line in inputCPP.readlines():
          l_out = line.replace("__IncludeFile__",comp.name)
          l_out = l_out.replace("__Class_name__",comp.name+"_i")
          #l_out = l_out.replace("__NS_name__","ossie" + comp.name+"Resource")
          if l_out.find("__PORT_INST__") != -1:
              self.writePortInst(outputCPP,comp)
              continue
          if l_out.find("__GET_PORT__") != -1:
              self.writeGetPort(outputCPP,comp)
              continue
          if l_out.find("__DEL_PORT__") != -1:
              self.writeDelPort(outputCPP,comp)
              continue
          if l_out.find("__ACE_SVC_PORTS__") != -1:
              self.writeACESvcPorts(outputCPP,comp)
              continue
          if l_out.find("__ACE_SVC_DEF__") != -1:
              if comp.ace == True:
                  self.writeACESvcDef(outputCPP,comp,'component',comp.timing, comp)
              continue
          outputCPP.write(l_out)

        inputCPP.close()
        outputCPP.close()

        # generate the main.cpp files for each component
        inputMain = open(self.wavedevPath + 'generate/sampleMain.cpp','r')
        outputMain = open(self.path + comp.name + "/main.cpp",'w')
        self.addGPL(outputMain,comp.name)

        for line in inputMain.readlines():
          l_out = line.replace("__IncludeFile__",comp.name)
          l_out = l_out.replace("__Class_name__",comp.name+"_i")
          l_out = l_out.replace("__CLASS_VAR__",comp.name.lower())
          if l_out.find("__CLASS_VAR_ACE__") != -1:
              if comp.ace == True:
                  l_out = l_out.replace("__CLASS_VAR_ACE__",comp.name.lower())
              else:
                  continue
          if l_out.find("__NAME_SPACE__") != -1:
              ns_list = []
              for p in comp.ports:
                  if p.interface.nameSpace not in ns_list:
                      ns_list.append(p.interface.nameSpace)
              l_out = ''
              for tmpns in ns_list:
                  l_out += 'using namespace ' + tmpns + ';\n'

          outputMain.write(l_out)

        inputMain.close()
        outputMain.close()

        # generate the port_impl.h file
        inputPortImpl = open(self.wavedevPath + 'generate/port_impl.h','r')
        outputPortImpl = open(self.path + comp.name + "/port_impl.h",'w')
        self.addGPL(outputPortImpl,comp.name)
        portSample_p = open(self.wavedevPath + 'generate/port_sample_p.h','r')
        portSample_u = open(self.wavedevPath + 'generate/port_sample_u.h','r')
        for line in inputPortImpl.readlines():
            l_out = line.replace("__IncludeFile__",comp.name)
            if l_out.find("__ACE_INCLUDES__") != -1:
              if comp.ace == True:
                  l_out = '#include "ace/Task.h"\n'
              else:
                  continue
            if l_out.find("__TIMING_DECL_AND_INCLUDES__") != -1:
              if comp.timing == True:
                  l_out = 'using namespace std;\n#ifndef time_signal_message_H\n#define time_signal_message_H\ntypedef struct {\n\tchar component_name[255];\n\tchar port_name[255];\n\tchar function_name[255];\n\tchar description[255];\n\tlong time_s;\n\tlong time_us;\n\tlong number_samples;\n} time_signal_message;\n#endif\n'
              else:
                  l_out = ''
            if l_out.find("__PORT_DECL__") != -1:
              self.writePortImplDecl(outputPortImpl,portSample_p,portSample_u,comp)
              continue
            outputPortImpl.write(l_out)

        inputPortImpl.close()
        outputPortImpl.close()
        portSample_p.close()
        portSample_u.close()

        # generate the port_impl.cpp file
        inputPortImpl = open(self.wavedevPath + 'generate/port_impl.cpp','r')
        outputPortImpl = open(self.path + comp.name + "/port_impl.cpp",'w')
        self.addGPL(outputPortImpl,comp.name)
        portSample_p = open(self.wavedevPath + 'generate/port_sample_p.cpp','r')
        portSample_u = open(self.wavedevPath + 'generate/port_sample_u.cpp','r')
        for line in inputPortImpl.readlines():
            l_out = line
            if l_out.find("__PORT_DEF__") != -1:
              self.writePortImplDef(outputPortImpl,portSample_p,portSample_u,comp)
              continue
            outputPortImpl.write(l_out)

        inputPortImpl.close()
        outputPortImpl.close()
        portSample_p.close()
        portSample_u.close()

    # Copy some required files into the main directory
    #  os.system('cp generate/basic_xml/* ' + self.path)
    #  os.system('cp generate/wavLoader.py ' + self.path)

  def writePortImplDecl(self, output,portSample_p,portSample_u,c):
    """ This function writes port implementation declarations for the port_impl.h file"""
    intList = []
    for x in c.ports:
        if x.interface.filename in intList:
            continue
        ts = '#include "' + x.interface.filename + '.h"\n'
        intList.append(x.interface.filename)
        output.write(ts)
    ts = '\n';output.write(ts);
    intList = []
    for x in c.ports:
        if x.interface.name in intList:
            continue
        if x.type == "Uses":
            portSample = portSample_u
        else:
            portSample = portSample_p
        portSample.seek(0)
        intList.append(x.interface.name)
        for line in portSample.readlines():
            l_out = line.replace("__IN_PORT__",x.p_cname)
            l_out = l_out.replace("__INT_TYPE__",x.interface.name)
            l_out = l_out.replace("__NAME_SPACE__",x.interface.nameSpace)
            l_out = l_out.replace("__OUT_PORT__",x.u_cname)
            l_out = l_out.replace("__IN_CLASS__",x.p_cname)
            l_out = l_out.replace("__OUT_CLASS__",x.u_cname)
            if l_out.find("__OPERATION__") != -1:
              self.writeOperation(output,x.interface,port=c)
              continue
            if l_out.find("__ACE_INHERIT__") != -1:
              if c.ace == True:
                  l_out = l_out.replace("__ACE_INHERIT__",", public ACE_Task<ACE_MT_SYNCH>")
              else:
                  l_out = l_out.replace("__ACE_INHERIT__","")
            if l_out.find("__TIMING_BUFFER_LENGTH__") != -1:
	      if (c.timing==True):
	        if (x.interface.name=='timingStatus'):
	          l_out = l_out.replace("__TIMING_BUFFER_LENGTH__",'#define NUMBER_TIMING_MESSAGE_BUFFER	100')
	        else:
	          l_out = l_out.replace("__TIMING_BUFFER_LENGTH__", '');
	      else:
	        l_out = l_out.replace("__TIMING_BUFFER_LENGTH__", '');
            if l_out.find("__TIMING_DECL__") != -1:
	      if (c.timing==True):
	        if (x.interface.name=='timingStatus'):
	          l_out = l_out.replace("__TIMING_DECL__",'void send_timing_message(string component_name, string port_name, string function_name, string description, long number_samples);')
	        else:
	          l_out = l_out.replace("__TIMING_DECL__",'')
	      else:
	        l_out = l_out.replace("__TIMING_DECL__",'')
            if l_out.find("__TIMING_VAR__") != -1:
	      if (c.timing==True):
	        if (x.interface.name=='timingStatus'):
	          l_out = l_out.replace("__TIMING_VAR__",'time_signal_message message_buffer[NUMBER_TIMING_MESSAGE_BUFFER];\n    int message_buffer_write_idx;\n    omni_mutex writing_to_timing_buffer;\n    omni_semaphore *data_is_ready;')
	        else:
	          l_out = l_out.replace("__TIMING_VAR__",'')
	      else:
	        l_out = l_out.replace("__TIMING_VAR__",'')
            if l_out.find("__ACE_SVC_DECL__") != -1:
              if (c.ace == True):
                  l_out = l_out.replace("__ACE_SVC_DECL__",'int svc(void);')
              else:
                  l_out = l_out.replace("__ACE_SVC_DECL__",'')
            if l_out.find("__COMP_ARG__") != -1:
                if c.type == "resource":
                    l_out = l_out.replace("__COMP_ARG__",c.name+"_i *_"+c.name.lower())
                else:
                    l_out = l_out.replace("__COMP_ARG__","")
            if l_out.find("__COMP_REF_DECL__") != -1:
                if c.type == "resource":
                    l_out = l_out.replace("__COMP_REF_DECL__",c.name+"_i *"+c.name.lower()+";")
                else:
                    l_out = l_out.replace("__COMP_REF_DECL__","")

            output.write(l_out)

  def writePortImplDef(self,output,portSample_p,portSample_u,c):
    """ This function writes port implementation definitions for the port_impl.cpp file"""
    intList = []
    for x in c.ports:
        if x.interface.name in intList:
            continue
        if x.type == "Uses":
            portSample = portSample_u
        else:
            portSample = portSample_p
        portSample.seek(0)
        intList.append(x.interface.name)
        for line in portSample.readlines():
            l_out = line.replace("__IN_PORT__",x.p_cname)
            l_out = l_out.replace("__INT_TYPE__",x.interface.name)
            l_out = l_out.replace("__NAME_SPACE__",x.interface.nameSpace)
            l_out = l_out.replace("__OUT_PORT__",x.u_cname)
            if l_out.find("__OPERATION__") != -1:
              l_out = l_out.replace("__OPERATION__",'')
              l_out = l_out.replace("\n",'')
              self.writeOperation(output,x.interface,prefix=l_out,cppFlag=True,in_name=c.name.lower(),using_ace=c.ace,comp=c,port=x)
              continue
            if l_out.find("__ACE_SVC_DEF__") != -1:
              if c.ace == True:
                  self.writeACESvcDef(output,x,'port',c.timing, c)
              continue
            if l_out.find("__TIMING_MESSAGE_DEF__") != -1:
              if (c.timing == True) & (x.interface.name=='timingStatus'):
                  self.writeTimingMessageDef(output,x,'port')
              continue
            if l_out.find("__COMP_ARG__") != -1:
                if c.type == "resource":
                    l_out = l_out.replace("__COMP_ARG__",c.name+"_i *_"+c.name.lower())
                else:
                    l_out = l_out.replace("__COMP_ARG__","")
            if l_out.find("__COMP_REF_DEF__") != -1:
                if c.type == "resource":
                    l_out = l_out.replace("__COMP_REF_DEF__",c.name.lower()+" = _"+c.name.lower()+";")
                else:
                    l_out = l_out.replace("__COMP_REF_DEF__","")
            if l_out.find("__INIT_VARS_DEF__") != -1:
                if (c.type == "resource") & (x.interface.name=='timingStatus'):
                    l_out = l_out.replace("__INIT_VARS_DEF__","message_buffer_write_idx = 0;\n    data_is_ready = new omni_semaphore(0);")
                else:
                    l_out = l_out.replace("__INIT_VARS_DEF__","")
            output.write(l_out)

  def writePortDecl(self, output,c):
    """ This function writes the corba declarations of the ports to the component header file"""
    inCount = 0; outCount=0;
    for x in c.ports:
        if x.type == "Provides":
            ts = " "*8 + x.cname + " " + "*inPort" + str(inCount) + "_servant;\n"
            output.write(ts)
            inCount += 1
    ts = "\n"; output.write(ts)
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*8 + x.cname + " " + "*outPort" + str(outCount) + "_servant;\n"
            output.write(ts)
            outCount += 1
    ts = "\n"; output.write(ts)
    inCount = 0; outCount=0;
    for x in c.ports:
        if x.type == "Provides":
            ts = " "*8 + x.interface.nameSpace + "::" + x.interface.name + "_var " + "inPort" + str(inCount) + "_var;\n"
            output.write(ts)
            inCount += 1
    ts = "\n"; output.write(ts)
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*8 + "CF::Port_var " + "outPort" + str(outCount) + "_var;\n"
            ts += " "*8 + "bool outPort" + str(outCount) + "_active;\n"
            ts += " "*8 + "size_t outPort" + str(outCount) + "_queue_size;\n"
            output.write(ts)
            outCount += 1
    ts = " "*8 + "bool component_alive;\n\n" + " "*8 + "string naming_service_name;\n"; output.write(ts)

  def writePortInst(self,output,c):
    """ This function writes the port instantiations to the component cpp file"""
    inCount = 0; outCount=0;
    for x in c.ports:
        if x.type == "Provides":
            ts = " "*4 + "inPort" + str(inCount) + "_servant" + " = new " + x.cname + "(this);\n"
            output.write(ts)
            ts = " "*4 + "inPort" + str(inCount) + "_var = inPort" + str(inCount)+ "_servant->_this();\n"
            output.write(ts)
            inCount += 1
    ts = "\n"; output.write(ts)
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*4 + "outPort" + str(outCount) + "_servant" + " = new " + x.cname + "(this);\n"
            output.write(ts)
            ts = " "*4 + "outPort" + str(outCount) + "_var = outPort" + str(outCount)+ "_servant->_this();\n"
            ts += " "*4 + "outPort" + str(outCount) + "_active = false;\n"
            ts += " "*4 + "outPort" + str(outCount) + "_queue_size = DEFAULT_QUEUE_BLOCK_SIZE;\n"
            output.write(ts)
            outCount += 1
    ts = "\n"; output.write(ts)
    ts = " "*4 + "queue_size = DEFAULT_QUEUE_BLOCK_SIZE;\n\n" + " "*4 + "component_alive = true;\n\n" + " "*4 + "naming_service_name = label;\n"; output.write(ts)

  def writeGetPort(self,output,c):
    """ This function writes the getPort functionality to the component cpp file"""
    inCount = 0; outCount=0;
    flag = True
    for x in c.ports:
        if x.type == "Provides":
            if flag:
                ts = " "*4 + 'if (strcmp(_id,"' + x.name + '") == 0) {\n'
            else:
                ts = " "*4 + 'else if (strcmp(_id,"' + x.name + '") == 0) {\n'
            output.write(ts)
#            ts = " "*8 + "return inPort" + str(inCount) + "_var;\n"
            ts = " "*8 + "return " + x.interface.nameSpace + "::" + x.interface.name
            ts += "::_duplicate(inPort" + str(inCount) + "_var);\n"
            ts += " "*4 + "}\n"
            output.write(ts)
            inCount += 1
    ts = "\n"; output.write(ts)
    for x in c.ports:
        if x.type == "Uses":
            if flag:
                ts = " "*4 + 'if (strcmp(_id,"' + x.name + '") == 0) {\n'
            else:
                ts = " "*4 + 'else if (strcmp(_id,"' + x.name + '") == 0) {\n'
            output.write(ts)
            ts = " "*8 + "outPort" + str(outCount) + "_active = true;\n"
            ts += " "*8 + "return CF::Port::_duplicate(outPort" + str(outCount) + "_var);\n"
            ts += " "*4 + "}\n"
            output.write(ts)
            outCount += 1
    ts = "\n"; output.write(ts)
    ts = " "*4 + 'return NULL;\n'; output.write(ts)

  def writeDelPort(self,output,c):
    """ This function writes the destructor functionality (for ports) to the component cpp file"""
    inCount = 0; outCount=0;
    flag = True
    for x in c.ports:
        if x.type == "Provides":
            ts = " "*4 + "delete inPort" + str(inCount) + "_servant;\n"
            output.write(ts)
            inCount += 1
    ts = "\n"; output.write(ts)
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*4 + "delete outPort" + str(outCount) + "_servant;\n"
            output.write(ts)
            outCount += 1
    ts = "\n"; output.write(ts)

##  def writeACESvcPorts(self,output,c):
##    """ This function writes the svc port functionality to the component cpp file"""
##    outCount=0;
##    for x in c.ports:
##        if x.type == "Uses":
##            ts = " "*4 + "outPort" + str(outCount) + "_servant->activate();\n"
##            output.write(ts)
##            outCount += 1
##    ts = "\n"; output.write(ts)

  def writeACESvcDef(self, output,c,type,timing_flag, comp=''):
    """ This function writes the implementation of the svn() function for a given component"""
    if type == 'component':
        ts = 'int ' + c.name + '_i::svc(void)\n{\n'
        output.write(ts)
        ts = " "*4 + '/* Start outgoing port threads */\n'
        output.write(ts)
        outCount=0;
        for x in c.ports:
            if x.type == "Uses":
                ts = " "*4 + "outPort" + str(outCount) + "_servant->activate();\n"; output.write(ts)
                outCount += 1
        ts = "\n"; output.write(ts)
        ts = " "*4 + 'std::vector<double> d1_data_double;\n'; output.write(ts)
        ts = " "*4 + 'std::vector<float> d1_data_float;\n'; output.write(ts)
        ts = " "*4 + 'std::vector<short> d1_data_short;\n'; output.write(ts)
        ts = " "*4 + 'std::vector<float> d2_data_double;\n'; output.write(ts)
        ts = " "*4 + 'std::vector<double> d2_data_float;\n'; output.write(ts)
        ts = " "*4 + 'std::vector<short> d2_data_short;\n'; output.write(ts)
        ts = " "*4 + 'ACE_Message_Block *mb;\n'; output.write(ts)
        ts = " "*4 + '/* Main function loop */\n'; output.write(ts)
        ts = " "*4 + 'while(component_alive)\n' + " "*4 + '{\n'; output.write(ts)
	ts = " "*8 + "ACE_Time_Value getq_time_out = ACE_OS::gettimeofday();\n"; output.write(ts)
	ts = " "*8 + "getq_time_out += 1;\n"; output.write(ts)
	ts = " "*8 + "if(getq(mb, &getq_time_out) >= 0) {\n"; output.write(ts)
	ts = " "*12 + "unsigned int buffer_size=mb->length();\n"; output.write(ts)
	ts = " "*12 + "unsigned short data_type;\n"; output.write(ts)
	ts = " "*12 + "ACE_OS::memmove( (char*)&data_type, mb->rd_ptr(), sizeof(unsigned short));\n"; output.write(ts)
	ts = " "*12 + "mb->rd_ptr(sizeof(unsigned short));\n"; output.write(ts)
	ts = " "*12 + "buffer_size=buffer_size - sizeof(unsigned short);\n"; output.write(ts)
	ts = " "*12 + "unsigned int packet_size = 0;\n"; output.write(ts)
	ts = " "*12 + "std::vector<double> data_I;\n"; output.write(ts)
	ts = " "*12 + "std::vector<double> data_Q;\n"; output.write(ts)
	ts = " "*12 + "// I've arbitrarily decided to use doubles as my working type inside the component\n"; output.write(ts)
	ts = " "*12 + "//	the working type is implementation-specific\n"; output.write(ts)
	ts = " "*12 + "switch(data_type) {\n"; output.write(ts)
	ts = " "*16 + "case 1:\n"; output.write(ts)
	ts = " "*20 + "// this is for complex double\n"; output.write(ts)
	ts = " "*20 + "packet_size=buffer_size/(sizeof(double)*2);\n"; output.write(ts)
	ts = " "*20 + "{\n"; output.write(ts)
	ts = " "*24 + "std::vector <double> vals(packet_size*2);\n"; output.write(ts)
	ts = " "*24 + "ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n"; output.write(ts)
	ts = " "*24 + "data_I.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "data_Q.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "for (unsigned int i = 0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*28 + "data_I[i] = vals[i];\n"; output.write(ts)
	ts = " "*28 + "data_Q[i] = vals[i+packet_size];\n"; output.write(ts)
	ts = " "*24 + "}\n"; output.write(ts)
	ts = " "*20 + "}\n"; output.write(ts)
	ts = " "*20 + "break;\n"; output.write(ts)
	ts = " "*16 + "case 2:\n"; output.write(ts)
	ts = " "*20 + "// this is for complex float\n"; output.write(ts)
	ts = " "*20 + "packet_size=buffer_size/(sizeof(float)*2);\n"; output.write(ts)
	ts = " "*20 + "{\n"; output.write(ts)
	ts = " "*24 + "std::vector <float> vals(packet_size*2);\n"; output.write(ts)
	ts = " "*24 + "ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n"; output.write(ts)
	ts = " "*24 + "data_I.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "data_Q.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "for (unsigned int i = 0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*28 + "data_I[i] = vals[i];\n"; output.write(ts)
	ts = " "*28 + "data_Q[i] = vals[i+packet_size];\n"; output.write(ts)
	ts = " "*24 + "}\n"; output.write(ts)
	ts = " "*20 + "}\n"; output.write(ts)
	ts = " "*20 + "break;\n"; output.write(ts)
	ts = " "*16 + "case 3:\n"; output.write(ts)
	ts = " "*20 + "// this is for complex short\n"; output.write(ts)
	ts = " "*20 + "packet_size=buffer_size/(sizeof(short)*2);\n"; output.write(ts)
	ts = " "*20 + "{\n"; output.write(ts)
	ts = " "*24 + "std::vector <short> vals(packet_size*2);\n"; output.write(ts)
	ts = " "*24 + "ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n"; output.write(ts)
	ts = " "*24 + "data_I.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "data_Q.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "for (unsigned int i = 0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*28 + "data_I[i] = vals[i];\n"; output.write(ts)
	ts = " "*28 + "data_Q[i] = vals[i+packet_size];\n"; output.write(ts)
	ts = " "*24 + "}\n"; output.write(ts)
	ts = " "*20 + "}\n"; output.write(ts)
	ts = " "*20 + "break;\n"; output.write(ts)
	ts = " "*16 + "case 4:\n"; output.write(ts)
	ts = " "*20 + "// this is for real double\n"; output.write(ts)
	ts = " "*20 + "packet_size=buffer_size/(sizeof(double));\n"; output.write(ts)
	ts = " "*20 + "{\n"; output.write(ts)
	ts = " "*24 + "std::vector <double> vals(packet_size);\n"; output.write(ts)
	ts = " "*24 + "ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n"; output.write(ts)
	ts = " "*24 + "data_I.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "data_Q.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "for (unsigned int i = 0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*28 + "data_I[i] = vals[i];\n"; output.write(ts)
	ts = " "*28 + "data_Q[i] = 0;\n"; output.write(ts)
	ts = " "*24 + "}\n"; output.write(ts)
	ts = " "*20 + "}\n"; output.write(ts)
	ts = " "*20 + "break;\n"; output.write(ts)
	ts = " "*16 + "case 5:\n"; output.write(ts)
	ts = " "*20 + "// this is for real float\n"; output.write(ts)
	ts = " "*20 + "packet_size=buffer_size/(sizeof(float));\n"; output.write(ts)
	ts = " "*20 + "{\n"; output.write(ts)
	ts = " "*24 + "std::vector <float> vals(packet_size);\n"; output.write(ts)
	ts = " "*24 + "ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n"; output.write(ts)
	ts = " "*24 + "data_I.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "data_Q.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "for (unsigned int i = 0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*28 + "data_I[i] = vals[i];\n"; output.write(ts)
	ts = " "*28 + "data_Q[i] = 0;\n"; output.write(ts)
	ts = " "*24 + "}\n"; output.write(ts)
	ts = " "*20 + "}\n"; output.write(ts)
	ts = " "*20 + "break;\n"; output.write(ts)
	ts = " "*16 + "case 6:\n"; output.write(ts)
	ts = " "*20 + "// this is for real short\n"; output.write(ts)
	ts = " "*20 + "packet_size=buffer_size/(sizeof(short));\n"; output.write(ts)
	ts = " "*20 + "{\n"; output.write(ts)
	ts = " "*24 + "std::vector <short> vals(packet_size);\n"; output.write(ts)
	ts = " "*24 + "ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n"; output.write(ts)
	ts = " "*24 + "data_I.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "data_Q.resize(packet_size);\n"; output.write(ts)
	ts = " "*24 + "for (unsigned int i = 0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*28 + "data_I[i] = vals[i];\n"; output.write(ts)
	ts = " "*28 + "data_Q[i] = 0;\n"; output.write(ts)
	ts = " "*24 + "}\n"; output.write(ts)
	ts = " "*20 + "}\n"; output.write(ts)
	ts = " "*20 + "break;\n"; output.write(ts)
	ts = " "*12 + "}\n"; output.write(ts)
	#ts = " "*8 + "}\n"; output.write(ts)
	ts = " "*12 + "mb->release();\n"; output.write(ts)
	ts = " "*12 + "/*******************************************************************\n"; output.write(ts)
	ts = " "*24 + "Insert functional code here\n"; output.write(ts)
	ts = " "*12 + "*******************************************************************/\n\n"; output.write(ts)
	ts = " "*12 + "/******************************************************************/\n\n"; output.write(ts)
	ts = " "*12 + "// Prepare data for output\n"; output.write(ts)
	ts = " "*12 + "d1_data_double.resize(packet_size);\n"; output.write(ts)
	ts = " "*12 + "d1_data_float.resize(packet_size);\n"; output.write(ts)
	ts = " "*12 + "d1_data_short.resize(packet_size);\n"; output.write(ts)
	ts = " "*12 + "d2_data_double.resize(packet_size*2);\n"; output.write(ts)
	ts = " "*12 + "d2_data_float.resize(packet_size*2);\n"; output.write(ts)
	ts = " "*12 + "d2_data_short.resize(packet_size*2);\n\n"; output.write(ts)
	ts = " "*12 + "for (unsigned int i=0; i<packet_size; i++) {\n"; output.write(ts)
	ts = " "*16 + "d1_data_double[i] = data_I[i];\n"; output.write(ts)
	ts = " "*16 + "d1_data_float[i] = data_I[i];\n"; output.write(ts)
	ts = " "*16 + "d1_data_short[i] = (short)data_I[i];\n"; output.write(ts)
	ts = " "*16 + "d2_data_double[i] = data_I[i];\n"; output.write(ts)
	ts = " "*16 + "d2_data_double[i+packet_size] = data_Q[i];\n"; output.write(ts)
	ts = " "*16 + "d2_data_float[i] = data_I[i];\n"; output.write(ts)
	ts = " "*16 + "d2_data_float[i+packet_size] = data_Q[i];\n"; output.write(ts)
	ts = " "*16 + "d2_data_short[i] = (short)data_I[i];\n"; output.write(ts)
	ts = " "*16 + "d2_data_short[i+packet_size] = (short)data_Q[i];\n"; output.write(ts)
	ts = " "*12 + "}\n"; output.write(ts)
        outCount=0;
        for x in c.ports:
            if (x.type == "Uses") & ((x.interface.name == 'realDouble')|(x.interface.name == 'realFloat')|(x.interface.name == 'realShort')|(x.interface.name == 'complexDouble')|(x.interface.name == 'complexFloat')|(x.interface.name == 'complexShort')):
                ts = " "*12 + "if (outPort" + str(outCount) + "_active) {\n"; output.write(ts)
		if x.interface.name == 'realDouble':
			DATA_TYPE_BEING_USED = 'double'
			VECTOR_COUNT = '1'
			VECTOR_NAME = 'd1_data_double'
		if x.interface.name == 'realFloat':
			DATA_TYPE_BEING_USED = 'float'
			VECTOR_COUNT = '1'
			VECTOR_NAME = 'd1_data_float'
		if x.interface.name == 'realShort':
			DATA_TYPE_BEING_USED = 'short'
			VECTOR_COUNT = '1'
			VECTOR_NAME = 'd1_data_short'
		if x.interface.name == 'complexDouble':
			DATA_TYPE_BEING_USED = 'double'
			VECTOR_COUNT = '2'
			VECTOR_NAME = 'd2_data_double'
		if x.interface.name == 'complexFloat':
			DATA_TYPE_BEING_USED = 'float'
			VECTOR_COUNT = '2'
			VECTOR_NAME = 'd2_data_float'
		if x.interface.name == 'complexShort':
			DATA_TYPE_BEING_USED = 'short'
			VECTOR_COUNT = '2'
			VECTOR_NAME = 'd2_data_short'
                ts = " "*16 + "ACE_Message_Block *message = new ACE_Message_Block (packet_size*" + VECTOR_COUNT + "*sizeof(" + DATA_TYPE_BEING_USED + "));\n"; output.write(ts)
                ts = " "*16 + "message->copy((const char*)&" + VECTOR_NAME + "[0], packet_size*" + VECTOR_COUNT + "*sizeof(" + DATA_TYPE_BEING_USED + "));\n"; output.write(ts)
		ts = " "*16 + "size_t message_length = packet_size*" + VECTOR_COUNT + "*sizeof(" + DATA_TYPE_BEING_USED + ");\n"; output.write(ts)
		ts = " "*16 + "size_t available_space = outPort" + str(outCount) + "_servant->msg_queue()->message_bytes();\n"; output.write(ts)
		ts = " "*16 + "if (available_space<=(outPort" + str(outCount) + "_queue_size+message_length)) {\n"; output.write(ts)
		ts = " "*20 + "outPort" + str(outCount) + "_queue_size+=QUEUE_BLOCK_SIZE;\n"; output.write(ts)
		ts = " "*20 + "outPort" + str(outCount) + "_servant->water_marks (ACE_IO_Cntl_Msg::SET_HWM, outPort" + str(outCount) + "_queue_size);\n"; output.write(ts)
		ts = " "*16 + "}\n"; output.write(ts)
                ts = " "*16 + "if (outPort" + str(outCount) + "_servant->putq(message) == -1) {\n"; output.write(ts)
                ts = " "*20 + "//  this is where a message for issues with the putq would appear\n"; output.write(ts)
                ts = " "*16 + "}\n"; output.write(ts)
                ts = " "*12 + "}\n"; output.write(ts)
                outCount += 1
	ts = " "*8 + "}\n"; output.write(ts)
	ts = " "*8 + "/* Polling rate, slow CPU spinning */\n"; output.write(ts)
	ts = " "*8 + "//ACE_OS::sleep (ACE_Time_Value (1));\n"; output.write(ts)
        ts = " "*4 + '}\n\n' + " "*4 + 'return 0;\n}\n'; output.write(ts)

    if type == 'port':
        #ts = 'int ' + c.u_cname + '::svc(void)\n{\n'; output.write(ts)
        #ts = " "*4 + 'ACE_Message_Block *mb;\n\n'; output.write(ts)
        #ts = " "*4 + 'while(1)\n' + " "*4 + '{\n' + " "*8 + 'if (getq(mb) == -1)\n'
        #output.write(ts)
        #ts = " "*8 + '{\n' + " "*12 + 'ACE_ERROR_RETURN ((LM_ERROR, ' + r'"%p\n",'
        #ts = ts + ' "getq"), -1);\n'
        #output.write(ts)
        #ts = " "*8 + '}\n\n' + " "*8 + '/* _complexShort->pushPacket(); */\n\n'
        #output.write(ts)
        #ts = " "*8 + '/* Release message block */\n' + " "*8 + 'mb->release();\n'
        #output.write(ts)
        #ts = " "*4 + '}\n' + " "*4 + 'return 0;\n}\n'
        #output.write(ts)
		# the following stuff is a work in progress
		#	it needs to be reconciled with the contents of the actual port
		#	This will be interesting for control ports instead of data ports
		#	in the case of control ports, it will likely need a slightly different structure
	#print c.interface.name
        ts = 'int ' + c.u_cname + '::svc(void)\n{\n'; output.write(ts)
	if ((c.interface.name == 'realDouble')|(c.interface.name == 'realFloat')|(c.interface.name == 'realShort')|(c.interface.name == 'complexDouble')|(c.interface.name == 'complexFloat')|(c.interface.name == 'complexShort')):
		ts = " "*4 + 'ACE_Message_Block *mb;\n'; output.write(ts)
		if c.interface.name == 'realDouble':
			DATA_TYPE_BEING_USED = 'double'
			DATA_TYPE_USED = 'Double'
			ARGUMENT_LIST_FOR_PUSH = ' I'
		if c.interface.name == 'realFloat':
			DATA_TYPE_BEING_USED = 'float'
			DATA_TYPE_USED = 'Float'
			ARGUMENT_LIST_FOR_PUSH = ' I'
		if c.interface.name == 'realShort':
			DATA_TYPE_BEING_USED = 'short'
			DATA_TYPE_USED = 'Short'
			ARGUMENT_LIST_FOR_PUSH = ' I'
		if c.interface.name == 'complexDouble':
			DATA_TYPE_BEING_USED = 'double'
			DATA_TYPE_USED = 'Double'
			ARGUMENT_LIST_FOR_PUSH = ' I, Q'
		if c.interface.name == 'complexFloat':
			DATA_TYPE_BEING_USED = 'float'
			DATA_TYPE_USED = 'Float'
			ARGUMENT_LIST_FOR_PUSH = ' I, Q'
		if c.interface.name == 'complexShort':
			DATA_TYPE_BEING_USED = 'short'
			DATA_TYPE_USED = 'Short'
			ARGUMENT_LIST_FOR_PUSH = ' I, Q'
		ts = " "*4 + 'vector < ' + DATA_TYPE_BEING_USED + ' > vals;\n'; output.write(ts)
		ts = " "*4 + 'PortTypes::' + DATA_TYPE_USED + 'Sequence ' + ARGUMENT_LIST_FOR_PUSH +';\n\n'; output.write(ts)
		ts = " "*4 + 'while(1)\n' + " "*8 + '{\n'; output.write(ts)
		ts = " "*8 + 'ACE_Time_Value getq_time_out = ACE_OS::gettimeofday();\n'; output.write(ts)
		ts = " "*8 + 'getq_time_out += 1;\n'; output.write(ts)
		ts = " "*8 + 'if(getq(mb, &getq_time_out) >= 0) {\n'; output.write(ts)
		portCount = 0
		if c.interface.name == 'realDouble':
			NUMBER_OF_VECTORS = '1'
		if c.interface.name == 'realFloat':
			NUMBER_OF_VECTORS = '1'
		if c.interface.name == 'realShort':
			NUMBER_OF_VECTORS = '1'
		if c.interface.name == 'complexDouble':
			NUMBER_OF_VECTORS = '2'
		if c.interface.name == 'complexFloat':
			NUMBER_OF_VECTORS = '2'
		if c.interface.name == 'complexShort':
			NUMBER_OF_VECTORS = '2'
		for individual_port in comp.ports:
			if individual_port.type == "Uses":
				if individual_port.interface.name == 'timingStatus':
					ts = " "*12 + "if (" + comp.name.lower() + "->outPort" + str(portCount) + '_active) {\n'; output.write(ts)
					ts = " "*16 + comp.name.lower() + "->outPort" + str(portCount) + '_servant->send_timing_message(' + comp.name.lower() + '->naming_service_name, "' + c.name + '", "pushPacket", "begin", mb->length()/(sizeof('+ DATA_TYPE_BEING_USED +')*'+ NUMBER_OF_VECTORS +'));\n'; output.write(ts)
					ts = " "*12 + '}\n'; output.write(ts)
				portCount += 1
		ts = " "*12 + 'unsigned int buffer_size=mb->length();\n'; output.write(ts)
		ts = " "*12 + 'unsigned int packet_size=buffer_size/(sizeof(' + DATA_TYPE_BEING_USED + ')*' + NUMBER_OF_VECTORS + ');\n'; output.write(ts)
		ts = " "*12 + 'vals.resize(packet_size*' + NUMBER_OF_VECTORS + ');\n'; output.write(ts)
		if c.interface.name == 'realDouble':
			ts = " "*12 + 'I.length(packet_size);\n'; output.write(ts)
		if c.interface.name == 'realFloat':
			ts = " "*12 + 'I.length(packet_size);\n'; output.write(ts)
		if c.interface.name == 'realShort':
			ts = " "*12 + 'I.length(packet_size);\n'; output.write(ts)
		if c.interface.name == 'complexDouble':
			ts = " "*12 + 'I.length(packet_size);\n'+" "*12 + 'Q.length(packet_size);\n'; output.write(ts)
		if c.interface.name == 'complexFloat':
			ts = " "*12 + 'I.length(packet_size);\n'+" "*12 + 'Q.length(packet_size);\n'; output.write(ts)
		if c.interface.name == 'complexShort':
			ts = " "*12 + 'I.length(packet_size);\n'+" "*12 + 'Q.length(packet_size);\n'; output.write(ts)
		ts = " "*12 + 'ACE_OS::memmove( (char*)&vals[0], mb->rd_ptr(), buffer_size);\n'; output.write(ts)
		ts = " "*12 + 'for (unsigned int i=0; i<packet_size; i++) {\n'; output.write(ts)
		if c.interface.name == 'realDouble':
			ts = " "*16 + 'I[i]=vals[i];\n'; output.write(ts)
		if c.interface.name == 'realFloat':
			ts = " "*16 + 'I[i]=vals[i];\n'; output.write(ts)
		if c.interface.name == 'realShort':
			ts = " "*16 + 'I[i]=vals[i];\n'; output.write(ts)
		if c.interface.name == 'complexDouble':
			ts = " "*16 + 'I[i]=vals[i];\n'; output.write(ts)
			ts = " "*16 + 'Q[i]=vals[i+packet_size];\n'; output.write(ts)
		if c.interface.name == 'complexFloat':
			ts = " "*16 + 'I[i]=vals[i];\n'; output.write(ts)
			ts = " "*16 + 'Q[i]=vals[i+packet_size];\n'; output.write(ts)
		if c.interface.name == 'complexShort':
			ts = " "*16 + 'I[i]=vals[i];\n'; output.write(ts)
			ts = " "*16 + 'Q[i]=vals[i+packet_size];\n'; output.write(ts)
		ts = " "*12 + '}\n'; output.write(ts)
		ts = " "*12 + 'for (unsigned int i = 0; i < outPorts.size(); i++) {\n'; output.write(ts)
		ts = " "*16 + 'outPorts[i].port_var->pushPacket( ' + ARGUMENT_LIST_FOR_PUSH + ' );\n'; output.write(ts)
		ts = " "*12 + '}\n'; output.write(ts)
		portCount = 0
		for individual_port in comp.ports:
			if individual_port.type == "Uses":
				if individual_port.interface.name == 'timingStatus':
					ts = " "*12 + "if (" + comp.name.lower() + "->outPort" + str(portCount) + '_active) {\n'; output.write(ts)
					ts = " "*16 + comp.name.lower() + "->outPort" + str(portCount) + '_servant->send_timing_message(' + comp.name.lower() + '->naming_service_name, "' + c.name + '", "pushPacket", "end", mb->length()/(sizeof('+ DATA_TYPE_BEING_USED +')*'+ NUMBER_OF_VECTORS +'));\n'; output.write(ts)
					ts = " "*12 + '}\n'; output.write(ts)
				portCount += 1
		ts = " "*12 + 'mb->release();\n'; output.write(ts)
		ts = " "*8 + '}\n'; output.write(ts)
    		ts = " "*4 + '}\n' + " "*4 + 'return 0;\n}\n'
    		output.write(ts)
	else:
	        if timing_flag & (c.interface.name=='timingStatus'):
	        	ts = " "*4 + 'dataOut_timingStatus_i *output_port = this;\n'; output.write(ts)
	        	ts = " "*4 + 'int message_buffer_read_idx = 0;\n'; output.write(ts)
	        	ts = " "*4 + '\n'; output.write(ts)
	        	ts = " "*4 + 'while(1) {\n'; output.write(ts)
	        	ts = " "*8 + 'output_port->data_is_ready->wait();\n'; output.write(ts)
	        	ts = " "*8 + 'for (unsigned int i = 0; i < output_port->outPorts.size(); i++) {\n'; output.write(ts)
	        	ts = " "*12 + 'output_port->outPorts[i].port_var->send_timing_event(output_port->message_buffer[message_buffer_read_idx].component_name,\n'; output.write(ts)
	        	ts = " "*16 + 'output_port->message_buffer[message_buffer_read_idx].port_name,\n'; output.write(ts)
	        	ts = " "*16 + 'output_port->message_buffer[message_buffer_read_idx].function_name,\n'; output.write(ts)
	        	ts = " "*16 + 'output_port->message_buffer[message_buffer_read_idx].description,\n'; output.write(ts)
	        	ts = " "*16 + 'output_port->message_buffer[message_buffer_read_idx].time_s,\n'; output.write(ts)
	        	ts = " "*16 + 'output_port->message_buffer[message_buffer_read_idx].time_us,\n'; output.write(ts)
	        	ts = " "*16 + 'output_port->message_buffer[message_buffer_read_idx].number_samples);\n'; output.write(ts)
	        	ts = " "*8 + '}\n'; output.write(ts)
	        	ts = " "*8 + 'message_buffer_read_idx++;\n'; output.write(ts)
	        	ts = " "*8 + 'message_buffer_read_idx = message_buffer_read_idx%NUMBER_TIMING_MESSAGE_BUFFER;\n'; output.write(ts)
	        	ts = " "*4 + '}\n'; output.write(ts)
	        	ts = " "*4 + 'return 0;\n'; output.write(ts)
	        	ts = '}\n'; output.write(ts)
		else:
	        	ts = " "*4 + 'return 0;\n' + '}\n'; output.write(ts)

  def writeTimingMessageDef(self, output,c,type):
    if type == 'port':
    	ts = 'void ' + c.u_cname + '::send_timing_message(string component_name, string port_name, string function_name, string description, long number_samples) {\n'; output.write(ts)
    	ts = " "*4 + 'writing_to_timing_buffer.lock();\n'; output.write(ts)
    	ts = " "*4 + 'struct timeval tv;\n'; output.write(ts)
    	ts = " "*4 + 'struct timezone tz;\n'; output.write(ts)
    	ts = " "*4 + 'gettimeofday(&tv, &tz);\n'; output.write(ts)
    	ts = " "*4 + 'strcpy(message_buffer[message_buffer_write_idx].component_name, component_name.c_str());\n'; output.write(ts)
    	ts = " "*4 + 'strcpy(message_buffer[message_buffer_write_idx].port_name, port_name.c_str());\n'; output.write(ts)
    	ts = " "*4 + 'strcpy(message_buffer[message_buffer_write_idx].function_name, function_name.c_str());\n'; output.write(ts)
    	ts = " "*4 + 'strcpy(message_buffer[message_buffer_write_idx].description, description.c_str());\n'; output.write(ts)
    	ts = " "*4 + 'message_buffer[message_buffer_write_idx].time_s = tv.tv_sec;\n'; output.write(ts)
    	ts = " "*4 + 'message_buffer[message_buffer_write_idx].time_us = tv.tv_usec;\n'; output.write(ts)
    	ts = " "*4 + 'message_buffer[message_buffer_write_idx].number_samples = number_samples;\n'; output.write(ts)
    	ts = " "*4 + 'message_buffer_write_idx++;\n'; output.write(ts)
    	ts = " "*4 + 'message_buffer_write_idx = message_buffer_write_idx%NUMBER_TIMING_MESSAGE_BUFFER;\n'; output.write(ts)
    	ts = " "*4 + 'writing_to_timing_buffer.unlock();\n'; output.write(ts)
    	ts = " "*4 + 'data_is_ready->post();\n'; output.write(ts)
    	ts = '}\n'; output.write(ts)

  def writeOperation(self,output,i,prefix='',cppFlag=False,in_name='',using_ace=False,comp='',port=''):
    """ Writes the declaration or definition of an operation (pushPacket) to
        the port_impl.h and port_impl.cpp files respectively """
    ocount = 0
    for o in i.operations:


        ocount += 1
        if cppFlag:
            if ocount > 1:
                ts = "\n" + o.returnType + ' ' + prefix + o.name + '('
                tscxx = "\n" + o.cxxReturnType + ' ' + prefix + o.name + '('
            else:
                ts = o.returnType + ' ' + prefix + o.name + '('
                tscxx = o.cxxReturnType + ' ' + prefix + o.name + '('
        else:
            ts = prefix + " "*4 + o.returnType + ' ' + o.name + '('
            tscxx = prefix + " "*4 + o.cxxReturnType + ' ' + o.name + '('

        first = True
        for p in o.params:
            _USE_AMPERSAND_ = ''
            _USE_CONST_ = 'const '
            _USE__OUT_ = ''
	    if p.direction == 'out':
                if len(p.dataType) > 8 and p.dataType[-8:] != 'Sequence':
                    _USE_CONST_ = ''
                    _USE_AMPERSAND_ = '&'
                if len(p.dataType) <= 8:
                    _USE_CONST_ = ''
                    _USE_AMPERSAND_ = '&'
	    if p.direction == 'in' and len(p.dataType) > 8 and p.dataType[-8:] == 'Sequence':
                _USE_AMPERSAND_ = '&'
	    if p.direction == 'inout' and len(p.dataType) > 8 and p.dataType[-8:] == 'Sequence':
                _USE_CONST_ = ''
                _USE_AMPERSAND_ = '&'
	    if p.direction == 'out' and len(p.dataType) > 8 and p.dataType[-8:] == 'Sequence':
                _USE__OUT_ = '_out'

            if not first:
                ts += ','
                tscxx += ','
            else:
                first = False
            ts += _USE_CONST_ + p.dataType + _USE__OUT_ + ' ' + _USE_AMPERSAND_ + p.name
            tscxx += p.cxxType + ' ' + p.name
        #if len(o.params) != 0:
        if cppFlag:
            ts += ')\n'
            tscxx += ')\n'
        else:
            ts += ');\n'
            tscxx += ');\n'
#        output.write(ts)
        output.write(tscxx)

        if cppFlag:
		#ts = "{\n" + " "*4 + "unsigned int len = " + "hello" + ".length();\n"; output.write(ts)
            	#ts = "{\n\n" + " "*4 + "/* Data flow and processing goes here */\n\n"; output.write(ts)
		if using_ace:
			if len(o.params)>0:
				if _USE__OUT_ == '' :
					if ((o.params[0].dataType == 'PortTypes::DoubleSequence')|(o.params[0].dataType == 'PortTypes::FloatSequence')|(o.params[0].dataType == 'PortTypes::ShortSequence')):
						portCount = 0
						ts = "{\n"; output.write(ts)
						for individual_port in comp.ports:
							if individual_port.type == "Uses":
								if individual_port.interface.name == 'timingStatus':
									ts = " "*4 + "if (" + comp.name.lower() + "->outPort" + str(portCount) + '_active) {\n'; output.write(ts)
									ts = " "*8 + comp.name.lower() + "->outPort" + str(portCount) + '_servant->send_timing_message(' + comp.name.lower() + '->naming_service_name, "' + port.name + '", "' + o.name + '", "begin", I.length());\n'; output.write(ts)
									ts = " "*4 + '}\n'; output.write(ts)
								portCount += 1
						ts = " "*4 + "unsigned int len = " + o.params[0].name + ".length();\n"; output.write(ts)
						if o.params[0].dataType == 'PortTypes::DoubleSequence':
							TYPE_NAME = 'double';
						if o.params[0].dataType == 'PortTypes::FloatSequence':
							TYPE_NAME = 'float';
						if o.params[0].dataType == 'PortTypes::ShortSequence':
							TYPE_NAME = 'short';
						if len(o.params) == 1:
							NUMBER_VECS = '1'
							if o.params[0].dataType == 'PortTypes::DoubleSequence':
								DATA_TYPE = '4';
							if o.params[0].dataType == 'PortTypes::FloatSequence':
								DATA_TYPE = '5';
							if o.params[0].dataType == 'PortTypes::ShortSequence':
								DATA_TYPE = '6';
						if len(o.params) == 2:
							NUMBER_VECS = '2'
							if o.params[0].dataType == 'PortTypes::DoubleSequence':
								DATA_TYPE = '1';
							if o.params[0].dataType == 'PortTypes::FloatSequence':
								DATA_TYPE = '2';
							if o.params[0].dataType == 'PortTypes::ShortSequence':
								DATA_TYPE = '3';
						ts = " "*4 + "vector <" + TYPE_NAME + "> data_in(len*" + NUMBER_VECS + ");\n"; output.write(ts)
						ts = " "*4 + "char *buffer;\n"; output.write(ts)
						ts = " "*4 + "buffer = new char[len*" + NUMBER_VECS + "*sizeof(" + TYPE_NAME + ")+sizeof(unsigned short)];\n\n"; output.write(ts)
						ts = " "*4 + "for (unsigned int i = 0; i<len; i++) {\n"; output.write(ts)
						if len(o.params) == 1:
							ts = " "*8 + "data_in[i] = " + o.params[0].name + "[i];\n"; output.write(ts)
						if len(o.params) == 2:
							ts = " "*8 + "data_in[i] = " + o.params[0].name + "[i];\n"; output.write(ts)
							ts = " "*8 + "data_in[i+len] = " + o.params[1].name + "[i];\n"; output.write(ts)
						ts = " "*4 + "}\n"; output.write(ts)
						ts = " "*4 + "unsigned short data_type = " + DATA_TYPE + ";\n"; output.write(ts)
						ts = " "*4 + "memcpy(buffer, &data_type, sizeof(unsigned short));\n"; output.write(ts)
						ts = " "*4 + "memcpy(&buffer[sizeof(unsigned short)], (char *)&data_in[0], len*" + NUMBER_VECS + "*sizeof(" + TYPE_NAME + ")+sizeof(unsigned short));\n"; output.write(ts)
						ts = "\n" + " "*4 + "ACE_Message_Block *message = new ACE_Message_Block (len*" + NUMBER_VECS + "*sizeof(" + TYPE_NAME + ")+sizeof(unsigned short));\n"; output.write(ts)
						ts = " "*4 + "message->copy((const char*)&buffer[0], len*" + NUMBER_VECS + "*sizeof(" + TYPE_NAME + ")+sizeof(unsigned short));\n"; output.write(ts)
						ts = " "*4 + "size_t message_length = len*" + NUMBER_VECS + "*sizeof(" + TYPE_NAME + ")+sizeof(unsigned short);\n"; output.write(ts)
						ts = " "*4 + "size_t available_space = " + in_name + "->msg_queue()->message_bytes();\n"; output.write(ts)
						ts = " "*4 + "if (available_space<=(" + in_name + "->queue_size+message_length)) {\n"; output.write(ts)
						ts = " "*8 + "" + in_name + "->queue_size+=QUEUE_BLOCK_SIZE;\n"; output.write(ts)
						ts = " "*8 + "" + in_name + "->water_marks (ACE_IO_Cntl_Msg::SET_HWM," + in_name + "->queue_size);\n"; output.write(ts)
						ts = " "*4 + "}\n"; output.write(ts)
						ts = " "*4 + "if (" + in_name + "->putq(message) == -1) {\n"; output.write(ts)
						ts = " "*8 + "// this is where there would be a message about the putq failing\n"; output.write(ts)
						ts = " "*4 + "}\n"; output.write(ts)
						portCount = 0
						for individual_port in comp.ports:
							if individual_port.type == "Uses":
								if individual_port.interface.name == 'timingStatus':
									ts = " "*4 + "if (" + comp.name.lower() + "->outPort" + str(portCount) + '_active) {\n'; output.write(ts)
									ts = " "*8 + comp.name.lower() + "->outPort" + str(portCount) + '_servant->send_timing_message(' + comp.name.lower() + '->naming_service_name, "' + port.name + '", "' + o.name + '", "end", I.length());\n'; output.write(ts)
									ts = " "*4 + '}\n'; output.write(ts)
								portCount += 1
						ts = " "*4 + "\ndelete buffer;\n}\n"; output.write(ts)
				        	#ts += " "*4 + "/* if using ACE:\n\n" + " "*7
					        #ts += "ACE_Message_Block *mb;\n" + " "*7 + "putq(mb);\n"
	        				#ts += " "*4 + "*/\n\n}\n"
				        	#output.write(ts)
					else:
						ts = "{\n\n}\n"; output.write(ts)
				else:
					ts = "{\n\n}\n"; output.write(ts)
			else:
				ts = "{\n\n}\n"; output.write(ts)
		else:
			ts = "{\n\n}\n"; output.write(ts)

  def writeFriendDecl(self,output,c):
      friendList = []
      for p in c.ports:
          if p.type == "Uses":
              if p.u_cname not in friendList:
                  friendList.append(p.u_cname)
          if p.type == "Provides":
              if p.p_cname not in friendList:
                  friendList.append(p.p_cname)

      for x in friendList:
          ts = " "*4 + "friend class " + x + ";\n"
          output.write(ts)


  def addGPL(self,outFile,name):
      inFile = open(self.wavedevPath + 'generate/gpl_preamble','r')
      for line in inFile.readlines():
          l_out = line.replace("__COMP_NAME__",name)
          outFile.write(l_out)

      inFile.close()


  def cleanUp(self):
      # Move the AssemblyController to the waveform Dir
      for c in self.active_wave.components:
        if c.AssemblyController == True and c.generate:
            shutil.move(self.path + c.name, self.path + self.active_wav.name)
