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
try:
    from WaveDev.wavedev.errorMsg import *
except ImportError:
    print "ERROR: basic_ports/genStructure.py could not import WaveDev module"
    print "  - Is /sdr/tools included in ossie.pth?"
    sys.exit(0)

class genAll:
  def __init__(self, path, wavedevPath, active_wave):
    if path[len(path)-1] != '/':
        path = path + '/'
    self.path = path
    if len(wavedevPath) > 0 and wavedevPath[len(wavedevPath)-1] != '/':
        wavedevPath = wavedevPath + '/'
    self.wavedevPath = wavedevPath
    self.active_wave = active_wave

  ##############################################################################
  ## genDirs - this function generates the directory structure for the generated
  ##           code for the waveform; puts required files in main folder
  ##############################################################################
  def genDirs(self):
    if os.path.exists(self.path) == False:
       errorMsg(self,"Waveform already exists - exiting")
       exit(1)

    if os.path.exists(self.path+self.active_wave.name) == False:
        os.mkdir(self.path + self.active_wave.name)

    shutil.copy(self.wavedevPath + 'generate/reconf',self.path + self.active_wave.name)
    os.chmod(self.path + self.active_wave.name + '/reconf', '0755')
    for x in os.listdir(self.wavedevPath + 'generate/basic_xml/'):
        if not os.path.isdir(x):
            shutil.copy(self.wavedevPath + 'generate/basic_xml/' + x,self.path + self.active_wave.name)

    for x in self.active_wave.components:
        if x.generate:
            if os.path.exists(self.path+x.name) == False:
                os.mkdir(self.path+x.name)
            if x.AssemblyController != True:
                shutil.copy(self.wavedevPath + 'generate/reconf',self.path + x.name)
                os.chmod(self.path + x.name + '/reconf', 0755)
                for f in os.listdir(self.wavedevPath + 'generate/basic_xml/'):
                    if not os.path.isdir(f):
                        shutil.copy(self.wavedevPath + 'generate/basic_xml/' + f,self.path + x.name)
                shutil.copy(self.wavedevPath + 'generate/LICENSE',self.path + x.name)

  ##############################################################################
  ## writeMakefiles - generates the make file for the waveform and then calls
  ##                  writeCompMakefile for each seperate component
  ##############################################################################
  def writeMakefiles(self,DevMan_flag):
    output = open(self.path + self.active_wave.name + '/Makefile.am','w')

    Flags = ["-Wall"]
    self.info2str(output,"AM_CXXFLAGS = ",Flags,1)

    tstr = "ossieName = " + self.active_wave.name + '\n\n'
    output.write(tstr)

    tstr = "SUBDIRS = "
    for c in self.active_wave.components:
        if c.AssemblyController == True and c.generate:
            tstr += c.name + '\n\n'
            output.write(tstr)

