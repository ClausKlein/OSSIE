/****************************************************************************
 
Copyright 2008, Virginia Polytechnic Institute and State University
 
This file is part of the OSSIE Core Framework.
 
OSSIE Core Framework is free software; you can redistribute it and/or modify
it under the terms of the Lesser GNU General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.
 
OSSIE Core Framework is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Lesser GNU General Public License for more details.
 
You should have received a copy of the Lesser GNU General Public License
along with OSSIE Core Framework; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 
****************************************************************************/

#include <iostream>
#include <sstream>

#include "ossie/debug.h"
#include "ossie/ossieSupport.h"
#include "ossie/portability.h"
#include "ossie/ApplicationFactory_impl.h"

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

ApplicationFactory_impl::ApplicationFactory_impl (const char *_softProfile, CF::DomainManager::ApplicationSequence *_appseq)
{
    orb = new ossieSupport::ORB();
    
    // Get application factory data for private variables
    _softwareProfile = _softProfile;
    _sadParser = new SADParser (_softwareProfile.c_str());
    _name = _sadParser->getName();
    _identifier = _sadParser->getID();
   
    appseq = _appseq;
   
    // Get an object reference for the domain manager
    CORBA::Object_ptr obj = orb->get_object_from_name("DomainName1/DomainManager");
    dmnMgr = CF::DomainManager::_narrow (obj);
    
#ifdef HAVE_OMNIEVENTS
    
    ApplicationFactoryEventHandler *_evtHandler =
        new ApplicationFactoryEventHandler (this);
        
    dmnMgr->registerWithEventChannel (_evtHandler->_this (),
                                      CORBA::string_dup (_identifier),
                                      CORBA::string_dup ("ODM_Channel"));
#endif
}


ApplicationFactory_impl::~ApplicationFactory_impl ()
{
    delete orb;
}


