#! /usr/bin/env python

'''
/****************************************************************************

Copyright 2007 Virginia Polytechnic Institute and State University

This file is part of the OSSIE pass_data.

OSSIE pass_data is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

OSSIE pass_data is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OSSIE pass_data; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/

'''

from omniORB import CORBA
from omniORB import URI
import CosNaming

try:     # mac framework
    import standardInterfaces__POA
    import customInterfaces__POA
    import CF, CF__POA
except ImportError:  # 0.6.2
    import ossie.standardinterfaces.standardInterfaces__POA as standardInterfaces__POA
    import ossie.custominterfaces.customInterfaces__POA as customInterfaces__POA
    import ossie.cf.CF as CF
    import ossie.cf.CF__POA as CF__POA

import sys
import threading
import time

#-------------------------------------------------------------
# pass_data_i class definition (main component class)
#-------------------------------------------------------------
class pass_data_i(CF__POA.Resource):
    def __init__(self, uuid, label, poa):
        CF._objref_Resource.__init__(self._this())

        print "pass_data_i __init__: " + label
        self.naming_service_name = label
        self.poa = poa

        self.inPort0_servant = dataIn_complexShort_i(self, "cshort_in")
        self.inPort0_var = self.inPort0_servant._this()

        self.outPort0_servant = dataOut_complexShort_i(self, "cshort_out")
        self.outPort0_var = self.outPort0_servant._this()
        self.outPort0_active = False

        self.timingPort_servant = dataOut_timingStatus_i(self, 
                                                         "send_timing_report")
        self.timingPort_var = self.timingPort_servant._this()
        self.timingPort_active = False
 
        self.configure_called = False

        self.propertySet = []
        self.work_mod = None
        
    def start(self):
        print "pass_data start called"
        
    def stop(self):
        print "pass_data stop called"
        
    def getPort(self, id):
        if str(id) == "cshort_in":
            return self.inPort0_var
        elif str(id) == "cshort_out":
            return self.outPort0_var
        elif str(id) == "send_timing_report":
            return self.timingPort_var

        return None  #port not found in available ports list
        
    def initialize(self):
        print "pass_data initialize called"
    
    def configure(self, props):
        print "pass_data configure called"
        buffer_size = 0
 
        if self.configure_called == False:        
            self.work_mod = WorkClass(self, buffer_size)
            self.configure_called = True

    def query(self, props):
        return self.propertySet
    
    def releaseObject(self):
        # release the main work module
        self.work_mod.Release()
        
        # release the main process threads for the ports
        self.outPort0_servant.releasePort()
                
        # deactivate the ports
        iid0 = self.poa.reference_to_id(self.inPort0_var)
        oid0 = self.poa.reference_to_id(self.outPort0_var)
        oid1 = self.poa.reference_to_id(self.timingPort_var)

        self.poa.deactivate_object(iid0)
        self.poa.deactivate_object(oid0)
        self.poa.deactivate_object(oid1)

#------------------------------------------------------------------
# dataIn_complexShort_i class definition
#------------------------------------------------------------------
class dataIn_complexShort_i(standardInterfaces__POA.complexShort):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def pushPacket(self, I, Q):
        self.parent.work_mod.AddData(I, Q)
        if (self.parent.timingPort_active):
            self.parent.timingPort_servant.send_timing_message(
                    self.parent.naming_service_name, self.name, 
                    "pushPacket", "end", len(I))

#------------------------------------------------------------------
# dataOut_complexShort_i class definition
#------------------------------------------------------------------
class dataOut_complexShort_i(CF__POA.Port):
    def __init__(self, parent, name):
        self.parent = parent
        self.outPorts = {}
        self.name = name
        
        self.data_buffer = []
        self.data_event = threading.Event()
        self.data_buffer_lock = threading.Lock()
        
        self.is_running = True
        self.process_thread = threading.Thread(target = self.Process)
        self.process_thread.start()

    def connectPort(self, connection, connectionId):
        port = connection._narrow(standardInterfaces__POA.complexShort)
        self.outPorts[str(connectionId)] = port
        self.parent.outPort0_active = True

    def disconnectPort(self, connectionId):
        self.outPorts.pop(str(connectionId))
        if len(self.outPorts)==0:
            self.parent.outPort0_active = False

    def releasePort(self):
        # shut down the Process thread
        self.is_running = False
        self.data_event.set()

    def send_data(self, I, Q):
        self.data_buffer_lock.acquire()
        self.data_buffer.insert(0, (I,Q))
        self.data_buffer_lock.release()
        self.data_event.set()

    def Process(self):
        while self.is_running:
            self.data_event.wait()
            while len(self.data_buffer) > 0:
                self.data_buffer_lock.acquire()
                new_data = self.data_buffer.pop()
                self.data_buffer_lock.release()
                for port in self.outPorts.values():
                    port.pushPacket(new_data[0], new_data[1])
                self.data_event.clear()