#    tstr = "waveformdir = $(prefix)/dom/waveforms/$(ossieName)\n"
    tstr = "waveformdir = $(prefix)/waveforms/" + self.active_wave.name + "\n"
    output.write(tstr)

    waveform_data = []
    waveform_data.append(self.active_wave.name + ".sad.xml")
    waveform_data.append(self.active_wave.name + "_DAS.xml")
    # If there is only one node - then install device manager files as well
    if DevMan_flag:
        waveform_data.append("DeviceManager.dcd.xml")
        waveform_data.append("DeviceManager.spd.xml")
        waveform_data.append("DeviceManager.scd.xml")
        waveform_data.append("DeviceManager.prf.xml")
    waveform_data.append("DomainManager.dmd.xml")
    waveform_data.append("DomainManager.spd.xml")
    waveform_data.append("DomainManager.scd.xml")
    waveform_data.append("DomainManager.prf.xml")

    self.info2str(output,"dist_waveform_DATA = ", waveform_data,1)

    output.close()

    for c in self.active_wave.components:
        if c.generate:
            tmpPath = self.path + c.name
            self.writeCompMakefile(c,tmpPath)

  ##############################################################################
  ## writeCompMakefilee - generates the make file for an indivdual component
  ##############################################################################
  def writeCompMakefile(self,comp,compPath):
    if compPath[len(compPath)-1] != '/':
        compPath = compPath + '/'

    Flags = ["-Wall"]

    output = open(compPath + 'Makefile.am','w')
    self.info2str(output,"AM_CXXFLAGS = ",Flags,1)

    tstr = "bin_PROGRAMS = " + comp.name + "\n\n"
    output.write(tstr)

    tstr = comp.name + "_SOURCES = " + comp.name + ".cpp " + comp.name + ".h main.cpp\n\n"
    output.write(tstr)
    tstr = "ossieName = " + comp.name + "\n"
    output.write(tstr)

    tstr = "xmldir = $(prefix)/xml/$(ossieName)\n"
    output.write(tstr)

    tstr = "bindir = $(prefix)/bin\n"
    output.write(tstr)

    tstr2 = comp.name

    xmlData = []
    xmlData.append(tstr2 + ".prf.xml")
    xmlData.append(tstr2 + ".scd.xml")
    xmlData.append(tstr2 + ".spd.xml")
    self.info2str(output,"dist_xml_DATA = ",xmlData,1,wrapFlag=True)

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
  def genConfigureACFiles(self,installPath):
    if installPath[-1] == '/':
        installPath = installPath[0:-1]

    tmpPath = self.path + self.active_wave.name + '/'
    self.writeConfAC(tmpPath,self.active_wave.name,self.active_wave.ace,True,installPath)

    for c in self.active_wave.components:
        if c.AssemblyController ==  True or not c.generate:
            continue
        tmpPath = self.path + c.name + '/'
        self.writeConfAC(tmpPath,c.name,c.ace,False,installPath)

  ##############################################################################
  ## writeConfAC - generates configure.ac files for autoconf
  ##############################################################################
  def writeConfAC(self,genPath,name,aceFlag,wavFlag,installPath="/sdr"):
     if genPath[len(genPath)-1] != '/':
        genPath = genPath + '/'

     output = open(genPath + 'configure.ac','w')
     tstr = "AC_INIT(" + name + ", 0.6.0)\nAM_INIT_AUTOMAKE\n\n"
     output.write(tstr)
     #tstr = 'AC_PREFIX_DEFAULT("/sdr")\n\n'
     tstr = 'AC_PREFIX_DEFAULT("' + installPath + '")\n\n'
     output.write(tstr)
     tstr = "AC_PROG_CXX\nAC_PROG_INSTALL\nAC_PROG_MAKE_SET\n\n"
     output.write(tstr)
     tstr = "AC_HEADER_SYS_WAIT\n\nAC_FUNC_FORK\n\n"
     output.write(tstr)
     #tstr = "AC_HAVE_XERCES_C\nAC_CORBA_ORB\nAC_CORBA_OMNIEVENTS\n\n"
     #tstr = "AC_CORBA_ORB\n\n"
     #output.write(tstr)

     tstr = 'AC_LANG_PUSH([C++])\n\n'
     output.write(tstr)

     tstr = 'AC_CHECK_LIB([omniORB4], [main], [], [AC_MSG_ERROR([cannot find omniORBi4 library])])\n'
     output.write(tstr)
     tstr = 'AC_CHECK_LIB([omnithread], [main], [], [AC_MSG_ERROR([cannot find omnithread library])])\n'
     output.write(tstr)
     tstr = 'AC_CHECK_LIB([omniDynamic4], [main], [], [AC_MSG_ERROR([cannot find omniDynamic4 library])])\n'
     output.write(tstr)
     tstr = 'AC_CHECK_HEADERS([omniORB4/CORBA.h], [], [AC_MSG_ERROR([cannot find omniORB4 header files])])\n\n'
     output.write(tstr)
     tstr = 'AC_CHECK_LIB([standardInterfaces], [main], [], [AC_MSG_ERROR([cannot find standardInterfaces])])\n'
     output.write(tstr)
     tstr = 'AC_CHECK_HEADERS([standardinterfaces/complexShort.h], [], [AC_MSG_ERROR([cannot find standardInterfaces header files])])\n\n'
     output.write(tstr)

     # TODO: Add support for sigproc
     if False:
         tstr = 'AC_CHECK_LIB([sigproc], [main], [], [AC_MSG_ERROR([cannot find sigproc library])])\n'
         output.write(tstr)
         tstr = 'AC_CHECK_HEADERS([sigproc/SigProc.h], [], [AC_MSG_ERROR([cannot find sigproc library header files])])\n\n'
         output.write(tstr)

     tstr = 'AC_LANG_POP\n\n'
     output.write(tstr)


     tstr = 'export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig"\n'
     output.write(tstr)
     tstr = "PKG_CHECK_MODULES(OSSIE, ossie >= 0.6.0,,exit)\n"
     output.write(tstr)
     tstr = 'CXXFLAGS="$CXXFLAGS $OSSIE_CFLAGS"\n'
     output.write(tstr)
     tstr = 'IDL_FLAGS="$OSSIE_CFLAGS"\nAC_SUBST(IDL_FLAGS)\n\n'
     output.write(tstr)

     if aceFlag == True:
         tstr = 'PKG_CHECK_MODULES(ACE, ACE >= 5.4.7)\n'
         tstr = tstr + 'AC_SUBST(ACE_CFLAGS)\nAC_SUBST(ACE_LIBS)\nLIBS="$LIBS $ACE_LIBS"\n\n'
         output.write(tstr)

     tstr = 'LIBS="$LIBS $OSSIE_LIBS"\n\n'
     output.write(tstr)

     tstr = 'AC_SUBST(SI_PATH)\n\n'
     output.write(tstr)

     tstr = "AC_CONFIG_FILES(Makefile"
     if wavFlag == True:
        for x in self.active_wave.components:
            if x.AssemblyController and x.generate:
                tstr2 = " " + x.name + "/Makefile"
                tstr = tstr + tstr2

     tstr = tstr + ")\n\n"
     output.write(tstr)

     tstr = "AC_OUTPUT\n"
     output.write(tstr)

     output.close()

  ##############################################################################
  ## This function generates the cpp and h files for each component:
  ## component.h, component.cpp, main.cpp, port_impl.h, and port_impl.cpp
  ##############################################################################
  def genCompFiles(self,comp):
      #for x in self.active_wave.components:
        # generate the .h files for each component
        inputH = open(self.wavedevPath + 'generate/templates/basic_ports/sampleComp.h','r')
        outputH = open(self.path + comp.name + "/" + comp.name + ".h",'w')
        self.addGPL(outputH,comp.name)
        for line in inputH.readlines():
          l_out = line.replace("__CLASS_DEF__",comp.name.upper()+"_IMPL_H")
          l_out = l_out.replace("__Class_name__",comp.name+"_i")
          if l_out.find("__SI_BASES__") != -1:
              self.writeInterfaceBaseIncludes(outputH,comp)
              continue
          if l_out.find("__USES_SI__") != -1:
              self.writeInterfaceUIncludes(outputH,comp)
              continue
          if l_out.find("__PROVIDES_SI__") != -1:
              self.writeInterfacePIncludes(outputH,comp)
              continue
          if l_out.find("__PORT_DECL__") != -1:
              self.writePortDecl(outputH,comp)
              continue
          if l_out.find("__CORBA_SIMPLE_PROP_DECL__") != -1:
              self.writeCORBASimplepropDeclarations(outputH,comp)
              continue
          if l_out.find("__CORBA_SIMPLE_SEQUENCE_PROP_DECL__") != -1:
              self.writeCORBASimpleSequencepropDeclarations(outputH,comp)
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
                  l_out = l_out.replace("__ACE_SVC_DECL__",'int svc(void);')
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
        inputCPP = open(self.wavedevPath + 'generate/templates/basic_ports/sampleComp.cpp','r')
        outputCPP = open(self.path + comp.name + "/" + comp.name + ".cpp",'w')
        self.addGPL(outputCPP,comp.name)
        for line in inputCPP.readlines():
          l_out = line.replace("__IncludeFile__",comp.name)
          l_out = l_out.replace("__ComponentName__",comp.name)
          l_out = l_out.replace("__Class_name__",comp.name +"_i")
          #l_out = l_out.replace("__NS_name__","ossie" + comp.name+"Resource")
          if l_out.find("__CONSTRUCTORS__") != -1:
              self.writePortConstructors(outputCPP,comp)
              continue
          if l_out.find("__PORT_DESTRUCTORS__") != -1:
              self.writePortDestructors(outputCPP,comp)
              continue
          if l_out.find("__SIMPLE_SEQUENCE_POINTER_DESTRUCTORS__") != -1:
              self.writeSimpleSequencePointerDestructors(outputCPP,comp)
              continue
          if l_out.find("__PORT_INST__") != -1:
              self.writePortInst(outputCPP,comp)
              continue
          if l_out.find("__GET_PORT__") != -1:
              self.writeGetPort(outputCPP,comp)
              continue
          if l_out.find("__READ_PROPS__") !=-1:
              self.writeReadProps(outputCPP,comp)
              continue
          if l_out.find("__PROCESS_DATA_DECLARATIONS__") != -1:
              self.writeProcessDataDeclaration(outputCPP,comp)
              continue
          if l_out.find("__PROCESS_DATA_LOOP__") != -1:
              self.writeProcessDataLoop(outputCPP,comp)
              continue
          if l_out.find("__ACE_SVC_PORTS__") != -1:
              self.writeACESvcPorts(outputCPP,comp)
              continue
          if l_out.find("__ACE_SVC_DEF__") != -1:
              if comp.ace == True:
                  self.writeACESvcDef(outputCPP,comp,'component')
              continue
          outputCPP.write(l_out)

        inputCPP.close()
        outputCPP.close()

        # generate the main.cpp files for each component
        inputMain = open(self.wavedevPath + 'generate/templates/basic_ports/sampleMain.cpp','r')
        outputMain = open(self.path + comp.name + "/main.cpp",'w')
        self.addGPL(outputMain,comp.name)

        for line in inputMain.readlines():
          l_out = line.replace("__IncludeFile__",comp.name)
          l_out = l_out.replace("__ComponentName__",comp.name)
          l_out = l_out.replace("__Class_name__",comp.name+"_i")
          l_out = l_out.replace("__CLASS_VAR__",comp.name.lower())
          if l_out.find("__CLASS_VAR_ACE__") != -1:
              if comp.ace == True:
                  l_out = l_out.replace("__CLASS_VAR_ACE__",comp.name.lower())
              else:
                  continue
          outputMain.write(l_out)

        inputMain.close()
        outputMain.close()

        # generate the Doxygen documentation.txt file
        inputDoc = open(self.wavedevPath + 'generate/templates/basic_ports/sampleDocumentation.txt','r')
        outputDoc = open(self.path + comp.name + '/documentation.txt','w')
        self.addGPL(outputDoc, comp.name)

        for line in inputDoc.readlines():
            l_out = line.replace("__ComponentName__", comp.name)
            outputDoc.write(l_out)
        inputDoc.close()
        outputDoc.close()

        # generate the Doxygen configure file
        inputDoxy = open(self.wavedevPath + 'generate/templates/basic_ports/sampleDoxyfile','r')
        outputDoxy = open(self.path + comp.name + '/Doxyfile','w')

        for line in inputDoxy.readlines():
            l_out = line.replace("__ComponentName__", comp.name)
            outputDoxy.write(l_out)
        inputDoxy.close()
        outputDoxy.close()

