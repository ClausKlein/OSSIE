AM_CXXFLAGS = -Wall 

bin_PROGRAMS = AutomaticGainControl

AutomaticGainControl_SOURCES =          \
    src/AutomaticGainControl.cpp        \
    src/AutomaticGainControl.h          \
    src/main.cpp

ossieName = AutomaticGainControl
xmldir = $(prefix)/xml/$(ossieName)
bindir = $(prefix)/bin

dist_xml_DATA =                         \
    xml/AutomaticGainControl.prf.xml    \
    xml/AutomaticGainControl.scd.xml    \
    xml/AutomaticGainControl.spd.xml

# ---------- documentation ---------

# make sure "make docs" doesn't conflict with
# separate docs/ directory
.PHONY: docs documentation

docs :
	./genDocs.py