#------------------------------------------------------------------
# dataOut_timingStatus_i class definition
#------------------------------------------------------------------
class dataOut_timingStatus_i(CF__POA.Port):
    def __init__(self, parent, name):
        self.parent = parent
        self.outPorts = {}
        self.name = name

        self.message_buffer = []
        self.timing_event = threading.Event()
        self.message_buffer_lock = threading.Lock()

        self.is_running = True
        self.process_thread = threading.Thread(target = self.Process)
        self.process_thread.start()

    def connectPort(self, connection, connectionId):
        # debug statement
        print "\nConnect called on timing port"
        port = connection._narrow(customInterfaces__POA.timingStatus)
        self.outPorts[str(connectionId)] = port
        self.parent.timingPort_active = True
	
    def disconnectPort(self, connectionId):
        self.outPorts.pop(str(connectionId))
        if len(self.outPorts) == 0:
            self.parent.timingPort_active = False
	
    def releasePort(self):
        # shut down the Process thread
        self.is_running = False
        self.timing_event.set()
	
    def send_timing_message(self, component_name, port_name, 
                            function_name, description, number_samples):
        tv = time.time()
        tv_sec = int(tv)
        tv_usec = int((tv-tv_sec)*1000000)
	
        tmpmsg = (str(component_name), str(port_name), 
                  str(function_name), str(description), 
                  tv_sec, tv_usec, number_samples)

        self.message_buffer_lock.acquire()
        self.message_buffer.insert(0, tmpmsg)
        self.message_buffer_lock.release()

        self.timing_event.set()

    def Process(self):
        while self.is_running:
            self.timing_event.wait()
            while len(self.message_buffer) > 0:
                self.message_buffer_lock.acquire()
                newmsg = self.message_buffer.pop()
                self.message_buffer_lock.release()
				
                for port in self.outPorts.values():
                    port.send_timing_event(newmsg[0], newmsg[1], 
                                           newmsg[2], newmsg[3], 
                                           newmsg[4], newmsg[5], 
                                           newmsg[6])

            else:
                self.timing_event.clear()

                
#-------------------------------------------------------------------
# ORB_Init class definition
#-------------------------------------------------------------------
class ORB_Init:
    """Takes care of initializing the ORB and bind the object"""
    
    def __init__(self, uuid, label):
        # initialize the orb
        self.orb = CORBA.ORB_init()
        
        # get the POA
        obj_poa = self.orb.resolve_initial_references("RootPOA")
        poaManager = obj_poa._get_the_POAManager()
        poaManager.activate()
        
        ns_obj = self.orb.resolve_initial_references("NameService")
        rootContext = ns_obj._narrow(CosNaming.NamingContext)
        
        # create the main component object
        self.pass_data_Obj = pass_data_i(uuid, label, obj_poa)
        pass_data_var = self.pass_data_Obj._this()
       
        name = URI.stringToName(label)
        rootContext.rebind(name, pass_data_var)
        
        self.orb.run()


class WorkClass:
    """This class provides a place for the main processing of the 
    component to reside."""

    def __init__(self, pass_data_ref, buffer_size):
        self.pass_data_ref = pass_data_ref
	
        self.data_queue = []
        self.data_queue_lock = threading.Lock()
        self.data_signal = threading.Event()

        self.is_running = True

        self.process_thread = threading.Thread(target=self.Process)
        self.process_thread.start()
	
    def __del__(self):
        # Destructor
        pass
	
    def AddData(self, I, Q):
        self.data_queue_lock.acquire()
        self.data_queue.insert(0, (I,Q))
        self.data_queue_lock.release()
        self.data_signal.set()  # indicate that there is data ready to be
                                # processed in self.Process
    	
    def Release(self):
        self.is_running = False
        self.data_signal.set()
		
    def Process(self):
        while self.is_running:
            # wait for the data_signal to be set in AddData
            self.data_signal.wait()               
            while len(self.data_queue) > 0:
                self.data_queue_lock.acquire()
                new_data = self.data_queue.pop()
                self.data_queue_lock.release()

                # Output the new data
                if self.pass_data_ref.outPort0_active:
                    self.pass_data_ref.outPort0_servant.send_data(new_data[0],
                                                                  new_data[1])

                self.data_signal.clear()  # if this is not cleared, I will 
                                          # always pass the 
                                          # self.data_signal.wait(statement), 
                                          # which causes me to pool in the 
                                          # following while statement until 
                                          # my packet has a length greater 
                                          # than 0.
				
        
#-------------------------------------------------------------------
# Code run when this file is executed
#-------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print sys.argv[0] + " <id> <usage name> "
    
    # r2983 framework:
    uuid = str(sys.argv[1])
    label = str(sys.argv[2])

    # /sdr/dom framework:
    # uuid = str(sys.argv[6])
    # label = str(sys.argv[4])

    print "Identifier - " + uuid + "  Label - " + label
    
    orb = ORB_Init(uuid, label)
    

