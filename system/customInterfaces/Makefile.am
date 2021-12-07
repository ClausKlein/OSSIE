%.pp.idl : %.idl
	@CC@ $(CPPFLAGS) -E -x c++ $< > $@

BUILT_SOURCES = customInterfaces.pp.idl

dist_pkginclude_DATA = customInterfaces.idl \
timingStatus.idl charArray.idl

pkgconfigdir = $(libdir)/pkgconfig
dist_pkgconfig_DATA = customInterfaces.pc

CLEANFILES = customInterfaces.pp.idl

SUBDIRS = python