/// \TODO Comment/Rewrite this function. It's painful.
CF::Application_ptr ApplicationFactory_impl::create (const char *name,
    const CF::Properties & initConfiguration,
    const CF::DeviceAssignmentSequence & deviceAssignments)
	throw (CORBA::SystemException, CF::ApplicationFactory::CreateApplicationError,
    CF::ApplicationFactory::CreateApplicationRequestError,
    CF::ApplicationFactory::InvalidInitConfiguration)
{

    DEBUG(1, AppFact, "entering appFactory->create")

    // Establish naming context for this waveform
	CORBA::Object_var obj_DN = orb->get_object_from_name("DomainName1");
	CosNaming::NamingContext_var DomainContext = CosNaming::NamingContext::_nil();
	DomainContext = CosNaming::NamingContext::_narrow(obj_DN);
	short WaveformCount = 0;
	string waveform_context_name("");
	CORBA::Object_var obj_WaveformContext;
	CosNaming::NamingContext_var WaveformContext = CosNaming::NamingContext::_nil();
	
	bool found_empty = false;
	
	do {
		WaveformCount++;
		waveform_context_name = "";
		waveform_context_name.append(name);
		waveform_context_name.append("_");
		ostringstream number_str;
		number_str << WaveformCount;
		waveform_context_name.append(number_str.str());
		string temp_waveform_context("DomainName1/");
		temp_waveform_context.append(waveform_context_name);
    		CosNaming::Name_var cosName = orb->string_to_CosName(temp_waveform_context.c_str());
		try {
			obj_WaveformContext = orb->inc->resolve(cosName);
		} catch (const CosNaming::NamingContext::NotFound &) {
			found_empty = true;
		}
	} while (!found_empty);
	
	CosNaming::Name WaveformContextName;
	WaveformContextName.length(1);
	WaveformContextName[0].id = CORBA::string_dup(waveform_context_name.c_str());
	DomainContext->bind_new_context(WaveformContextName);
	
	string base_naming_context("DomainName1/");
	base_naming_context.append(waveform_context_name);
    
	// The reason why it needs to be re-parsed is to populate the vector with the new waveform naming context
    if (requiredComponents.size()!=0) {
    	requiredComponents.clear();
	}
    
    getRequiredComponents(base_naming_context.c_str());
    
    // If there is a device assignment sequence, verify its validity;
    // otherwise generate deployment information automatically
    /// \TODO Write dynamic component deployment routine
    if (deviceAssignments.length() > 0) {
        verifyDeviceAssignments(deviceAssignments);
	} else {
		std::cerr << "No Device Assignment Sequence, write dynamic deployment code" << endl;
        throw CF::ApplicationFactory::CreateApplicationRequestError();
    }
    
    // Allocate space for device assignment
    /// \TODO (assume maximum length of 10 - will make dynamic in later version)
    CF::DeviceAssignmentSequence* _availableDevs =
        new CF::DeviceAssignmentSequence(deviceAssignments);
        
    PROC_ID_SEQ* _pidSeq = new PROC_ID_SEQ (30);
    
    _pidSeq->length (0);
    
    if (registeredDevices.size()==0) {
		// Populate registeredDevices vector
    	getRegisteredDevices();
	}
    
    DEBUG(2, AppFact, "requiredComponents size - " << requiredComponents.size())

    for (unsigned int rc_idx = 0; rc_idx < requiredComponents.size (); rc_idx++) {
        ossieSupport::ComponentInfo *component = requiredComponents[rc_idx];
        
        DEBUG(1, AppFact, "Component - " << component->getName() << "   Assigned device - " << component->getAssignedDeviceId())
        
        CF::ExecutableDevice_ptr device = find_device_from_id(component->getAssignedDeviceId());
        
        DEBUG(1, AppFact, "Host is " << device->label () << " Local file name is " << component->getLocalFileName())
        
        // Now we have a pointer to the required device
        // Get allocation properties
        device->allocateCapacity (component->getAllocationCapacities());
        
        // Get file name, load if it is not empty
        if (strlen (component->getLocalFileName()) >  0) {
            /// \TODO Validate that the intended device supports the LoadableDevice interface
     
            DEBUG(1, AppFact, "loading " << component->getLocalFileName())
            
			CF::FileSystem_ptr fs = CF::FileSystem::_narrow(dmnMgr->fileMgr());
            device->load (fs, component->getLocalFileName(), component->getCodeType());
            
            // Execute when necesary
            if (component->getCodeType() == CF::LoadableDevice::EXECUTABLE
                    || component->getCodeType() == CF::LoadableDevice::SHARED_LIBRARY
                    && strcmp (component->getEntryPoint(), "") != 0) {
                /// \TODO: Validate that the intended device supports the LoadableDevice interface
                
                DEBUG(1, AppFact, "executing-> " << component->getLocalFileName())

				CF::DataType dt;
				dt.id = component->getIdentifier();

				string initial_name("");
				
				if (!strncmp("DomainName1", component->getNamingServiceName(), 11)) {
					initial_name.append((component->getNamingServiceName()+12));
				} else {
					initial_name.append(component->getNamingServiceName());
				}
				
				dt.value <<= component->getNamingServiceName();
					
				component->addExecParameter(&dt);
				
				CORBA::Object_ptr NC_obj = orb->get_object_from_name(base_naming_context.c_str());

				CORBA::String_var ior = orb->orb->object_to_string(NC_obj);

				dt.id = "NAMING_CONTEXT_IOR";
				dt.value <<= ior;

				component->addExecParameter(&dt);

				dt.id = "NAME_BINDING";
				dt.value <<= component->getName();

				component->addExecParameter(&dt);
						
				CF::ExecutableDevice::ProcessID_Type tempPid = device->
						execute (component->getLocalFileName(),
								 component->getOptions(),
								 component->getExecParameters());

				if (tempPid < 0) {
					/// \TODO throw exception here
				} else {
					_pidSeq->length (_pidSeq->length() + 1);
					(* _pidSeq)[_pidSeq->length() - 1].processId = tempPid;
					(* _pidSeq)[_pidSeq->length() - 1].componentId =
						CORBA::string_dup(component->getIdentifier());
				}
				// NOTE: The PID returned by execute is not handled
				// An exception shall be thrown when PID = -1
            }
        }
    }
    
    /// \TODO Move this code into above loop

    CF::Resource_ptr _assemblyController = NULL;
    
    ELEM_SEQ* _namingCtxSeq = new ELEM_SEQ ();
    _namingCtxSeq->length (requiredComponents.size ());
    
    ELEM_SEQ* _implSeq = new ELEM_SEQ ();
    _implSeq->length (requiredComponents.size ());
    
	// Install the different components in the system
	for (unsigned int rc_idx = 0; rc_idx < requiredComponents.size (); rc_idx++) {
		ossieSupport::ComponentInfo *component = requiredComponents[rc_idx];
		
		DEBUG(1, AppFact, "installing-> " << component->getLocalFileName())

		// This makes sure that the resource factory is not handled like a resource
		if (!component->getIsResource ()) {
			continue;
		}
		
		(*_namingCtxSeq)[rc_idx].componentId =
			CORBA::string_dup (component->getIdentifier ());
			
		(*_implSeq)[rc_idx].componentId =
			CORBA::string_dup (component->getIdentifier ());
			
		// Assuming 1 instantiation for each componentplacement
		if (component->getNamingService ()) {
			// This is for the naming-service based configuration,
			// it assumes that the component already exists (like a device)
			const char* _lookupName = component->getNamingServiceName ();

			DEBUG(1, AppFact, "component NamingServiceName: " << component->getNamingServiceName())
								
			(*_namingCtxSeq)[rc_idx].elementId = CORBA::string_dup (_lookupName);
			
			CORBA::Object_ptr _obj = CORBA::Object::_nil ();
			DEBUG(1, AppFact, "Wait component to start")
			// Wait for component to start
			do {
				try {
					_obj = orb->get_object_from_name(_lookupName);
				} catch (CosNaming::NamingContext::NotFound) {
				};
				

				///\todo Check the name not found exceptions and make certain this is correct
				ossieSupport::nsleep(0,50 * 1000);
			} while (CORBA::is_nil (_obj));
			DEBUG(1, AppFact, "Check for initialized and configured ressource")
			// Check to see if the resource is the assembly controller
			// either way, the resource is initialized and configured
			CF::Resource_ptr _rsc = CF::Resource::_narrow (_obj);
			component->setResourcePtr(_rsc);

			if (component->getIsAssemblyController()) {
				_assemblyController = _rsc;
				_assemblyController->initialize ();
				_assemblyController->configure (initConfiguration);
				_assemblyController->configure (component->getConfigureProperties());
			} else {
				if (component->getIsResource () && component->getIsConfigurable ()) {
					_rsc->initialize ();
					_rsc->configure (component->getConfigureProperties());
				}
			}
		}
#if 0 ///\todo Add support for resource factories 
	else if ((*ComponentInstantiationVector)[0]->isResourceFactoryRef ()) {
			// resource-factory based component instantiation
			SADComponentInstantiation* _resourceFacInstantiation = NULL;
			
			int tmpCnt = 0;
			
			// figure out which resource factory is used
			while (_resourceFacInstantiation == NULL) {
				_resourceFacInstantiation =
					(*ComponentsVector)[tmpCnt]->
					getSADInstantiationById ((*ComponentInstantiationVector)
											 [0]->getResourceFactoryRefId ());
				tmpCnt++;
			}
			
			(*_namingCtxSeq)[i].elementId =
				CORBA::string_dup (_resourceFacInstantiation->
								   getFindByNamingServiceName ());
								   
			CORBAOBJ _obj =
				orb->get_object_from_name (_resourceFacInstantiation->
										   getFindByNamingServiceName ());
										   
			CF::ResourceFactory_ptr _resourceFactory =
				CF::ResourceFactory::_narrow (_obj);
				
			// configure factory
			/*std::vector < InstantiationProperty * >*_factoryInstantiationProps
				= (*ComponentInstantiationVector)[0]->getFactoryProperties ();
			 
			CF::Properties _factoryProperties (_factoryInstantiationProps->
				size ());
			 
			for (unsigned int j = 0; j < _factoryInstantiationProps->size ();
				j++)
			{
				_factoryProperties[j].id
					=
			CORBA::string_dup ((*_factoryInstantiationProps)[j]->
			getID ());
			_factoryProperties[j].
			value <<= CORBA::
			string_dup ((*_factoryInstantiationProps)[j]->getValue ());
			}*/
			
			// unused PJB                   char *value = LoadInfoVector[vector_access]->name;
			
			// instantiate resource
			// (mechanism for this is left up to the factory's implementation)
			
			CF::Resource_ptr _resourceCreated =
				_resourceFactory->
				createResource (LoadInfoVector[vector_access]->name,
								LoadInfoVector[vector_access]->factoryParameters);
								
			if (CORBA::is_nil (_resourceCreated))
				throw CF::ApplicationFactory::CreateApplicationError ();
				
			// check to see if the resource is the assembly controller
			//      either way, the resource is initialized and configured
			if (strcmp (_assemblyControllerProfile->getID (),
						(*ComponentInstantiationVector)[0]->getID ()) == 0) {
				_assemblyController = _resourceCreated;
				_assemblyController->initialize ();
				_assemblyController->configure (initConfiguration);
				_assemblyController->
				configure (LoadInfoVector[vector_access]->configureProperties);
			} else {
				_resourceCreated->initialize ();
				_resourceCreated->
				configure (LoadInfoVector[vector_access]->configureProperties);
			}
			vector_access++;
		} else {
			const char* _id, *_usagename;
			
			_id = LoadInfoVector[i]->implId;
			
			_usagename = LoadInfoVector[i]->name;
			
			char* _lookup = new char[strlen (_usagename) + strlen (_id) + 1];
			
			strcpy (_lookup, _usagename);
			strcat (_lookup, "_");
			strcat (_lookup, _id);
			
			(*_namingCtxSeq)[i].elementId = CORBA::string_dup (_lookup);
			
			CORBA::Object_ptr _obj = orb->get_object_from_name(_lookup);
			
			if (_assemblyControllerProfile == (*ComponentInstantiationVector)[0]) {
				_assemblyController = CF::Resource::_narrow (_obj);
				_assemblyController->initialize ();
				_assemblyController->configure (initConfiguration);
				_assemblyController->configure (LoadInfoVector[i]->
												configureProperties);
			} else {
				CF::Resource_ptr _rsc = CF::Resource::_narrow (_obj);
				_rsc->initialize ();
				_rsc->configure (LoadInfoVector[i]->configureProperties);
			}
			
			delete _lookup;
			_lookup = NULL;
		}
#endif // End resource factory support
	}                                         // end for()
    
    std::vector < Connection * >*_connection = _sadParser->getConnections ();
    if (connectionData.size()!=0) {
    	connectionData.clear();
	}
    
    // Create all resource connections
    for (int c_idx = _connection->size () - 1; c_idx >= 0; c_idx--) {
		Connection *connection = (*_connection)[c_idx];

		DEBUG(3, AppFact, "Processing connection " << connection->getID())

		// Process provides port
        CORBA::Object_var provides_port_ref;

		ProvidesPort* _providesPortParser = connection->getProvidesPort ();
		FindBy * _findProvidesPortBy;
        CORBA::Object_var _providesObj;

        if (connection->isProvidesPort ()) {
		    DEBUG(3, AppFact, "Provides Port is provides port") 
            _providesPortParser = connection->getProvidesPort ();

			if (_providesPortParser->isFindBy()) {
				DEBUG(3, AppFact, "Provides port is find by component name")
				FindBy* _findProvidesPortBy = _providesPortParser->getFindBy ();

				if (_findProvidesPortBy->isFindByNamingService ()) {
					string findbyname(base_naming_context);
					findbyname.append("/");

					// This initial string compare is here for legacy reasons
					if (!strncmp("DomainName1", _findProvidesPortBy->getFindByNamingServiceName (), 11)) {
						findbyname.append((_findProvidesPortBy->getFindByNamingServiceName ()+12));
					} else {
						findbyname.append(_findProvidesPortBy->getFindByNamingServiceName ());
					}
					try{
					  _providesObj = orb->get_object_from_name(findbyname.c_str());
					}
					catch (CosNaming::NamingContext::NotFound) {
					  string my_component_name = findbyname;
					  size_t location_first_slash = my_component_name.find('/', 0);
					  size_t location_second_slash = my_component_name.find('/', location_first_slash+1);
					  findbyname = "DomainName1/";
					  findbyname.append(my_component_name, location_second_slash+1, \
							    my_component_name.length()-location_second_slash-1);
					  DEBUG(4, AppFact, "The findname that I'm using is: " << findbyname);
					  _providesObj = orb->get_object_from_name (findbyname.c_str());
					};

				}
			} else if (_providesPortParser->isComponentInstantiationRef()) {
				DEBUG(3, AppFact, "Provides port is find by componentinstantiationref")

				for (unsigned int i=0; i < requiredComponents.size(); i++) {
					ossieSupport::ComponentInfo *component = requiredComponents[i];
					DEBUG(3, AppFact, "Looking for provides port component ID " << component->getIdentifier() \
							<< " ID from SAD " << _providesPortParser->getComponentInstantiationRefID())

					if (strcmp(component->getIdentifier(), _providesPortParser->getComponentInstantiationRefID()) == 0) {
						_providesObj = component->getResourcePtr();
						break;
					}

					if (i == (requiredComponents.size() - 1)) {
						std::cerr << "Provides port component not found" << std::endl;
						///\todo throw exception
					}
				}
			}
		} else if (connection->isFindBy ()) {
			DEBUG(3, AppFact, "Provides Port is FindBy port name") \
				_findProvidesPortBy = connection->getFindBy ();

			if (_findProvidesPortBy->isFindByNamingService ()) {
				string findbyname(base_naming_context);
				findbyname.append("/");

				// This initial string compare is here for legacy reasons
				if (!strncmp("DomainName1", _findProvidesPortBy->getFindByNamingServiceName (), 11)) {
					findbyname.append((_findProvidesPortBy->getFindByNamingServiceName ()+12));
				} else {
					findbyname.append(_findProvidesPortBy->getFindByNamingServiceName ());
				}

		    	// The name is not found because it is hardware
				DEBUG(4, AppFact, "The findname that I'm using is: " << findbyname)
				try {
					provides_port_ref = orb->get_object_from_name (findbyname.c_str());
				} catch (CosNaming::NamingContext::NotFound) {
					string my_component_name = findbyname;
					size_t location_first_slash = my_component_name.find('/', 0);
					size_t location_second_slash = my_component_name.find('/', location_first_slash+1);
					findbyname = "DomainName1/";
					findbyname.append(my_component_name, location_second_slash+1, \
							my_component_name.length()-location_second_slash-1);
					DEBUG(4, AppFact, "The findname that I'm using is: " << findbyname)
					provides_port_ref = orb->get_object_from_name (findbyname.c_str());
				};
			} else {
				std::cerr << "Cannot find naming service name for FindBy provides port" << std::endl;
				/// \todo throw an exception?
			}
		} else {
			std::cerr << "Cannot find port information for provides port" << std::endl;
			/// \todo throw an exception?
        }
 
		// Find object ref for uses port
		// Process uses port
		UsesPort* _usesPortParser = connection->getUsesPort ();
		DEBUG(3, AppFact, "Uses port Identifier - " << _usesPortParser->getID())
		CORBA::Object_var _usesObj;

		if (_usesPortParser->isFindBy()) {
			FindBy* _findUsesPortBy = _usesPortParser->getFindBy ();

			if (_findUsesPortBy->isFindByNamingService ()) {
				string findbyname(base_naming_context);
				findbyname.append("/");

				// This initial string compare is here for legacy reasons
				if (!strncmp("DomainName1", _findUsesPortBy->getFindByNamingServiceName (), 11)) {
					findbyname.append((_findUsesPortBy->getFindByNamingServiceName ()+12));
				} else {
					findbyname.append(_findUsesPortBy->getFindByNamingServiceName ());
				}
				try {
					_usesObj = orb->get_object_from_name (findbyname.c_str());
				} catch (CosNaming::NamingContext::NotFound) {
					string my_component_name = findbyname;
					size_t location_first_slash = my_component_name.find('/', 0);
					size_t location_second_slash = my_component_name.find('/', location_first_slash+1);
					findbyname = "DomainName1/";
					findbyname.append(my_component_name, location_second_slash+1, \
							my_component_name.length()-location_second_slash-1);
					DEBUG(4, AppFact, "The findname that I'm using is: " << findbyname)
					_usesObj = orb->get_object_from_name (findbyname.c_str());
				};
			}
		} else if (_usesPortParser->isComponentInstantiationRef()) {
			for (unsigned int i=0; i < requiredComponents.size(); i++) {
				ossieSupport::ComponentInfo *component = requiredComponents[i];
				if (strcmp(component->getIdentifier(), _usesPortParser->getComponentInstantiationRefID()) == 0) {
					_usesObj = component->getResourcePtr();
					break;
				}
				if (i == requiredComponents.size()) {
					std::cerr << "Uses port component not found" << std::endl;
					///\todo throw exception
				}
			}
		} else {
			std::cerr << "Did not find method to get uses port" << std::endl;
			///\todo throw exception
		}
			
		/**************************************/
		/*                                    */
		/* Connection Establishment Rewritten */
		/*                                    */
		/**************************************/
		
		// CORBA object reference
		CORBA::Object_var uses_port_ref;
		
		// Output Uses Port Name
		const char* portName = _usesPortParser->getID();
		DEBUG(3, AppFact, "Getting Uses Port " << portName)
		
		// Get Uses Port
		CF::Resource_var _usesComp = CF::Resource::_narrow(_usesObj);
		uses_port_ref = _usesComp->getPort (_usesPortParser->getID());

		DEBUG(3, AppFact, "back from getport")
		CF::Port_ptr usesPort = CF::Port::_narrow (uses_port_ref);
		DEBUG(3, AppFact, "result from getport narrowed")

		if (CORBA::is_nil (usesPort)) {
			std::cerr << "getPort returned nil reference" << std::endl;
			throw CF::ApplicationFactory::CreateApplicationError();
		}

		// Output Provides Port Name
		DEBUG(3, AppFact, "Done with uses port")
		DEBUG(3, AppFact, "Getting Provides Port ")
			
		// Get Provides Port
		// Note: returned object reference is NOT narrowed to a CF::Port
		if (!connection->isFindBy ()){
			CF::Resource_ptr _providesResource;
			DEBUG(3, AppFact, "Narrowing provides resource")
			_providesResource = CF::Resource::_narrow (_providesObj);
			DEBUG(3, AppFact, "Getting provides port with id - " << _providesPortParser->getID())
			provides_port_ref = _providesResource->getPort (_providesPortParser->getID());
		}

		if (CORBA::is_nil (provides_port_ref)) {
		std::cerr << "getPort returned nil or non-port reference" << std::endl;
			throw CF::ApplicationFactory::CreateApplicationError();
		}
		
		// Output ConnectionID
		DEBUG(3, AppFact, "Creating Connection " << connection->getID());
		
		// Create connection
		usesPort->connectPort (provides_port_ref, connection->getID());
			
		connectionData.push_back(new ossieSupport::ConnectionInfo(usesPort, connection->getID()));
    }

    // Check to make sure _assemblyController was initialized
    if (_assemblyController == NULL) {
        std::cerr << "ERROR: ApplicationFactory_impl::create()" << std::endl \
                  << "  => assembly controller was never initialized" << std::endl;

        // Throw exception
        CF::ApplicationFactory::CreateApplicationError create_app_error;
        create_app_error.msg = "assembly controller was never initialized";
        create_app_error.errorNumber = CF::CFNOTSET;
        throw create_app_error;
    }
    
    // We are assuming that all components and their resources are collocated.
    // This means that we assume the SAD <partitioning> element contains the
    // <hostcollocation> element.
    Application_impl* _application = new Application_impl (_identifier.c_str(), name, _softwareProfile.c_str(), \
			_availableDevs, _implSeq, _namingCtxSeq, _pidSeq, connectionData, \
			CF::Resource::_duplicate (_assemblyController), appseq);
												 
                                     
    /// \todo Pass object ref for application when application servant/ref stuff sorted out
    ossieSupport::sendObjAdded_event(_identifier.c_str(), _application->identifier(), _application->name(), \
			(CORBA::Object_var) NULL, StandardEvent::APPLICATION);

    // Add a reference to the new application to the ApplicationSequence in DomainManager
    int old_length = appseq->length();
    appseq->length(old_length+1);
    (*appseq)[old_length] = CF::Application::_duplicate (_application->_this ());

    return CF::Application::_duplicate (_application->_this ());
}
; /* END ApplicationFactory_impl::create() */


