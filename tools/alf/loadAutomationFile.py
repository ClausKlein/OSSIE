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

import xml.dom.minidom  # builtin python XML parser
import compform
import os


#try:  # 0.6.2
from alf_plugins.AWG import AWG
import ossie.standardinterfaces.standardInterfaces__POA as standardInterfaces__POA
import ossie.cf.CF as CF
import cProfile as profile
import pstats
#except ImportError:  # pre 0.6.2
#    import tools.AWG.AWG as AWG
#    import standardInterfaces__POA
#    import CF
#    import profile

import time

import CosNaming    # narrowing naming context stuff
import sys       
from omniORB import CORBA


class automation(standardInterfaces__POA.complexShort):
    def __init__(self, parent, automation_file):
        ''' Parse the XML file to give a list of producers and a list
            of consumers '''
       
        self.connectToolRef = parent
        self.alfFrameRef = parent.alfFrameRef

        self._init_ORB()    # gives me self.orb and self.rootContext

        self.waveform_XML_dir = '/sdr/waveforms/'
        self.comp_XML_dir = '/sdr/xml/'

        self.header_len = 1

        self.profiling_on = False        # True or False
        self.profile_counter = 0
        self.my_profile = profile.Profile()
        # bias is needed when using profile module (not cProfile)
        # This bias is system dependent
        #self.my_profile.bias = 1.6989519401052302e-05
        # profile.bias = 1.6989519401052302e-05
        
        self.packet_counter = 0

        # parse the XML file
        automationXML = xml.dom.minidom.parse(automation_file)

        # producers:
        self.producers_list = []
        producersXML = automationXML.getElementsByTagName('producer')
        for producerXML in producersXML:
            producer_dict = {}
            for n in producerXML.childNodes:
                if n.nodeName != u"#text":
                    # strip() method removes blank spaces
                    producer_dict[n.nodeName] = n.firstChild.data.strip()
            self.producers_list.append(producer_dict)


        # consumers
        self.consumers_list = []
        consumersXML = automationXML.getElementsByTagName("consumer")
        for consumerXML in consumersXML:
            consumer_dict = {}
            for n in consumerXML.childNodes:
                if n.nodeName != u"#text":
                    # strip() method removes blank spaces 
                    consumer_dict[n.nodeName] = n.firstChild.data.strip()
                    if n.nodeName == u'install_at_startup':
                        if not(
                        n.firstChild.data.find("True")!=-1 
                     or n.firstChild.data.find("False")!=-1):
                            print "ERROR: XML node install_at_startup must be either true or false"
                            return
            self.consumers_list.append(consumer_dict)


        # Look for consumer applications that need to be installed at startup
        # and install them.
        counter = 0
        while counter < len(self.consumers_list):

            if self.consumers_list[counter].has_key('waveformInstance'):
                self.consumers_list[counter] = self._find_app_ref(
                                                self.consumers_list[counter])
        
                # set install at startup to true so that the initial
                # connection will be set up
                self.consumers_list[counter]['install_at_startup'] = 'True'

            elif self.consumers_list[counter]['install_at_startup'].find('True')!=-1:
                self.consumers_list[counter] = self._install_necessary_waveform(self.consumers_list[counter])
            counter += 1


        # Look for producer applications that need to be installed at startup
        # and install them.
        counter = 0
        while counter < len(self.producers_list):
            
            if self.producers_list[counter].has_key('waveformInstance'):
                self.producers_list[counter] = self._find_app_ref(
                                                self.producers_list[counter])
                # set install at startup to true so that the initial
                # connection will be set up
                self.producers_list[counter]['install_at_startup'] = 'True'
                counter += 1
                continue

            self.producers_list[counter] = self._install_necessary_waveform(self.producers_list[counter])
            counter += 1

        self._create_initial_connections()


    def _init_ORB(self):
        ''' creates self.orb and self.rootContext '''
        self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        obj = self.orb.resolve_initial_references("NameService")
        self.rootContext = obj._narrow(CosNaming.NamingContext)
        if self.rootContext is None:
            print "Failed to narrow the root naming context"
            sys.exit(1)


    def _find_app_ref(self, prod_or_cons_dict):
        ''' This method will use the waveformInstace key of the incomming
            dictionary to find an application reference.  The application
            reference ("app_ref") will be added to the dictionary '''
       
        appSeq = self.alfFrameRef.domMgr._get_applications()
        for tmp_app in appSeq:
            compNameCon = tmp_app._get_componentNamingContexts()
            for compElementType in compNameCon:
                if prod_or_cons_dict['waveformInstance'] in compElementType.elementId:
                    print "found the application"
                    prod_or_cons_dict['app_ref'] = tmp_app
                    break

        return prod_or_cons_dict


    def _install_necessary_waveform(self, prod_or_cons_dict):
        ''' Private.  Installs an application based on incomming dictionary.
            The dictionary should originate from the XML file that was
            parsed durring startup'''

        #for dict in objects_list:
        if prod_or_cons_dict.has_key('toolname'):
            # If I'm dealing with an alf tool
            prod_or_cons_dict['tool_ref'] = self.create_tool(prod_or_cons_dict)

        else:
            # Do the necessary installation of waveform or compform
            # make initial connections when necessary            
            if 'waveform' not in prod_or_cons_dict:
                if 'component' not in prod_or_cons_dict:
                    print "ERROR: producer or consumer defined in XML file does not seem to have a waveformInstance, a toolname, a waveform, or a component"
                else:
                    # Install compform
                    prod_or_cons_dict['app_ref'] = self.install_compform_from_dict(prod_or_cons_dict)

                    compNamingCon = prod_or_cons_dict['app_ref']._get_componentNamingContexts()

                    waveInstName = compNamingCon[0].elementId.split('/')[1]
                    prod_or_cons_dict['waveformInstance'] = waveInstName

                prod_or_cons_dict['waveformInstance'] = prod_or_cons_dict['app_ref']._get_componentNamingContexts()

            else:  # have a waveform to install
                prod_or_cons_dict['app_ref'] = self.install_waveform_from_dict(prod_or_cons_dict)
                compNamingCon = prod_or_cons_dict['app_ref']._get_componentNamingContexts()

                waveInstName = compNamingCon[0].elementId.split('/')[1]
                prod_or_cons_dict['waveformInstance'] = waveInstName
                    

        return prod_or_cons_dict


    def create_tool(self, tool_dict):
        if tool_dict['toolname'] == "AWG":
            return AWG.create_from_other_tool(self.connectToolRef)


    def install_compform_from_dict(self, compform_dict):
        compName = str(compform_dict['component'])
        compNameAndDir = self.comp_XML_dir + compName 

        self.alfFrameRef.compform_counter = self.alfFrameRef.compform_counter + 1

        tmp_dir_name = "/sdr/_tmp_alf_waveforms/"  # this is where I put my temporary
                                              # xml files
        tmp_wave_name = "_" + compName + str(self.alfFrameRef.compform_counter)


        #make the directory to put the XML
        if os.path.exists(tmp_dir_name) == False:
            try:
                os.mkdir(tmp_dir_name)   
            except:
                errorMsg(self,"Cannot create temporary directory in the waveform directory.  You may need to change the temporary directory to one that you have write permissions to")

        if os.path.exists(tmp_dir_name + tmp_wave_name) == False:   
            try:
                os.mkdir(tmp_dir_name + tmp_wave_name)
            except:
                errorMsg(self,"Cannot create temporary directory in the waveform directory.  You may need to change the temporary directory to one that you have write permissions to")
                return
 

        # assumes that alf is in /sdr/tools
        my_compform = compform.compform(compName, compNameAndDir, 
                                        tmp_dir_name, tmp_wave_name)
        my_compform.create()

     
        print "WARNING: tmp files generated in " + tmp_dir_name

        tmp_dir_name = tmp_dir_name +  tmp_wave_name + "/"

        app_ref = self.alfFrameRef.InstallWaveform(tmp_wave_name + ".sad.xml", 
                                   tmp_dir_name + tmp_wave_name + ".sad.xml",
                                   tmp_wave_name + "_DAS.xml",
                                   tmp_dir_name + tmp_wave_name + "_DAS.xml")

        return app_ref



    def install_waveform_from_dict(self, waveform_dict):
        ''' Installs a waveform application as an SCA application based on 
            the given dictionary.  Dictionary should originate from the 
            XML parsing done durring module initialization'''
 
        name_SAD = str(waveform_dict['waveform']) + '.sad.xml'
        absolute_name_SAD = self.waveform_XML_dir + str(waveform_dict['waveform']) + "/" + name_SAD

        name_DAS = str(waveform_dict['waveform']) + '_DAS.xml'
        absolute_name_DAS = self.waveform_XML_dir + str(waveform_dict['waveform']) + "/" + name_DAS

        app_ref = self.alfFrameRef.InstallWaveform(name_SAD, absolute_name_SAD,
                                         name_DAS, absolute_name_DAS)

        return app_ref


    def _create_initial_connections(self):
        ''' This is where I set up the initial connections 
            for applications installed at startup'''

        counter = 0
        for consumer in self.consumers_list:
            if consumer[u'install_at_startup'].find(u'True') != -1:
                self.consumers_list[counter]['PortHandle'] = self.connect_to_consumer_comp(consumer)
            counter +=1

        counter = 0
        for producer in self.producers_list:
            if producer.has_key('toolname'):
                continue  # connecting to the tool is handled elsewhere
            else:
                self.producers_list[counter]['PortHandle'] = self.connect_to_producer_component(producer)

            counter += 1


    def connect_to_consumer_comp(self, consumer_dict):
        ''' Connects the consumer component's provides port to self.  
            returns a port handle'''

        # Format the domain, waveform, and component name so that
        # the root context can understand it
        name = [CosNaming.NameComponent("DomainName1" ,"" ),
           CosNaming.NameComponent(str(consumer_dict['waveformInstance']) ,"" ),
           CosNaming.NameComponent(str(consumer_dict['componentInstance']) ,"" )]

        # Attempt to get a reference to the resource
        try:
            ResourceRef = self.rootContext.resolve(name)
        except:
            # could not find the resource.  Something has gone wrong.  Throw error.
            print "Required resource not found in the naming service"
            sys.exit(1)

        # connect to an existing port
        ResourceHandle = ResourceRef._narrow(CF.Resource)
        PortReference = ResourceHandle.getPort(str(consumer_dict['port']))
            
        if PortReference is None:
            # the component's getPort method did not give me a port reference for some reason
            print "WANRING: failed to get Port Reference from consumerresource"


        # return portHandle
        # Assuming complexShort
        return PortReference._narrow(standardInterfaces__POA.complexShort)


    def connect_to_producer_component(self, producer_dict):
        ''' Returns a PortHandle that will allow you to call disconnect later'''

        name = [CosNaming.NameComponent("DomainName1" ,"" ),
           CosNaming.NameComponent(str(producer_dict['waveformInstance']) ,"" ),
           CosNaming.NameComponent(str(producer_dict['componentInstance']) ,"" )]

        try:
            ResourceRef = self.rootContext.resolve(name)
        except:
            print "FATAL ERROR:  Required resource (producer) not found in connect_to_producer_component method"
            sys.exit(1)

        ResourceHandle = ResourceRef._narrow(CF.Resource)

        # get a reference to the uses port
        PortReference = ResourceHandle.getPort(str(producer_dict[u'port']))
        if PortReference is None:
            print "getPort from a producer component did not return a valid port reference"
        PortHandle = PortReference._narrow(CF.Port)

        PortHandle.connectPort(self._this(),
                             "connection_id:_" + str(producer_dict['port']))


    def stripHeader(self, data):
        return data[self.header_len: len(data)]



    # -------------------------------------------------------------------
    # Begin push packet methods:

    def pushPacketMetaData(self, I_data, Q_data, metadata):
        print "WARNING: metadata not yet supported in automations.py"
        print "metadata is being ignored"

        # TODO: get the metadata that describes where the packet is going, 
        # and inset it to the beginning of the packet
        self.pushPacket(I_data, Q_data)


    def pushPacket(self, I_data, Q_data):

        if self.profiling_on:
            tmp_filename = "profiles/pushPacket_" + str(self.profile_counter) + ".profile"

            self.my_profile.runctx("tmp_self._pushPacket(I_data, Q_data)",
                    None,
                    {"tmp_self": self, "I_data": I_data, "Q_data": Q_data})
            self.my_profile.dump_stats(tmp_filename)

            self.profile_counter += 1

        else:   # profiling off
            self._pushPacket(I_data, Q_data)
    
    def _pushPacket(self, I_data, Q_data):
       
        consumer_index = -1  # I have to start at -1 so that I increment
                             # the index before the main body of the for 
                             # loop.  This way i never miss the incrementation
                             # if I use a continue statement

        current_packet_header = I_data[0]
        
        I_data = self.stripHeader(I_data)
        Q_data = self.stripHeader(Q_data)

        for consumer in self.consumers_list:

            consumer_index += 1
            if int(consumer[u'header']) == abs(current_packet_header):

                if current_packet_header >= 0:
                    # send data to the consumer, install if necessary
     
                    if consumer.has_key('app_ref'):
                        # application already installed, send it data
                        consumer['PortHandle'].pushPacket(I_data, Q_data)

                    else:
                        # install the application, connect, then send data
                        self.consumers_list[consumer_index] = self._install_necessary_waveform(consumer)
                        self.consumers_list[consumer_index]['PortHandle'] = self.connect_to_consumer_comp(consumer)
                        self.consumers_list[consumer_index]['PortHandle'].pushPacket(I_data, Q_data)



                else:   # current_packet_header < 0
                        # this is the uninstall case
                    
                    I_data = self.stripHeader(I_data)
                    Q_data = self.stripHeader(Q_data)
                    if consumer.has_key('PortHandle'):

                        # send the last piece of data
                        consumer['PortHandle'].pushPacket(I_data, Q_data)
   

                    else:     
                        # Header is negative and connection does not exist
                        # install the application, connect, send data, then uninstall

                        self.consumers_list[consumer_index] = self._install_necessary_waveform(consumer)
            
                        self.consumers_list[consumer_index]['PortHandle'] = self.connect_to_consumer_comp(consumer)

                        self.consumers_list[consumer_index]['PortHandle'].pushPacket(I_data, Q_data)


                    # uninstall the consumer application
                    self.consumers_list[consumer_index]['app_ref'].releaseObject()

                    # remove unwanted keys from the appropriate consumers dictionary
                    del self.consumers_list[consumer_index]['app_ref']
                    del self.consumers_list[consumer_index]['PortHandle']
                    del self.consumers_list[consumer_index]['waveformInstance']    


    # end push packet methods
    # --------------------------------------------------------------------


    def __del__(self):
        pass



