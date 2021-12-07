AM_CXXFLAGS = -Wall

bin_PROGRAMS = soundCardCapture

soundCardCapture_SOURCES =          \
    main.cpp                        \
    soundCardCapture.cpp            \
    soundCardCapture.h

ossieName = soundCardCapture
xmldir = $(prefix)/xml/$(ossieName)
bindir = $(prefix)/bin

dist_xml_DATA =                     \
    soundCardCapture.scd.xml        \
    soundCardCapture.spd.xml        \
    soundCardCapture.prf.xml


# ---------- documentation ---------

docs :
	doxygen Doxyfile