// Verify each component from the SAD exits in the device assignment sequence
void ApplicationFactory_impl::verifyDeviceAssignments (const CF::DeviceAssignmentSequence& _deviceAssignments)
{
    CF::DeviceAssignmentSequence badAssignments;
    badAssignments.length(requiredComponents.size());
    
    unsigned int notFound = 0;
    
    for (unsigned int i = 0; i < requiredComponents.size (); i++) {
        bool found = false;

        for (unsigned int j = 0; j < _deviceAssignments.length (); j++) {
            DEBUG(4, AppFact, "ComponentID - " << _deviceAssignments[j].componentId << "   Component - " \
					<< requiredComponents[i]->getIdentifier())

            if (strcmp (_deviceAssignments[j].componentId, requiredComponents[i]->getIdentifier()) == 0) {
                found = true;
                requiredComponents[i]->setAssignedDeviceId(_deviceAssignments[j].assignedDeviceId);
            }
        }

        if (!found) {
            badAssignments[notFound++].componentId = CORBA::string_dup(requiredComponents[i]->getName());
        }
    }
    
    if (notFound > 0) {
		std::cerr << "Device Assignment Sequence does not validate against the .sad file" << std::endl;
		throw CF::ApplicationFactory::CreateApplicationRequestError(badAssignments);
    }
}

