#! /usr/bin/env python

from distutils.core import setup
import sys

install_location = '/usr/local/Oasis/Dev_Tools/OSSIECF'

if len(sys.argv) != 2:
        sys.exit(1)

sys.argv.append('--install-lib='+install_location)

setup(name='pass_data_waveform', 
      description='pass_data_waveform',
      data_files=[
                  (install_location+'/waveforms/pass_data_waveform',
                      ['pass_data_waveform.sad.xml', 
                       'pass_data_waveform_DAS.xml'])
                 ]
     )
