#! /usr/bin/env python

from distutils.core import setup
import sys

if len(sys.argv) != 2:
	sys.exit(1)

# Packages
generate=['WaveDev/wavedev/generate', 'WaveDev/wavedev/generate/templates', 'WaveDev/wavedev/generate/templates/basic_ports', 'WaveDev/wavedev/generate/templates/custom_ports', 'WaveDev/wavedev/generate/templates/py_comp']
wavedev_packages=['WaveDev', 'WaveDev/wavedev', 'WaveDev/wavedev/XML_gen'] + generate
alf_plugins=['alf_plugins', 'alf_plugins/AWG', 'alf_plugins/plot', 'alf_plugins/speaker', 'alf_plugins/write_to_file']

# ALF Files
alf_files=['images/*', 'config/*', 'LICENSE']

# ALF Plugin Files
awg_files=['toolconfig.xml']
plot_files=['toolconfig.xml']
speaker_files=['audio-off.xpm', 'audio-on.xpm', 'toolconfig.xml']
write_to_file_files=['toolconfig.xml']

# WaveDev Files
WaveDev_files=['INSTALL', 'LICENSE', 'README.txt', 'wavedev.cfg']
wavedev_files=['images/*']
xml_gen_files=['templates/*', 'DevMan/*', 'dtd/*', 'README', '*.tpl']
generate_files=['gpl_preamble', 'basic_xml/*', 'LICENSE', 'reconf']
basic_ports_files=['*.cpp', '*.h', 'sampleDocumentation.txt', 'sampleDoxyfile']
custom_ports_files=['*.cpp', '*.h']
py_comp_files=['README']

setup(
      name='ossietools', 
      version='0.7.0',
      description='ossietools',
      packages=wavedev_packages + ['alf'] + alf_plugins,
      package_data={
          'WaveDev' : WaveDev_files, \
          'WaveDev/wavedev' : wavedev_files, \
          'WaveDev/wavedev/XML_gen' : xml_gen_files, \
          'WaveDev/wavedev/generate' : generate_files,
          'WaveDev/wavedev/generate/templates/basic_ports' : basic_ports_files, \
          'WaveDev/wavedev/generate/templates/custom_ports' : custom_ports_files, \
          'WaveDev/wavedev/generate/templates/py_comp' : py_comp_files, \
          'alf' : alf_files, \
          'alf_plugins/AWG' : awg_files, \
          'alf_plugins/speaker' : speaker_files, \
          'alf_plugins/plot' : plot_files, \
          'alf_plugins/write_to_file' : write_to_file_files },
      scripts=['ALF', 'OWD', 'OWDC'],
     )
