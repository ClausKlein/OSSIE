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

Nov/10/03	C. Neely	Created
C. Aguayo

****************************************************************************/
#include <iostream>

#include <string.h>
#ifdef HAVE_UNISTD_H
#include <unistd.h>
#else  /// \todo change else to ifdef windows var
#include <process.h>
#endif
#ifdef HAVE_STDLIB_H
#include <stdlib.h>
#endif
#include <errno.h>
#include <stdio.h>

#include "ossie/debug.h"
#include "ossie/ossieSupport.h"
#include "ossie/DeviceManager_impl.h"
#include "ossie/portability.h"

DeviceManager_impl::~DeviceManager_impl ()
{
}


DeviceManager_impl::DeviceManager_impl(const char *DCDInput)

{

  _deviceConfigurationProfile = DCDInput;
}

//Parsing constructor
void DeviceManager_impl::post_constructor (CF::DeviceManager_var my_object_var) throw (CORBA::SystemException)

{
    orb_obj = new ossieSupport::ORB();

    myObj = my_object_var;

    _registeredDevices.length(0);
    _registeredServices.length(0);

    fs_servant = new FileSystem_impl();
    _fileSys = fs_servant->_this();


    if (_fileSys->exists (_deviceConfigurationProfile.c_str()))
    {


//Get Device Manager attributes (deviceConfigurationProfile, identifier and label)
//from DCD file

        DCDParser _DCDParser (_deviceConfigurationProfile.c_str());

        _identifier = _DCDParser.getID();
        _label = _DCDParser.getName();

//get DomainManager reference

        getDomainManagerReference ((char *)_DCDParser.getDomainManagerName ());

//Register DeviceManager with DomainManager
        _dmnMgr->registerDeviceManager (my_object_var);

        _adminState = DEVMGR_REGISTERED;

//parse filesystem names

//Parse local componenents from DCD files
        std::vector <componentPlacement> componentPlacements = _DCDParser.getComponentPlacements ();

        for (unsigned int i = 0; i < componentPlacements.size(); i++)
        {
//get spd reference
//parse spd file
	    SPDParser _SPDParser (_DCDParser.getFileNameFromRefId(componentPlacements[i].refId()));

//get code file name from implementation
            std::vector < SPDImplementation * >*_implementations =
                _SPDParser.getImplementations ();

///----------Assuming only one implementation
//spawn device
#ifdef HAVE_WORKING_FORK
            int myPid2;

            DEBUG(2, DevMgr, "Launching Device file " << (*_implementations)[0]->getCodeFile () << " Usage name " << componentPlacements[i].usageName())

            if ((myPid2 = fork()) < 0)
		std::cout << "Fork Error" << std::endl;

            if (myPid2 == 0)
            {
		// in child
		if (getenv("VALGRIND")) {
		    string logFile = "--log-file=";
		    logFile += (*_implementations)[0]->getCodeFile ();
		    char *val = "/usr/local/bin/valgrind";
		    execl(val, val, logFile.c_str(), (*_implementations)[0]->getCodeFile (), componentPlacements[i].id(), componentPlacements[i].usageName() , _DCDParser.getFileNameFromRefId(componentPlacements[i].refId()), NULL);
		} else {
		    execl((*_implementations)[0]->getCodeFile (), (*_implementations)[0]->getCodeFile (),componentPlacements[i].id(), componentPlacements[i].usageName() , _DCDParser.getFileNameFromRefId(componentPlacements[i].refId()), NULL);

		}
		std::cout << "Device did not execute : " << strerror(errno) << std::endl;
                exit (-1);
            }
#endif

            CORBA::Object_var _obj = CORBA::Object::_nil();
            char nameStr[255];
            sprintf( nameStr, "DomainName1/%s", componentPlacements[i].usageName() );
	    DEBUG(3, DevMgr, "searching for "<< nameStr)
            do
            {
/// \todo sleep prevents system from beating Name Service to death, Fix better
		ossieSupport::nsleep(0, 50*1000);
		try {
		    _obj = orb_obj->get_object_from_name(nameStr);
		} catch (CosNaming::NamingContext::NotFound) {};
            }
            while (CORBA::is_nil (_obj));
	    DEBUG(3, DevMgr, "found "<< nameStr)

            CF::Device_var tempDevice = CF::Device::_narrow (_obj);
            tempDevice->initialize ();

//Get properties from SCD
            PRFParser _PRFparser (_SPDParser.getPRFFile ());
            std::vector <PRFProperty *> *prfSimpleProp = _PRFparser.getConfigureProperties ();
            CF::Properties configCapacities;
            configCapacities.length (prfSimpleProp->size ());
            for (unsigned int i = 0; i < prfSimpleProp->size (); i++)
            {
                configCapacities[i] = *((*prfSimpleProp)[i]->getDataType ());
            }

//configure properties
	    DEBUG(3, DevMgr, "Configuring capacities")
            tempDevice->configure (configCapacities);
	    DEBUG(3, DevMgr, "Registering device")
            registerDevice (CF::Device::_duplicate(tempDevice));
 	    DEBUG(3, DevMgr, "Device Registered")

        }

//So far, it is assumed that all components are local
/*//Obtain DEPLY-ON components
   std::vector<DCDComponentPlacement> DeployOnComponentsVector = _DCDParser.getDeployOnComponents();

   std::vector<char*> DPDList;

   //Get DPD file names from DeployOnComponentsVector
   for(int i = 0; i < DeployOnComponentsVector.size(); i++) //Makes list of DPD files.
   DPDList.push_back( DeployOnComponentsVector[i].getDPDFile() );
 */

    }
    else
	std::cout << "Device Manager DCD file : " << _deviceConfigurationProfile << " doesn't exist." << std::endl;

}