#--------------------------------------------------------------------------------------------
#############################################################################################


        ##code for generating port_impl.h and .cpp files has been temporarily
        ##commented out. this code should be rewritten to put port_impl
        ##functionality into the appropriate .cpp function
##        # generate the port_impl.h file
##        inputPortImpl = open(self.wavedevPath + 'generate/port_impl.h','r')
##        outputPortImpl = open(self.path + comp.name + "/port_impl.h",'w')
##        self.addGPL(outputPortImpl,comp.name)
##        portSample = open(self.wavedevPath + 'generate/port_sample.h','r')
##        for line in inputPortImpl.readlines():
##            l_out = line.replace("__IncludeFile__",comp.name)
##            if l_out.find("__ACE_INCLUDES__") != -1:
##              if comp.ace == True:
##                  l_out = '#include "ace/Task.h"\n'
##              else:
##                  continue
##            if l_out.find("__PORT_DECL__") != -1:
##              self.writePortImplDecl(outputPortImpl,portSample,comp)
##              continue
##            outputPortImpl.write(l_out)
##
##        inputPortImpl.close()
##        outputPortImpl.close()
##        portSample.close()
##
##        # generate the port_impl.cpp file
##        inputPortImpl = open(self.wavedevPath + 'generate/port_impl.cpp','r')
##        outputPortImpl = open(self.path + comp.name + "/port_impl.cpp",'w')
##        self.addGPL(outputPortImpl,comp.name)
##        portSample = open(self.wavedevPath + 'generate/port_sample.cpp','r')
##        for line in inputPortImpl.readlines():
##            l_out = line
##            if l_out.find("__PORT_DEF__") != -1:
##              self.writePortImplDef(outputPortImpl,portSample,comp)
##              continue
##            outputPortImpl.write(l_out)
##
##        inputPortImpl.close()
##        outputPortImpl.close()
##        portSample.close()

    # Copy some required files into the main directory
    #  os.system('cp ' + self.wavedevPath + 'generate/basic_xml/* ' + self.path)
    #  os.system('cp ' + self.wavedevPath + 'generate/wavLoader.py ' + self.path)
