#! /usr/bin/env python

## Copyright 2005, 2006 Virginia Polytechnic Institute and State University
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

import os,sys,re,string
import gzip

def beautify(data,output=""):
    store_stdout = sys.stdout
    if len(output) > 0:
        sys.stdout = open(output,'w')

    myprint = sys.stdout.write

    fields = re.split('(<.*?>)',data)
    #remove any lone instances of '\n' or '\t' or pure whitespace strings
    for x in fields:
        if '\n' in x or '\t' in x or x=='' or x.isspace():
            fields.remove(x)
    level = 0
    f = fields
    for x in range(len(f)):
        if string.strip(f[x])=='': continue
        if f[x][0]=='<' and f[x][1] != '/' and f[x][1] != '!':
            if f[x][1]!='?':
                print ''
            myprint(' '*(level*4) + f[x])
            if f[x][-2:] != "/>" and f[x][:2] != "<?":
                level = level + 1
        elif f[x][:2]=='</':
            level = level - 1
            if x>0 and len(f[x-1]) > 0 and f[x-1][0] !='<' and f[x-1][0] != '\n':
                print f[x],
            else:
                print ''
                myprint(' '*(level*4) + f[x])
        elif f[x][:2]=='<!':
            print ''
            print ' '*(level*4) + f[x],
        else:
            if x>0 and len(f[x-1]) > 0 and f[x-1][0] =='<':
                myprint(f[x])
            else:
                print ' '*(level*4) + f[x],

    if len(output) > 0:
        print ''
        sys.stdout = store_stdout

if __name__ == "__main__":
    fname = sys.argv[1]
    if fname[-2:] == 'gz':
        data = gzip.GzipFile(fname,'r').read()
    else:
        data = open(fname,'r').read()
    beautify(data)