void
DeviceManager_impl::init ()
{

    _adminState = DEVMGR_UNREGISTERED;
}


void
DeviceManager_impl::getDomainManagerReference (char *domainManagerName)
{
    CORBA::Object_var obj = CORBA::Object::_nil();

/// \todo sleep prevents system from beating Name Service to death, Fix better
    do{
      obj = orb_obj->get_object_from_name (domainManagerName);
      usleep(1000);
    }while(CORBA::is_nil(obj));

    _dmnMgr = CF::DomainManager::_narrow (obj);
}


char *DeviceManager_impl::deviceConfigurationProfile ()
throw (CORBA::SystemException)
{
    return CORBA::string_dup(_deviceConfigurationProfile.c_str());
}


CF::FileSystem_ptr DeviceManager_impl::fileSys ()throw (CORBA::
SystemException)
{
    CF::FileSystem_var result = _fileSys;
    return result._retn();
}


char *DeviceManager_impl::identifier ()
throw (CORBA::SystemException)
{
    return CORBA::string_dup (_identifier.c_str());
}


char *DeviceManager_impl::label ()
throw (CORBA::SystemException)
{
    return CORBA::string_dup (_label.c_str());
}


CF::DeviceSequence *
DeviceManager_impl::registeredDevices ()throw (CORBA::SystemException)
{
    CF::DeviceSequence_var result = new CF::DeviceSequence(_registeredDevices);
    return result._retn();
}


CF::DeviceManager::ServiceSequence *
DeviceManager_impl::registeredServices ()throw (CORBA::SystemException)
{
    CF::DeviceManager::ServiceSequence_var result = new CF::DeviceManager::ServiceSequence(_registeredServices);
    return result._retn();
}


void
DeviceManager_impl::registerDevice (CF::Device_ptr registeringDevice)
throw (CORBA::SystemException, CF::InvalidObjectReference)
{
    if (CORBA::is_nil (registeringDevice)) {
	//writeLogRecord(FAILURE_ALARM,invalid reference input parameter.)

        throw (CF::
            InvalidObjectReference
            ("Cannot register Device. registeringDevice is a nil reference."));
        return;
    }

    // Register the device with the Device manager, unless it is already
    // registered 
    if (!deviceIsRegistered (registeringDevice)) {
        _registeredDevices.length (_registeredDevices.length () + 1);
        _registeredDevices[_registeredDevices.length () - 1] =
            registeringDevice;
    }

    // If this Device Manager is registered with a Domain Manager, register
    // the new device with the Domain Manager
    if (_adminState == DEVMGR_REGISTERED) {
        _dmnMgr->registerDevice (registeringDevice, myObj);
    }

//The registerDevice operation shall write a FAILURE_ALARM log record to a
//DomainManagers Log, upon unsuccessful registration of a Device to the DeviceManagers
//registeredDevices.
}


//This function returns TRUE if the input registeredDevice is contained in the _registeredDevices list attribute
bool DeviceManager_impl::deviceIsRegistered (CF::Device_ptr registeredDevice)
{
//Look for registeredDevice in _registeredDevices
    for (unsigned int i = 0; i < _registeredDevices.length (); i++)
    {
        if (strcmp (_registeredDevices[i]->label (), registeredDevice->label ())
            == 0)
        {
            return true;
        }
    }
    return false;
}