####################################################################################################
#---------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------
###################################################################################
  def writeInterfaceBaseIncludes(self,output,c):
    """ This function writes the corba declarations of the base types for the ports"""
    compShort = 0
    compFloat = 0
    compDouble = 0
    compChar = 0
    compLong = 0

    realShort = 0
    realFloat = 0
    realDouble = 0
    realChar = 0
    realLong = 0

    for x in c.ports:
        if x.interface.name == "complexShort" and compShort == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            compShort += 1
        elif x.interface.name == "complexFloat" and compFloat == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            compFloat += 1
        elif x.interface.name == "complexDouble" and compDouble == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            compDouble += 1
        elif x.interface.name == "complexChar" and compChar == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            compChar += 1
        elif x.interface.name == "complexLong" and compLong == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            compLong += 1

        elif x.interface.name == "realShort" and realShort == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            realShort += 1
        elif x.interface.name == "realFloat" and realFloat == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            realFloat += 1
        elif x.interface.name == "realDouble" and realDouble == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            realDouble += 1
        elif x.interface.name == "realChar" and realChar == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            realChar += 1
        elif x.interface.name == "realLong" and realLong == 0:
            ts = '#include "standardinterfaces/' + x.interface.name + '.h"\n'
            output.write(ts)
            realLong += 1

        else:
            continue
###################################################################################
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
###################################################################################
  def writeInterfaceUIncludes(self,output,c):
    """ This function writes the corba declarations of the uses ports to the component header file"""
    compShort = 0
    compFloat = 0
    compDouble = 0
    compChar = 0
    compLong = 0

    realShort = 0
    realFloat = 0
    realDouble = 0
    realChar = 0
    realLong = 0

    for x in c.ports:
        if x.type == "Uses":
            if x.interface.name == "complexShort" and compShort == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                compShort += 1
            elif x.interface.name == "complexFloat" and compFloat == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                compFloat += 1
            elif x.interface.name == "complexDouble" and compDouble == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                compDouble += 1
            elif x.interface.name == "complexChar" and compChar == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                compChar += 1
            elif x.interface.name == "complexLong" and compLong == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                compLong += 1


            elif x.interface.name == "realShort" and realShort == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                realShort += 1
            elif x.interface.name == "realFloat" and realFloat == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                realFloat += 1
            elif x.interface.name == "realDouble" and realDouble == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                realDouble += 1
            elif x.interface.name == "realChar" and realChar == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                realChar += 1
            elif x.interface.name == "realLong" and realLong == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_u.h"\n';
                output.write(ts)
                realLong += 1

            else:
                continue

##################################################################################
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
###################################################################################
  def writeInterfacePIncludes(self,output,c):
    """ This function writes the corba declarations of the provides ports to the component header file"""
    compShort = 0;
    compFloat = 0;
    compDouble = 0;
    compChar = 0;
    compLong = 0;

    realShort = 0;
    realFloat = 0;
    realDouble = 0;
    realChar = 0;
    realLong = 0;


    inCount = 0;
    for x in c.ports:
        if x.type == "Provides":
            if x.interface.name == "complexShort" and compShort == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                compShort += 1
            elif x.interface.name == "complexFloat" and compFloat == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                compFloat += 1
            elif x.interface.name == "complexDouble" and compDouble == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                compDouble += 1
            elif x.interface.name == "complexChar" and compChar == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                compChar += 1
            elif x.interface.name == "complexLong" and compLong == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                compLong += 1


            elif x.interface.name == "realShort" and realShort == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                realShort += 1
            elif x.interface.name == "realFloat" and realFloat == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                realFloat += 1
            elif x.interface.name == "realDouble" and realDouble == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                realDouble += 1
            elif x.interface.name == "realShort" and realShort == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                realShort += 1
            elif x.interface.name == "realChar" and realChar == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                realChar += 1
            elif x.interface.name == "realLong" and realLong == 0:
                ts = '#include "standardinterfaces/' + x.interface.name + '_p.h"\n';
                output.write(ts)
                realLong += 1

            else:
                continue

###################################################################################
#---------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
##################################################################################


