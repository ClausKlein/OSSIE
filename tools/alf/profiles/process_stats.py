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

import profile
import pstats
import os
import re


if __name__ == "__main__":

    profile_files = os.listdir(".")

    my_stats = None


    for file in profile_files:
        if file.find(".profile") != -1:
            if my_stats == None:
                my_stats = pstats.Stats(file)
            else:
                my_stats.add(file)
    
    

    my_stats.strip_dirs()

    #my_stats.sort_stats('time')
    #my_stats.print_stats()


    
    my_stats.sort_stats('cumulative')
    my_stats.print_stats()

    #my_stats.sort_stats('name')
    #my_stats.print_stats()

    #my_stats.print_callers()
    #my_stats.print_callees()


    '''
    my_stats.sort_stats('line')
    my_stats.print_stats()
    

    my_stats.sort_stats('calls')
    my_stats.print_stats(50)


    '''



