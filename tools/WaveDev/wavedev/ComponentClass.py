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

import uuidgen

# Component Class
class Component:
  def __init__(self, name="",AC=False,type="resource",description="",generate=True):
    self.name = name        # this refers to the instance name
    self.baseName = name    # this refers to the component that the instance is based on
    self.connections = []
    self.ports = []
    self.mutable_params = []
    self.device = None
    self.node = None
    self.uuid = uuidgen.uuidgen()
    self.file_uuid = uuidgen.uuidgen()
    self.ace = False
    self.timing = False
    self.AssemblyController = AC
    self.type = type
    self.generate = generate
    self.xmlName = name     #if imported from component library - this may change
    self.properties = []
    self.description = description

  def __getitem__(self,i):
      return self.connections[i]

  def setUUID(self):
      self.uuid = uuidgen.uuidgen()

  def changeName(self,newname):
      self.name = newname
      if self.generate == True:
          self.baseName = newname
          self.xmlName = newname

class Node:
  def __init__(self, name="", path="", description="", generate=True):
    self.name = name
    self.path = path
    self.Devices = []
    self.type = "node"
    self.generate = generate
    self.description = description
    self.id = ""

  def addDevice(self, in_dev=None):
    if in_dev != None:
      self.Devices.append(in_comp)


class Port:
  def __init__(self, name, interface, type="Uses",portType="data"):#,dataType="ShortSequence",interface_ns="standardInterfaces"):
    self.name = name
    self.interface = interface
    self.portType = portType    #control or data
    self.type = type            #Uses or Provides
    self.u_cname = "dataOut_" + interface.name + "_i"
    self.p_cname = "dataIn_" + interface.name + "_i"
    if type == "Uses":
        self.cname = self.u_cname
    if type == "Provides":
        self.cname = self.p_cname

class Connection:
    def __init__(self, LP, RP, RC):
        self.localPort = LP
        self.remotePort = RP
        self.remoteComp = RC

class Interface:
    def __init__(self,name,nameSpace="standardInterfaces",operations=[],filename="",fullpath=""):
        self.name = name
        self.nameSpace = nameSpace
        self.operations = []
        self.filename = filename    #does not include the '.idl' suffix
        self.fullpath = fullpath

    def __eq__(self,other):
        if isinstance(other, Interface):
            return (other.nameSpace == self.nameSpace ) and (other.name == self.name)
        else:
            return False

    def __ne__(self,other):
        if isinstance(other, Interface):
            return (other.nameSpace != self.nameSpace ) and (other.name != self.name)
        else:
            return True


class Operation:
    def __init__(self,name,returnType,params=[]):
        self.name = name
        self.returnType = returnType
        self.cxxReturnType = ''
        self.params = []

class Param:
    def __init__(self,name,dataType='',direction=''):
        """
        Exampleinterface complexShort {
            void pushPacket(in PortTypes::ShortSequence I, in PortTypes::ShortSequence Q);
        };
        """

        self.name = name            # The actual argument name: 'I'
        self.dataType = dataType    # The type of the argument: 'PortTypes::ShortSequence'
        self.cxxType = ""
        self.direction = direction  # Flow of data: 'in'

class Property:
    def __init__(self,elementType,name,mode,description=''):
        self.elementType = elementType
        self.name = name
        self.mode = mode
        self.id = 'DCE:' + uuidgen.uuidgen()

class SimpleProperty(Property):
    def __init__(self,name,mode,type,description='',value=None,defaultValue=None,units=None,
                range=(-1,-1),enum='',kind='configure',action=None):
        Property.__init__(self,"Simple",name,mode,description)
        self.type = type
        self.description = description
        self.value = value
        self.defaultValue = defaultValue
        self.units = units
        self.range = range
        self.enum = enum
        self.kind = kind
        self.action = action

class SimpleSequenceProperty(Property):
    def __init__(self,name,mode,type,description='',values=[],defaultValues=[],units=None,range=(-1,-1),kind='configure',action=None):
        Property.__init__(self,"SimpleSequence",name,mode,description)
        self.type = type
        self.description = description
        self.values = values
        self.defaultValues = defaultValues
        self.units = units
        self.range = range
        self.kind = kind
        self.action = action