#  def writePortImplDecl(self, output,portSample,c):
#    """ This function writes port implementation declarations for the port_impl.h file"""
#    intList = []
#    for x in c.ports:
#        if x.interface.filename in intList:
#            continue
#        ts = '#include "' + x.interface.filename + '.h"\n'
#        intList.append(x.interface.filename)
#        output.write(ts)
#    ts = '\n';output.write(ts);
#    intList = []
#    for x in c.ports:
#        if x.interface.name in intList:
#            continue
#        portSample.seek(0)
#        intList.append(x.interface.name)
#        for line in portSample.readlines():
#            l_out = line.replace("__IN_PORT__",x.p_cname)
#            l_out = l_out.replace("__INT_TYPE__",x.interface.name)
#            l_out = l_out.replace("__NAME_SPACE__",x.interface.nameSpace)
#            l_out = l_out.replace("__OUT_PORT__",x.u_cname)
#            l_out = l_out.replace("__IN_CLASS__",x.p_cname)
#            l_out = l_out.replace("__OUT_CLASS__",x.u_cname)
#            if l_out.find("__OPERATION__") != -1:
#              self.writeOperation(output,x.interface)
#              continue
#            if l_out.find("__ACE_INHERIT__") != -1:
#              if c.ace == True:
#                  l_out = l_out.replace("__ACE_INHERIT__",", public ACE_Task<ACE_MT_SYNCH>")
#              else:
#                  l_out = l_out.replace("__ACE_INHERIT__","")
#            if l_out.find("__ACE_SVC_DECL__") != -1:
#              if c.ace == True:
#                  l_out = l_out.replace("__ACE_SVC_DECL__",'int svc(void);')
#              else:
#                  continue
#            if l_out.find("__COMP_ARG__") != -1:
#                if c.type == "resource":
#                    l_out = l_out.replace("__COMP_ARG__",c.name+"_i *_"+c.name.lower())
#                else:
#                    l_out = l_out.replace("__COMP_ARG__","")
#            if l_out.find("__COMP_REF_DECL__") != -1:
#                if c.type == "resource":
#                    l_out = l_out.replace("__COMP_REF_DECL__",c.name+"_i *"+c.name.lower()+";")
#                else:
#                    l_out = l_out.replace("__COMP_REF_DECL__","")
#
#            output.write(l_out)

#################################################################################################################
#----------------------------------------------------------------------------------------------------------------


#availableTypes = ["boolean", "char", "double", "float", "short", "long","objref", "octet", "string", "ulong","ushort"]



#---------------------------------------------------------------------------------
#################################################################################

  def writeCORBASimplepropDeclarations(self,output,c):
    simpleCount = 0;
    for x in c.properties:
        tmp_type = str(x.type)

        if x.elementType == "Simple":
            ts = " "*8 + "CORBA::" + tmp_type.capitalize() + " simple_" + str(simpleCount) + "_value;\n";
            output.write(ts)
            simpleCount += 1;
        else:
            continue

###################################################################################
#----------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
#################################################################################

  def writeCORBASimpleSequencepropDeclarations(self,output,c):
    simplesequenceCount = 0;
    for x in c.properties:
        tmp_type = str(x.type)

        if x.elementType == "SimpleSequence":
            ts = " "*8 + "CORBA::" + tmp_type.capitalize() + "Seq *simplesequence_" + str(simplesequenceCount) + ";\n"
            output.write(ts)
            simplesequenceCount = simplesequenceCount + 1
        else:
            continue

################################################################################
#-------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------
###############################################################################################################

#  def writePortImplDef(self,output,portSample,c):
#    """ This function writes port implementation definitions for the port_impl.cpp file"""
#    intList = []
#    for x in c.ports:
#        if x.interface.name in intList:
#            continue
#        portSample.seek(0)
#        intList.append(x.interface.name)
#        for line in portSample.readlines():
#            l_out = line.replace("__IN_PORT__",x.p_cname)
#            l_out = l_out.replace("__INT_TYPE__",x.interface.name)
#            l_out = l_out.replace("__NAME_SPACE__",x.interface.nameSpace)
#            l_out = l_out.replace("__OUT_PORT__",x.u_cname)
#            if l_out.find("__OPERATION__") != -1:
#              l_out = l_out.replace("__OPERATION__",'')
#              l_out = l_out.replace("\n",'')
#              self.writeOperation(output,x.interface,prefix=l_out,cppFlag=True,in_name=c.name,using_ace=c.ace)
#              continue
#            if l_out.find("__ACE_SVC_DEF__") != -1:
#              if c.ace == True:
#                  self.writeACESvcDef(output,x,'port')
#              continue
#            if l_out.find("__COMP_ARG__") != -1:
#                if c.type == "resource":
#                    l_out = l_out.replace("__COMP_ARG__",c.name+"_i *_"+c.name.lower())
#                else:
#                    l_out = l_out.replace("__COMP_ARG__","")
#            if l_out.find("__COMP_REF_DEF__") != -1:
#                if c.type == "resource":
#                    l_out = l_out.replace("__COMP_REF_DEF__",c.name.lower()+" = _"+c.name.lower()+";")
#                else:
#                    l_out = l_out.replace("__COMP_REF_DEF__","")
#            output.write(l_out)
###############################################################################################################
#-------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------
###############################################################################################################

  def writePortDecl(self, output,c):
    """ This function writes the corba declarations of the ports to the component header file"""
    inCount = 0; outCount=0;
    for x in c.ports:
        if x.type == "Provides":
            ts = " "*8 + "standardInterfaces_i::" + x.interface.name + "_p *dataIn_" + str(inCount) + ";\n";
            output.write(ts)
            inCount += 1
        elif x.type == "Uses":
            ts = " "*8 + "standardInterfaces_i::" + x.interface.name + "_u *dataOut_" + str(outCount) + ";\n";
            output.write(ts)
            outCount += 1
        else:
            continue

###############################################################################################################
#-------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------
###############################################################################################################

