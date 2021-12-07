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

import os, sys
import string

try:
    from omniidl import idlast, idlvisitor, idlutil, main, idltype
    from omniidl_be.cxx import types
    import _omniidl
except ImportError:
    print "ERROR: importIDL.py cannot import the omniidl module"
    print "  - Is omniORBpy installed?"
    print "  - Is /usr/local/lib/pythonX.X/site-packages included in ossie.pth?"
    sys.exit(0)

import ComponentClass as CC

keyList = range(34)
valList = ['null','void','short','long','ushort','ulong','float','double','boolean', \
           'char','octet','any','TypeCode','Principal','objref','struct','union','enum', \
           'string','sequence','array','alias','except','longlong','ulonglong', \
           'longdouble','wchar','wstring','fixed','value','value_box','native', \
           'abstract_interface','local_interface']
baseTypes = dict(zip(keyList,valList))

# Non-standard kinds for forward-declared structs and unions
baseTypes[100] = 'ot_structforward'
baseTypes[101] = 'ot_unionforward'

class ExampleVisitor (idlvisitor.AstVisitor):
    def __init__(self,*args):
        self.myInterfaces = []   #Used to store the interfaces that are found
        if hasattr(idlvisitor.AstVisitor,'__init__'):
            idlvisitor.AstVisitor.__init__(self,args)

    def visitAST(self, node):
        for n in node.declarations():
            n.accept(self)

    def visitModule(self, node):
        for n in node.definitions():
            n.accept(self)

    def visitInterface(self, node):
        new_int = CC.Interface(node.identifier(),node.scopedName()[0])
        
	ops_list = []
 	self.addOps(node,ops_list)
        new_int.operations.extend(ops_list)
        #print node.identifier() + " has " + str(len(new_int.operations)) + " operations"
        self.myInterfaces.append(new_int)

    def addOps(self,node,ops):
	
	for i in node.inherits():
            self.addOps(i,ops)

        for d in node.contents():
            if isinstance(d, idlast.Operation):
                new_op = CC.Operation(d.identifier(),baseTypes[d.returnType().kind()])
                # Get the c++ mappping of the return type
                cxxRT = types.Type(d.returnType())
                new_op.cxxReturnType = cxxRT.base()
#                if new_op.returnType == 'string':
#                    print foo2.base()
                #print new_op.name + "::" + d.identifier() + "()"
                #tmpstr = node.identifier() + "::" + d.identifier() + "("
                #tmpstr2 = "  " + node.identifier() + "::" + d.identifier() + "("
                if hasattr(d,'parameters'):
                    for p in d.parameters():
                        new_param = CC.Param(p.identifier())
                        t =  p.paramType()
                        # Get the c++ mapping of the type
                        cxxT = types.Type(t)
                        new_param.cxxType = cxxT.op(types.direction(p))
						
                        if hasattr(t,'scopedName'):
                            #print ' '*8 + str(t.scopedName()),
                            new_param.dataType = idlutil.ccolonName(t.scopedName())
                        else:
                            if isinstance(t,idltype.Type):
                                #print ' '*8 + baseTypes[t.kind()],
                                new_param.dataType = baseTypes[t.kind()]

                        if p.is_in() and p.is_out():
                            new_param.direction = 'inout'
                        elif p.is_out():
                            new_param.direction = 'out'
                        else:
                            new_param.direction = 'in'
                        new_op.params.append(new_param)
                        #tmpstr += new_param.direction + " " + new_param.dataType + ","
                        #tmpstr2 += new_param.direction + " " + new_param.cxxType + ","
                ops.append(new_op)
                #print tmpstr[:-1] + ")"
                #print tmpstr2[:-1] + ")"

def run(tree, args):
    visitor = ExampleVisitor()
    tree.accept(visitor)
    return visitor.myInterfaces

def getInterfaces(filename):
  f = os.popen(main.preprocessor_cmd + ' -I "/usr/local/include" -I "/usr/include" "' \
               + filename + '"','r')
  tree = _omniidl.compile(f)
  ints = run(tree,'')
  f.close()
  del tree
  idlast.clear()
  idltype.clear()
  _omniidl.clear()
  #store file name and location information for each interface
  for x in ints:
      x.fullpath = filename
      i = filename.rfind("/")
      if i >= 0:
          x.filename = filename[i+1:]
          
      x.filename = x.filename[:-4] #remove the .idl suffix
    
      
  return ints
  

if __name__ == '__main__':
    print "Command line not supported in this version"
