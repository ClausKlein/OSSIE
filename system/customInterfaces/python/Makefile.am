IDL_BIN = $(shell which omniidl)

all:
	$(IDL_BIN) -bpython $(CPPFLAGS) -I/usr/local/include -Wbpackage=ossie.custominterfaces -Wbinline ../charArray.idl
	$(IDL_BIN) -bpython $(CPPFLAGS) -I/usr/local/include -Wbpackage=ossie.custominterfaces -Wbinline ../customInterfaces.idl
	$(IDL_BIN) -bpython $(CPPFLAGS) -I/usr/local/include -Wbpackage=ossie.custominterfaces -Wbinline ../timingStatus.idl

install-data-local:
	rm -rf $(DESTDIR)$(pythondir)/ossie/custominterfaces
	mkdir -p $(DESTDIR)$(pythondir)/ossie/custominterfaces
	cp -R ossie/custominterfaces $(DESTDIR)$(pythondir)/ossie

distclean:
	rm -rf ossie

clean:
	rm -rf ossie