//This function returns TRUE if the input serviceName is contained in the _registeredServices list attribute
bool DeviceManager_impl::serviceIsRegistered (const char *serviceName)
{
//Look for registeredDevice in _registeredDevices
    for (unsigned int i = 0; i < _registeredServices.length (); i++)
    {
        if (strcmp (_registeredServices[i].serviceName, serviceName)  == 0)
        {
            return true;
        }
    }
    return false;
}


void
DeviceManager_impl::unregisterDevice (CF::Device_ptr registeredDevice)
throw (CORBA::SystemException, CF::InvalidObjectReference)
{
    bool deviceFound = false;
    if (CORBA::is_nil (registeredDevice))         //|| !deviceIsRegistered(registeredDevice) )
    {
//The unregisterDevice operation shall write a FAILURE_ALARM log record, when it cannot
//successfully remove a registeredDevice from the DeviceManagers registeredDevices.

//The unregisterDevice operation shall raise the CF InvalidObjectReference when the input
//registeredDevice is a nil CORBA object reference or does not exist in the DeviceManagers
//registeredDevices attribute.
/*writeLogRecord(FAILURE_ALARM,invalid reference input parameter.); */
        throw (CF::
            InvalidObjectReference
            ("Cannot unregister Device. registeringDevice is a nil reference."));

        return;
    }

//The unregisterDevice operation shall remove the input registeredDevice from the
//DeviceManagers registeredDevices attribute.

//Look for registeredDevice in _registeredDevices
    for (unsigned int i = 0; i < _registeredDevices.length (); i++)
    {
        if (strcmp (_registeredDevices[i]->label (), registeredDevice->label ())
            == 0)
        {
//when the appropiater device is found, remove it from the _registeredDevices sequence
            deviceFound = true;
            if (_adminState == DEVMGR_REGISTERED)
            {
                _dmnMgr->unregisterDevice (CF::Device::_duplicate (registeredDevice));
                CORBA::release (registeredDevice);
            }
            for (unsigned int j = i; j < _registeredDevices.length () - 1; j++)
            {
//The unregisterDevice operation shall unregister
//the input registeredDevice from the DomainManager when the input registeredDevice is
//registered with the DeviceManager and the DeviceManager is not shutting down.
                _registeredDevices[j] = _registeredDevices[j + 1];
            }
//_registeredDevices[_registeredDevices.length() - 1] = 0;
            _registeredDevices.length (_registeredDevices.length () - 1);
//TO DO: Avoid memory leaks by reducing the length of the sequence _registeredDevices
            break;
        }
    }
    if (!deviceFound)
    {
/*writeLogRecord(FAILURE_ALARM,invalid reference input parameter.); */

        throw (CF::
            InvalidObjectReference
            ("Cannot unregister Device. registeringDevice was not registered."));
        return;
    }

}


void
DeviceManager_impl::shutdown ()
throw (CORBA::SystemException)
{
    _adminState = DEVMGR_SHUTTING_DOWN;

//The shutdown operation shall unregister the DeviceManager from the DomainManager.
//    _dmnMgr->unregisterDeviceManager (this->_this ()); ///\bug This looks wrong.

//The shutdown operation shall perform releaseObject on all of the DeviceManagers registered
//Devices (DeviceManagers registeredDevices attribute).

    for (int i = _registeredDevices.length () - 1; i >= 0; i--)
    {
//Important Note: It is necessary to manage the lenght of the _registeredDevices sequence
//otherwise, some elements in the sequence will be null.
        _registeredDevices[i]->label ();          ////////////////////////////////////////////////test
        CF::Device_var tempDev = CF::Device::_duplicate (_registeredDevices[i]);
//_registeredDevices[i]->releaseObject();
        unregisterDevice (_registeredDevices[i]);
		try
		{
       		DEBUG(2, DevMgr, "Releasing object: " << tempDev->label())
        	tempDev->releaseObject ();
    	}
    	catch(...)
    	{
        	DEBUG(2, DevMgr, "Error releasing object!")
    	}
        CORBA::release(tempDev);
    }

    _dmnMgr->unregisterDeviceManager (CF::DeviceManager::_duplicate(this->_this ())); ///\bug This looks wrong.
}


