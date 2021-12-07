#!/usr/bin/python
'''Usage: %s [OPTIONS]
OSSIE build script
'''

## Copyright 2007 Virginia Polytechnic Institute and State University
##
## This file is part of the OSSIE Installer.
##
## OSSIE Installer is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## OSSIE Installer is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with OSSIE Installer; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import sys

# Global variables
ossieversion = "0.7.0"

def usageString():
    '''Construct program usage string'''
    return __doc__ % sys.argv[0]

def Usage( problem = None):
    '''print usage'''
    if problem is None:
        print(usageString())
        sys.exit(0)
    else:
        sys.stderr.write( usageString() )
        Abort(problem)

def Abort(problem):
    '''Print error message and exit'''
    sys.stderr.write('\n')
    sys.stderr.write(problem)
    sys.stderr.write('\n\n')
    sys.exit(2)

def BuildDirectory(installasroot=False):
    '''Try to rebuild directory'''
    if not os.access('.doNotBuild', os.F_OK):

        if (os.system('libtoolize -i') != 0):
            if (os.system('glibtoolize -i --force') != 0):
                print('FAILED: libtoolize -i')
                return False
        if (os.system('./reconf') != 0):
            print('FAILED: reconf')
            return False
        if (os.system('CXXFLAGS=-std=c++11 ./configure --prefix=$ESSOR_NTE_PRT_HOME') != 0):
            print('FAILED: configure')
            return False
        if (os.system('make -j') != 0):
            print('FAILED: make -j')
            return False
        if installasroot:
            if (os.system('make install') != 0):
                print('FAILED: make install')
                return False
        else:
            if (os.system('make install') != 0):
                problemstr  = 'FAILED: make install\n'
                problemstr += '  Try changing permissions on install directory, e.g.\n'
                problemstr += '  # chown -R myusername.myusername /sdr'
                Abort(problemstr)
        print("\nPackage installed\n")
        return True
    else:
        print("Ignoring directory\n")
        return True



if __name__ == '__main__':
    if len(sys.argv) != 1:
        Usage()

    # check for existence, ownership of /sdr
    #if not os.path.exists(os.path.sep + 'sdr'):
        # /sdr does not exist
        #problemstr  = "  ERROR: directory " + os.path.sep + "sdr does not exist\n"
        #problemstr += "  Create with root permissions, and change ownership:\n"
        #problemstr += "    # mkdir /sdr\n"
        #problemstr += "    # chown -R myusername.myusername /sdr"
        #Abort(problemstr)
    #elif os.stat(os.path.sep + 'sdr')[5] == 0:
        # /sdr exists but owned by root
        #problemstr  = "  ERROR: directory " + os.path.sep + "sdr is owned by root\n"
        #problemstr += "  Change ownership:\n"
        #problemstr += "    # chown -R myusername.myusername /sdr"
        #Abort(problemstr)

    cwd = os.getcwd()

    # build system
#    system_dirs = ['ossie', 'standardInterfaces', 'customInterfaces', 'nodebooter', 'wavLoader', 'SigProc',]
    system_dirs = ['ossie', 'standardInterfaces', 'nodebooter', 'wavLoader', 'SigProc',]
    for dir in system_dirs:
        path = 'system' + os.path.sep + dir
        os.chdir(cwd + os.path.sep + path)
        print("building " + path + "...")

        if not BuildDirectory( True ):
            Abort("ERROR: building " + path + " failed")

    """
    # build platform
    platform_dirs = ['GPP', 'domain', 'dtd', 'nodes/default_GPP_node', ]
    for dir in platform_dirs:
        path = 'platform' + os.path.sep + dir
        os.chdir(cwd + os.path.sep + path)
        print "building " + path + "..."

        if not BuildDirectory( False ):
            Abort("ERROR: building " + path + " failed")

    # build components
    components_dirs = ['TxDemo', 'ChannelDemo', 'RxDemo', 'am_demod', 'amplifier', 'AutomaticGainControl', 'Decimator', 'WFMDemod',]
    for dir in components_dirs:
        path = 'components' + os.path.sep + dir
        os.chdir(cwd + os.path.sep + path)
        print "building " + path + "..."

        if not BuildDirectory( False ):
            Abort("ERROR: building " + path + " failed")

    # build waveforms
    waveforms_dirs = ['ossie_demo', ]
    for dir in waveforms_dirs:
        path = 'waveforms' + os.path.sep + dir
        os.chdir(cwd + os.path.sep + path)
        print "building " + path + "..."

        if not BuildDirectory( False ):
            Abort("ERROR: building " + path + " failed")

    # build pass_data component and waveform
    os.chdir(cwd + os.path.sep + 'components/pass_data')
    if (os.system('python setup.py install') != 0):
        Abort("ERROR: building pass_data component failed")
    print "building pass_data ..."

    os.chdir(cwd + os.path.sep + 'waveforms/pass_data_waveform')
    if (os.system('python setup.py install') != 0):
        Abort("ERROR: building pass_data_waveform failed")
    print "building pass_data_waveform ..."
    """

    # successful install message
    print("\n" + "*"*60 + "\n")
    print("    Complete installation of OSSIE " + ossieversion + " finished!")
    print("\n" + "*"*60 + "\n")

    print("    NOTE: If this is your first time installing OSSIE you will")
    print("    need to link the libraries.  Edit /etc/ld.so.conf and add")
    print("      $ESSOR_NTE_PRT_HOME/lib")
    print("    As root run /sbin/ldconfig\n")
    os.system('date')
    sys.exit(0)




