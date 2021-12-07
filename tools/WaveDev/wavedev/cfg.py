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

##-------------------------------------------------------------------------
## This file defines basic methods for retrieving information from the
## wavedev.cfg file.
##-------------------------------------------------------------------------
import xml.dom.minidom
import os

##-------------------------------------------------------------------------
## Public functions
##-------------------------------------------------------------------------

def version():
    return ossieCfgValue('version')


def ossieInstallDir():
    return ossieCfgValue('installpath')


def ossieCfgValue(key):
    if __overrides.has_key(key):
        return __overrides[key]
    else:
        val = __keyFromXml(key)
        # cache it
        setCfgValueIfNecessary(key)
        return val


def overrideCfgValue(key, value):
    __overrides['key'] = value


def setCfgValueIfNecessary(key, value):
    if not __overrides.has_key(key):
        overrideCfgValue(key, value)


def commentLine():
    if __commentLine == None:
        __commentLine = u'<!--Created with OSSIE WaveDev ' + version() \
            + u'-->\n<!--Powered by Python-->\n'
    return __commentLine


##-------------------------------------------------------------------------
## Internal
##-------------------------------------------------------------------------

__overrides = {'installpath' : '/sdr' }
__cachedXml = None
__commentLine = None


def __xml():
    if __cachedXML == None:
        fileName = '../wavedev.cfg'
        if not os.path.exists(fileName):
            fileName = ossieInstallDir() + '/toos/WaveDev/wavedev.cfg'
        if os.path.exists(fileName):
            __cachedXml = xml.dom.minidom.parse(fileName)
    return __cachedXml


def __keyFromXml(key):
    result = None
    if __xml() != None:
        result = str(__xml().getElementsByTagName(key)[0].firstChild.data)
    return result