#  def writePortInst(self,output,c):
#    """ This function writes the port instantiations to the component cpp file"""
#    inCount = 0; outCount=0;
#    for x in c.ports:
#        if x.type == "Provides":
#            ts = " "*4 + "inPort" + str(inCount) + "_servant" + " = new " + x.cname + "(this);\n"
#            output.write(ts)
#            ts = " "*4 + "inPort" + str(inCount) + "_var = inPort" + str(inCount)+ "_servant->_this();\n"
#            output.write(ts)
#            inCount += 1
#    ts = "\n"; output.write(ts)
#    for x in c.ports:
#        if x.type == "Uses":
#            ts = " "*4 + "outPort" + str(outCount) + "_servant" + " = new " + x.cname + "(this);\n"
#            output.write(ts)
#            ts = " "*4 + "outPort" + str(outCount) + "_var = outPort" + str(outCount)+ "_servant->_this();\n"
#            ts += " "*4 + "outPort" + str(outCount) + "_active = false;\n"
#            output.write(ts)
#            outCount += 1
#    ts = "\n"; output.write(ts)
#    ts = " "*4 + "component_alive = true;\n"; output.write(ts)

#---------------------------------------------------------------------------------
##################################################################################

  def writeGetPort(self,output,c):
    """ This function writes the getPort functionality to the component cpp file"""
    inCount = 0; outCount=0;
    flag = True
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*4 + "p = dataOut_" + str(outCount) + "->getPort(portName);\n"; output.write(ts)
            outCount += 1;
        elif x.type == "Provides":
            ts = " "*4 + "p = dataIn_" + str(inCount) + "->getPort(portName);\n"; output.write(ts)
            inCount += 1;
        else:
            continue

        ts = "\n"; output.write(ts)
        ts = " "*4 + "if (!CORBA::is_nil(p))\n"; output.write(ts)
        ts = " "*8 + "return p._retn();\n\n"; output.write(ts)

    ts = " "*4 + '/*exception*/\n'; output.write(ts)
    ts = " "*4 + 'throw CF::PortSupplier::UnknownPort();\n'; output.write(ts)
#################################################################################
#----------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
###############################################################################

  def writePortConstructors(self,output,c):
    inCount = 0;
    outCount = 0;
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*4 + 'dataOut_' + str(outCount) + ' = new standardInterfaces_i::';
            ts = ts + str(x.interface.name) + '_u("' + x.name + '");\n';
            output.write(ts)
            outCount += 1;
        elif x.type == "Provides":
            ts = " "*4 + 'dataIn_' + str(inCount) + ' = new standardInterfaces_i::';
            ts = ts + str(x.interface.name) + '_p("' + x.name + '");\n';
            output.write(ts)
            inCount += 1;
        else:
            continue

###################################################################################
#----------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
##################################################################################
  def writePortDestructors(self,output,c):
    inCount = 0;
    outCount = 0;
    for x in c.ports:
        if x.type == "Uses":
            ts = " "*4 + 'delete dataOut_' + str(outCount) + ';\n';
            output.write(ts)
            outCount += 1;

        elif x.type == "Provides":
            ts = " "*4 + 'delete dataIn_' + str(inCount) + ';\n';
            output.write(ts)
            inCount += 1;
        else:
            continue
##################################################################################
#-------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
###################################################################################

  def writeSimpleSequencePointerDestructors(self,output,c):
    simplesequenceCount = 0;
    for x in c.properties:
        tmp_type = str(x.type)

        if x.elementType == "SimpleSequence":
            ts = " "*4 + "delete []simplesequence_" + str(simplesequenceCount) + ";\n"
            output.write(ts)
            simplesequenceCount += 1;
        else:
            continue

###################################################################################
#--------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
###################################################################################

  def writeReadProps(self,output,c):
    """write the code that will read properties from the prf file"""
    simpleCount = 0;
    simplesequenceCount = 0;
    #make sure there are properties first

    ts = " "*4 + 'std::cout << "props length : " << props.length() << std::endl;\n\n'
    ts = ts + " "*4 + "for (unsigned int i = 0; i <props.length(); i++)\n"
    ts = ts + " "*4 + "{\n"; output.write(ts)
    ts = " "*8 + 'std::cout << "Property id : " << props[i].id << std::endl;\n\n'
    output.write(ts)

    for p in c.properties:

        ts = " "*8 + 'if (strcmp(props[i].id, "' + p.id + '") == 0)\n' + " "*8 + "{\n";output.write(ts)

        if p.elementType == "Simple":
            tmp_type = "unsupported_type";
            if p.type == "short":
                tmp_type = "Short";
            elif p.type == "ushort":
                tmp_type = "UShort";
            elif p.type == "float":
                tmp_type = "Float";
            elif p.type == "double":
                tmp_type = "Double";
            else:
                print "ERROR: " + p.type + " is not supported in basic_ports/genStructure"
                return

            ts = " "*12 + "CORBA::" + str(tmp_type) + " simple_temp;\n";
            output.write(ts)
            ts = " "*12 + 'props[i].value >>= simple_temp;\n';
            ts = ts + " "*12 + 'simple_' + str(simpleCount) + '_value = simple_temp;\n';
            ts = ts + " "*8 + "}\n\n"
            output.write(ts)
            simpleCount += 1;

        elif p.elementType == "SimpleSequence":
            tmp_type = "unsupported_type";
            if p.type == "short":
                tmp_type = "Short";
            elif p.type == "ushort":
                tmp_type = "UShort";
            elif p.type == "float":
                tmp_type = "Float";
            elif p.type == "double":
                tmp_type = "Double";
            else:
                print "ERROR: " + p.type + " is not supported in basic_ports/genStructure"
                return

            ts = " "*12 + "props[i].value >>= simplesequence_" + str(simplesequenceCount) + ";\n";
            output.write(ts)

            ts = " "*8 + "}\n\n"        # close the if statement
            output.write(ts)

            simplesequenceCount += 1;
        else:
            print "WARNING: properties other than simple and simple sequence are not supported yet"
            continue

    ts = " "*4 + "}\n"; output.write(ts)  #closes the for loop

