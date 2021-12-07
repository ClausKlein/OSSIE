from omniORB import CORBA
from omniORB import URI
import CosNaming
from ossie.standardinterfaces import standardInterfaces__POA
from ossie.custominterfaces import customInterfaces__POA
from ossie.cf import CF, CF__POA
import sys

import WorkModule  # module found in the component directory.
                   # this module is where the main processing
                   # thread resides.  
import threading
import time        # primarily availble for time.sleep() statements

#-------------------------------------------------------------
# __CLASS_NAME___i class definition (main component class)
#-------------------------------------------------------------
class __CLASS_NAME___i(CF__POA.Resource):
    def __init__(self, uuid, label, poa):
        CF._objref_Resource.__init__(self._this())
        print "__CLASS_NAME___i __init__: " + label
        self.naming_service_name = label
        self.poa = poa

        __PORT_DECL__
        
        self.WorkModule_created = False

        self.propertySet = []
        self.work_mod = None
        
    def start(self):
        print "__CLASS_NAME__ start called"
        
    def stop(self):
        print "__CLASS_NAME__ stop called"
        
    def getPort(self, id):
        __GET_PORT__
        
        return None  #port not found in available ports list
        
    def initialize(self):
        print "__CLASS_NAME__ initialize called"
    
    def configure(self, props):
        ''' The configure method is called twice by the framework:
        once to read the default properties in the component.prf
        file, and once to read the component instance properties
        storred in the waveform.sad file.  This method should be
        called before the start method.  This method is where
        the properties are read in by the component.  
        ''' 

        print "__CLASS_NAME__ configure called"
        buffer_size = 0
        
        __READ_PROPS__
    
        # make sure that only one WorkModule thread is started, 
        # even if configure method is called more than once    
        if not self.WorkModule_created:
            self.work_mod = WorkModule.WorkClass(self, buffer_size)
            self.WorkModule_created = True    

    def query(self, props):
        return self.propertySet
    
    def releaseObject(self):
        # release the main work module
        self.work_mod.Release()
        
        # release the main process threads for the ports
        __REL_MAIN_PROCESS_THREADS__
                
        # deactivate the ports
        __DEACTIVATE_PORTS__


__DATA_IN_CLASS_DEFS__        

__DATA_OUT_CLASS_DEFS__

__TIMING_MESSAGE_DEF__

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
        self.__CLASS_NAME___Obj = __CLASS_NAME___i(uuid, label, obj_poa)
        __CLASS_NAME___var = self.__CLASS_NAME___Obj._this()
        
        name = URI.stringToName(label)
        rootContext.rebind(name, __CLASS_NAME___var)
        
        self.orb.run()
        
#-------------------------------------------------------------------
# Code run when this file is executed
#-------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print sys.argv[0] + " <id> <usage name> "
    
    uuid = str(sys.argv[1])
    label = str(sys.argv[2])
    
    print "Identifier - " + uuid + "  Label - " + label
    
    orb = ORB_Init(uuid, label)
    