void ApplicationFactory_impl::getRequiredComponents(const char * incomingNamingContext)
{

    std::vector <SADComponentPlacement*> *componentsFromSAD = _sadParser->getComponents();

    const char *assemblyControllerRefId = _sadParser->getAssemblyControllerRefId();

    for (unsigned int i = 0; i < componentsFromSAD->size(); i++) {
		SADComponentPlacement *component = (*componentsFromSAD)[i];
        ossieSupport::ComponentInfo *newComponent = new ossieSupport::ComponentInfo();

        // Extract required data from SPD file
        SPDParser spd(component->getSPDFile());
        SCDParser scd(spd.getSCDFile());

        newComponent->setName(spd.getSoftPkgName());
		newComponent->setIsResource(scd.isResource());
		newComponent->setIsConfigurable(scd.isConfigurable());

        // Extract implementation data from SPD file
        vector <SPDImplementation *> *spd_i = spd.getImplementations();
        
        // Assume only one implementation, use first available result [0]
        newComponent->setImplId((*spd_i)[0]->getID());
        newComponent->setCodeType((*spd_i)[0]->getCodeType());
		newComponent->setLocalFileName((*spd_i)[0]->getCodeFile());
        newComponent->setEntryPoint((*spd_i)[0]->getEntryPoint());
        
        // Extract Properties
        PRFParser prf(spd.getPRFFile());
        std::vector <PRFProperty *> *prop = prf.getFactoryParamProperties();

        for (unsigned int i=0; i < prop->size(); i++) {
            newComponent->addFactoryParameter((*prop)[i]->getDataType());
        }
        
        prop = prf.getExecParamProperties();

        for (unsigned int i=0; i < prop->size(); i++) {
            newComponent->addExecParameter((*prop)[i]->getDataType());
	    
        }
        
        prop = prf.getMatchingProperties();

        for (unsigned int i=0; i < prop->size(); i++) {
            newComponent->addAllocationCapacity((*prop)[i]->getDataType());
        }
        
        prop = prf.getConfigureProperties();

        for (unsigned int i=0; i < prop->size(); i++) {
            newComponent->addConfigureProperty((*prop)[i]->getDataType());
        }
        

		// Extract Instantiation data from SAD
		// This is wrong, there can be more than one instantiation per placement
		// Basic fix, iterate over instantiations
		///\todo Fix for multiple instantiations per component
		vector <SADComponentInstantiation *> *instantiations = component->getSADInstantiations();
		
		SADComponentInstantiation *instance = (*instantiations)[0];

		newComponent->setIdentifier(instance->getID());

		if (strcmp(newComponent->getIdentifier(), assemblyControllerRefId) == 0) {
			newComponent->setIsAssemblyController(true);
		}

		newComponent->setNamingService(instance->isNamingService());

		if (newComponent->getNamingService()) {
			string initial_name(incomingNamingContext);
			initial_name.append("/");
			// this initial string compare is here for legacy reasons
			if (!strncmp("DomainName1", instance->getFindByNamingServiceName(), 11)) {
				initial_name.append((instance->getFindByNamingServiceName()+12));
			} else {
				initial_name.append(instance->getFindByNamingServiceName());
			}
			DEBUG(1, AppFact, "set NamingServiceName:" << initial_name)
			//newComponent->setNamingServiceName(instance->getFindByNamingServiceName());
			newComponent->setNamingServiceName(initial_name.c_str());
		}

		newComponent->setUsageName(instance->getUsageName());
		std::vector <InstantiationProperty *> *ins_prop = instance->getProperties();

		for (unsigned int i = 0; i < ins_prop->size(); ++i) {
			DEBUG(3, AppFact, "Instantiation property id = " << (*ins_prop)[i]->getID())
			vector <string> ins_values = (*ins_prop)[i]->getValues();
			newComponent->overrideProperty((*ins_prop)[i]->getID(), (*ins_prop)[i]->getValues());
		}

		requiredComponents.push_back(newComponent);
	}
}