#################################################################################
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
#################################################################################


  def writeProcessDataDeclaration(self,output,c):
    """This function sets up the majority of the process data function (in the .cpp file) based on the port type"""

    outPort_present = False
    inPort_present = False
    inCount = 0;
    outCount = 0;
    #declare the output (uses) variables
    for x in c.ports:  #assumes that you have at least one port
        if x.type == "Uses":

            if x.interface.name == "complexShort":
                ts = " "*4 + "PortTypes::ShortSequence I_out_" + str(outCount) + ", Q_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;

            elif x.interface.name == "complexFloat":
                ts = " "*4 + "PortTypes::FloatSequence I_out_" + str(outCount) + ", Q_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;

            elif x.interface.name == "complexDouble":
                ts = " "*4 + "PortTypes::DoubleSequence I_out_" + str(outCount) + ", Q_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;

            elif x.interface.name == "complexChar":
                ts = " "*4 + "PortTypes::CharSequence I_out_" + str(outCount) + ", Q_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;

            elif x.interface.name == "complexLong":
                ts = " "*4 + "PortTypes::LongSequence I_out_" + str(outCount) + ", Q_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;


            elif x.interface.name == "realShort":
                ts = " "*4 + "PortTypes::ShortSequence I_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;
            elif x.interface.name == "realFloat":
                ts = " "*4 + "PortTypes::FloatSequence I_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;
            elif x.interface.name == "realDouble":
                ts = " "*4 + "PortTypes::DoubleSequence I_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;

            elif x.interface.name == "realChar":
                ts = " "*4 + "PortTypes::CharSequence I_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;
            elif x.interface.name == "realLong":
                ts = " "*4 + "PortTypes::LongSequence I_out_" + str(outCount) + ";\n";
                output.write(ts)
                outCount += 1;



            else:
                print "\nInterfaces other than complex and real Short, Float, Char, long and Double are not supported yet in the process data function generation!!\n  See writeProcessDataDeclaration in genStructure.\n"
            #declare input values short, shortsequence, float, floatSequence, unsupported
                continue
    ts = "\n";
    output.write(ts)

    #declare input (provides) values based on interface type
    for x in c.ports:
        if x.type == "Provides":

            if x.interface.name == "complexShort":
                ts = "\n" + " "*4 + "PortTypes::ShortSequence *I_in_"+str(inCount)+"(NULL), *Q_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length, Q_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexFloat":
                ts = "\n" + " "*4 + "PortTypes::FloatSequence *I_in_"+str(inCount)+"(NULL), *Q_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length, Q_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexDouble":
                ts = "\n" + " "*4 + "PortTypes::DoubleSequence *I_in_"+str(inCount)+"(NULL), *Q_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length, Q_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexChar":
                ts = "\n" + " "*4 + "PortTypes::CharSequence *I_in_"+str(inCount)+"(NULL), *Q_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length, Q_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexLong":
                ts = "\n" + " "*4 + "PortTypes::LongSequence *I_in_"+str(inCount)+"(NULL), *Q_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length, Q_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;


            elif x.interface.name == "realShort":
                ts = "\n" + " "*4 + "PortTypes::ShortSequence *I_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realFloat":
                ts = "\n" + " "*4 + "PortTypes::FloatSequence *I_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realDouble":
                ts = "\n" + " "*4 + "PortTypes::DoubleSequence *I_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realChar":
                ts = "\n" + " "*4 + "PortTypes::CharSequence *I_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realLong":
                ts = "\n" + " "*4 + "PortTypes::LongSequence *I_in_"+str(inCount)+"(NULL);\n";
                output.write(ts)
                ts = " "*4 + "CORBA::UShort I_in_" + str(inCount) + "_length;\n";
                output.write(ts)
                inCount += 1;


            else:
                print "\nInterfaces other than real/complex Float, short, Long, char, and double are not supported yet in the process data function generation!!\nSee writeProcessDataDeclaration in genStructure."
            #only one provides port is supported at this point
                continue

