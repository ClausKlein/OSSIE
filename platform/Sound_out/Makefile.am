%SK.cpp %.h :
	@IDL@ @IDL_FLAGS@ -bcxx -Wbh=.h -Wbs=SK.cpp -Wbkeep_inc_path soundControl.idl
       
AM_CXXFLAGS = -Wall

bin_PROGRAMS = soundCardPlayback
soundCardPlayback_SOURCES =         \
    main.cpp                        \
    soundCardPlayback.h             \
    soundCardPlayback.cpp           \
    port_impl.cpp

BUILT_SOURCES =                     \
   soundControlSK.cpp               

CLEANFILES =                        \
    soundControlSK.cpp              \
    soundControl.h                  

nodist_soundCardPlayback_SOURCES =  \
    soundControlSK.cpp              

ossieName = soundCardPlayback
xmldir = $(prefix)/xml/$(ossieName)
bindir = $(prefix)/bin

dist_xml_DATA =                     \
    soundCardPlayback.scd.xml       \
    soundCardPlayback.spd.xml       \
    soundCardPlayback.prf.xml


# ---------- documentation ---------

docs :
	doxygen Doxyfile