void
DeviceManager_impl::registerService (CORBA::Object_ptr registeringService,
const char *name)
throw (CORBA::SystemException, CF::InvalidObjectReference)
{
//This release does not support services
    if (CORBA::is_nil (registeringService))
    {
/*writeLogRecord(FAILURE_ALARM,invalid reference input parameter.); */

        throw (CF::
            InvalidObjectReference
            ("Cannot register Device. registeringDevice is a nil reference."));
        return;
    }

//The registerService operation shall add the input registeringService to the DeviceManagers
//registeredServices attribute when the input registeringService does not already exist in the
//registeredServices attribute. The registeringService is ignored when duplicated.
    if (!serviceIsRegistered (name))
    {
        _registeredServices.length (_registeredServices.length () + 1);
        _registeredServices[_registeredServices.length () - 1].serviceObject = registeringService;
        _registeredServices[_registeredServices.length () - 1].serviceName = name;
    }

//The registerService operation shall register the registeringService with the DomainManager
//when the DeviceManager has already registered to the DomainManager and the
//registeringService has been successfully added to the DeviceManagers registeredServices
//attribute.
    if (_adminState == DEVMGR_REGISTERED)
    {
        _dmnMgr->registerService (registeringService, this->_this (), name);
    }

//The registerService operation shall write a FAILURE_ALARM log record, upon unsuccessful
//registration of a Service to the DeviceManagers registeredServices.
//The registerService operation shall raise the CF InvalidObjectReference exception when the
//input registeringService is a nil CORBA object reference.

}


void
DeviceManager_impl::unregisterService (CORBA::Object_ptr registeredService,
const char *name)
throw (CORBA::SystemException, CF::InvalidObjectReference)
{
    if (CORBA::is_nil (registeredService))
    {
/*writeLogRecord(FAILURE_ALARM,invalid reference input parameter.); */

        throw (CF::
            InvalidObjectReference
            ("Cannot unregister Service. registeringService is a nil reference."));
        return;
    }

//The unregisterService operation shall remove the input registeredService from the
//DeviceManagers registeredServices attribute. The unregisterService operation shall unregister
//the input registeredService from the DomainManager when the input registeredService is
//registered with the DeviceManager and the DeviceManager is not in the shutting down state.

//Look for registeredService in _registeredServices
    for (unsigned int i = 0; i < _registeredServices.length (); i++)
    {
        if (strcmp (_registeredServices[i].serviceName, name) == 0)
        {
//when the appropiater device is found, remove it from the _registeredDevices sequence
            if (_adminState == DEVMGR_REGISTERED)
            {
                _dmnMgr->unregisterService (registeredService, name);
            }

            for (unsigned int j = i; j < _registeredServices.length ()-1; j++)
            {

                CORBA::release (registeredService);
                _registeredServices[j] = _registeredServices[j+1];
            }
            _registeredServices.length (_registeredServices.length () - 1);
            return;
        }
    }

//If it didn't find registeredDevice, then throw an exception
/*writeLogRecord(FAILURE_ALARM,invalid reference input parameter.);*/
    throw (CF::
        InvalidObjectReference
        ("Cannot unregister Service. registeringService was not registered."));
//The unregisterService operation shall write a FAILURE_ALARM log record, when it cannot
//successfully remove a registeredService from the DeviceManagers registeredServices.
//The unregisterService operation shall raise the CF InvalidObjectReference when the input
//registeredService is a nil CORBA object reference or does not exist in the DeviceManagers
//registeredServices attribute.
}


char *
DeviceManager_impl::
getComponentImplementationId (const char *componentInstantiationId)
throw (CORBA::SystemException)
{
//The getComponentImplementationId operation shall return the SPD implementation elements
//ID attribute that matches the SPD implementation element used to create the component
//identified by the input componentInstantiationId parameter.

#if 0
    DCDParser _DCDParser (_deviceConfigurationProfile);
    std::vector < char *>*LocalComponentsVector =
        _DCDParser.getLocalComponents ();
#endif

    cout << "If this appears look at DeviceManager_impl.cpp line 572" << endl;
/*for (int i = 0; i<localComponentsVector->size();i++)
   {
   //get componentInstatiationId from each loal component
   std::vector<ComponentInstantiation*> instantiations = LocalComponentsVector[i].getInstantiations();
   //assuming only one instantiation
   if( strcmp(componentInstantiationId, instantiations[0]->getID()) == 0)
   {
   SPDParser spdParser ( LocalComponentsVector[i].getSPDFile() );
   std::vector<SPDImplementation*>  implementations = spdParser.getImplementations();
   return implementations[0]->getID();
   }
} */
    return "";

//The getComponentImplementationId operation shall return an empty string when the input
//componentInstantiationId parameter does not match the ID attribute of any SPD implementation
//element used to create the component.
}