###################################################################################
#----------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#################################################################################


  def writeProcessDataLoop(self,output,c):
    """This function sets up the majority of the process data function (in the .cpp file) based on the port type"""
    inCount = 0;
    outCount = 0;
    ts = " "*4 + "while(1)\n" + " "*4 + "{\n";
    output.write(ts)

    #define input (provides) values input to them and get length on each loop
    for x in c.ports:
        if x.type == "Provides":
            if x.interface.name == "complexShort":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+", Q_in_"+str(inCount) + ");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n";
                output.write(ts)
                ts = " "*8 + "Q_in_" + str(inCount) + "_length = Q_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexFloat":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+", Q_in_"+str(inCount) + ");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n";
                output.write(ts)
                ts = " "*8 + "Q_in_" + str(inCount) + "_length = Q_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexDouble":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+", Q_in_"+str(inCount) + ");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n";
                output.write(ts)
                ts = " "*8 + "Q_in_" + str(inCount) + "_length = Q_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexChar":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+", Q_in_"+str(inCount) + ");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n";
                output.write(ts)
                ts = " "*8 + "Q_in_" + str(inCount) + "_length = Q_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "complexLong":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+", Q_in_"+str(inCount) + ");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n";
                output.write(ts)
                ts = " "*8 + "Q_in_" + str(inCount) + "_length = Q_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realShort":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realFloat":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realDouble":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realChar":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;
            elif x.interface.name == "realLong":
                ts = " "*8 + "dataIn_"+str(inCount)+"->getData(I_in_"+str(inCount)+");\n\n";
                output.write(ts)
                ts = " "*8 + "I_in_" + str(inCount) + "_length = I_in_" + str(inCount) + "->length();\n\n";
                output.write(ts)
                inCount += 1;


            else:
                print "\nInterfaces other than complex/real Short,  Float, Char, Long and Double are not supported yet in the process data function generation!!\nSee writeProcessDataLoop in genStructure.\n"
                continue

    for x in c.ports:
        if x.type == "Uses":
            if x.interface.name == "complexShort" or x.interface.name == "complexFloat" or x.interface.name == "complexDouble" or x.interface.name == "complexChar" or x.interface.name == "complexLong":
                ts = " "*8 + "I_out_" + str(outCount) + ".length(); //must define length of output\n";
                output.write(ts)
                ts = " "*8 + "Q_out_" +  str(outCount) + ".length(); //must define length of output\n\n";
                output.write(ts)
                outCount += 1;



            elif x.interface.name == "realShort" or x.interface.name == "realFloat" or x.interface.name == "realDouble" or x.interface.name == "realChar" or x.interface.name == "realLong":
                ts = " "*8 + "I_out_" + str(outCount) + ".length(); //must define length of output\n\n";
                output.write(ts)
                outCount += 1;

            else:
                print "\nInterfaces other than complex/real Short, Float, Char, Long and Double are not supported yet in the process data function generation!!\nSee writeProcessDataLoop in genStructure.\n"
            #declare input values short, shortsequence, float, floatSequence, unsupported
                continue

    ts = " "*8 + "/*insert code here to do work*/\n\n\n\n\n\n\n";
    output.write(ts)

    inCount = 0;
    for x in c.ports:
        if x.type == "Provides":
            if x.interface.name == "complexShort" or x.interface.name == "complexFloat" or x.interface.name == "complexDouble" or x.interface.name == "complexChar" or x.interface.name == "complexLong":
                ts = " "*8 + "dataIn_" + str(inCount) + "->bufferEmptied();\n";
                output.write(ts)
                inCount += 1;

            elif x.interface.name == "realShort" or x.interface.name == "realFloat" or x.interface.name == "realDouble" or x.interface.name == "realChar" or x.interface.name == "realLong":
                ts = " "*8 + "dataIn_" + str(inCount) + "->bufferEmptied();\n";
                output.write(ts)
                inCount += 1;

            else:
                print "\nInterfaces other than complexand real Short, Char, long, FLoat and Double are not supported yet in the process data function generation!!\nSee writeProcessDataLoop in genStructure.\n"
                continue

    outCount = 0;
    for x in c.ports:  #assumes that you have at least one port
        if x.type == "Uses":
            if x.interface.name == "complexShort" or x.interface.name == "complexFloat" or x.interface.name == "complexDouble" or x.interface.name == "complexChar" or x.interface.name == "complexLong":
                ts = " "*8 + "dataOut_" + str(outCount) + "->pushPacket(I_out_" + str(outCount) + ", Q_out_" + str(outCount) + ");\n";
                output.write(ts)
                outCount += 1;

            elif x.interface.name == "realShort" or x.interface.name == "realFloat" or x.interface.name == "realDouble" or x.interface.name == "realChar" or x.interface.name == "realLong":

                ts = " "*8 + "dataOut_" + str(outCount) + "->pushPacket(I_out_" + str(outCount) + ");\n";
                output.write(ts)
                outCount += 1;

            else:
                print "\nInterfaces other than complex and real Short, Float, char, long, and Double are not supported yet in the process data function generation!!\nSee writeProcessDataLoop in genStructure.\n"
            continue
            #declare input values short, shortsequence, float, floatSequence, unsupported
    #close the infinate while loop

    ts = " "*4 + "}\n"; output.write(ts)

##################################################################################
#---------------------------------------------------------------------------------




  def writeACESvcDef(self, output,c,type):
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
        ts = " "*12 + "//    the working type is implementation-specific\n"; output.write(ts)
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

        outCount=0

        for x in c.ports:
            if x.type == "Uses":
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
                ts = " "*16 + "if (outPort" + str(outCount) + "_servant->putq(message) == -1) {\n"; output.write(ts)
                ts = " "*20 + "//  this is where a message for issues with the putq would appear\n"; output.write(ts)
                ts = " "*16 + "}\n"; output.write(ts)
                ts = " "*12 + "}\n"; output.write(ts)
                outCount += 1
        ts = " "*8 + "}\n"; output.write(ts)
        ts = " "*8 + "/* Polling rate, slow CPU spinning */\n"; output.write(ts)
        ts = " "*8 + "ACE_OS::sleep (ACE_Time_Value (1));\n"; output.write(ts)
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
        #    it needs to be reconciled with the contents of the actual port
        #    This will be interesting for control ports instead of data ports
        #    in the case of control ports, it will likely need a slightly different structure
    #print c.interface.name
        ts = 'int ' + c.u_cname + '::svc(void)\n{\n'; output.write(ts)
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
    ts = " "*12 + 'unsigned int buffer_size=mb->length();\n'; output.write(ts)
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
    ts = " "*12 + 'mb->release();\n'; output.write(ts)
    ts = " "*8 + '}\n'; output.write(ts)
    ts = " "*4 + '}\n' + " "*4 + 'return 0;\n}\n'
    output.write(ts)


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
            os.system('mv ' + self.path + c.name + ' ' + self.path + self.active_wave.name)


