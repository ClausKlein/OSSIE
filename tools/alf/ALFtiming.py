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

from omniORB import CORBA
import CosNaming

try:   # mac 
    import customInterfaces__POA
    import standardInterfaces__POA
    import CF, CF__POA

except:    # 0.6.2
    import ossie.standardinterfaces.standardInterfaces__POA as standardInterfaces__POA
    import ossie.custominterfaces.customInterfaces__POA as customInterfaces__POA
    import ossie.cf.CF as CF 
    import ossie.cf.CF__POA as CF__POA

import time, threading, sys

last_time = 0 # used so ALF won't kill the waverform when it exits
class my_timing_structure(customInterfaces__POA.timingStatus):
    def __init__(self, orb, parent):
        self.orb = orb
        self.parent = parent
        if not hasattr(parent, "processTimingEvent"):
            print "Calling function does not support timing events"
            sys.exit(1)

    def send_timing_event(self, component_name, port_name, function_name, description, time_s, time_us, number_samples):
        #print "Component name: " + component_name
        #print "Port name: " + port_name
        #print "Time(s): " + str(time_s)
        #print "Time(us): " + str(time_us)
        #print "Description: " + description
        #print "-----------------------"
        self.parent.processTimingEvent(str(component_name),str(port_name),
            str(function_name),str(description), long(time_s),long(time_us),long(number_samples))
        last_time = time.time()

class TimingDisplay:
    def __init__(self, waveform_naming_context_text, parent):
        self.connected_ports = []
        self.orb = None
        
        self.createTimingPortList(waveform_naming_context_text)
        
        # Create the orb
        self.timing_struct = my_timing_structure(self.orb,parent)
        obj_poa = self.orb.resolve_initial_references("RootPOA")
        poaManager = obj_poa._get_the_POAManager()
        poaManager.activate()
        obj_poa.activate_object(self.timing_struct)

        for porthandle in self.connected_ports:
            porthandle.connectPort(self.timing_struct._this(), "thisismyconnectionid_timing")

    def createTimingPortList(self, waveform_naming_context_text):
        self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        obj = self.orb.resolve_initial_references("NameService")
    
        rootContext = obj._narrow(CosNaming.NamingContext)
  
        if rootContext is None:
            print "Failed to narrow the root naming context"
            sys.exit(1)
    
        #name = [CosNaming.NameComponent("DomainName1","")]
        name = [CosNaming.NameComponent("DomainName1",""),
                CosNaming.NameComponent(waveform_naming_context_text,"")]

        #domain_context = obj2._narrow(CosNaming.NamingContext);
        
        #name2 = [CosNaming.NameComponent(waveform_naming_context_text,"")]
        #obj3 = domain_context.resolve(name2)
        
        try:
            wav_obj = rootContext.resolve(name)
    
        except:
            print waveform_naming_context_text + " could not be found"
            sys.exit(1)
        
        waveform_context = wav_obj._narrow(CosNaming.NamingContext);
        

            
        #waveform_context = obj._narrow(CosNaming.NamingContext)
        if waveform_context is None:
            print "Could not narrow to: " + waveform_naming_context_text
            sys.exit(1)
     

        # Create a list of port handles to resources containing the timingStatus interface
        members = waveform_context.list(100)
        for m in members[0]:
            res_name = m.binding_name[0]
            res = waveform_context.resolve([res_name])
            res_handle = res._narrow(CF.Resource)
            if res_handle is None:
                continue
            
            PortReference = res_handle.getPort("send_timing_report")
            if PortReference is None:
                continue
            PortHandle = PortReference._narrow(CF.Port)
            if PortHandle != None:
                self.connected_ports.append(PortHandle)

    def __del__(self):
        for porthandle in self.connected_ports:
            porthandle.disconnectPort("thisismyconnectionid_timing")

        while(time.time() - last_time) < 1.0:
            time.sleep(.3)