void ApplicationFactory_impl::getRegisteredDevices ()
{

    CF::DomainManager::DeviceManagerSequence* devMgrs;
    devMgrs = dmnMgr->deviceManagers ();
    
    for (unsigned int i=0; i<devMgrs->length(); i++) {
        CF::DeviceSequence* devices = (*devMgrs)[i]->registeredDevices();

        for (unsigned int j=0; j<devices->length(); j++) {
            registeredDevices.push_back((*devices)[j]);
        }
    }
}


CF::ExecutableDevice_ptr ApplicationFactory_impl::find_device_from_id(const char *device_id)
{
    for (unsigned int i=0; i<registeredDevices.size(); i++) {
        if (strcmp(registeredDevices[i]->identifier(), device_id) == 0) {
            return CF::ExecutableDevice::_narrow(registeredDevices[i]);
        }
    }

    std::cerr << "Device not found, this should never happen" << std::endl;

    return 0;
}

#ifdef HAVE_OMNIEVENTS
ApplicationFactoryEventHandler::ApplicationFactoryEventHandler (ApplicationFactory_impl * _appFac)
{
    appFactory = _appFac;
}


voidApplicationFactoryEventHandler::push (const CORBA::Any & _any)
	throw (CORBA::SystemException, CosEventComm::Disconnected)
{}


void ApplicationFactoryEventHandler::disconnect_push_consumer ()
	throw (CORBA::SystemException)
{}
#endif

