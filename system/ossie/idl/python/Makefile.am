IDL_BIN = $(shell which omniidl)

all : 
	$(IDL_BIN) -bpython -Wbpackage=ossie.cf ../cf.idl
	$(IDL_BIN) -bpython -Wbpackage=ossie.cf ../StandardEvent.idl
	$(IDL_BIN) -bpython -Wbpackage=ossie.cf ../PortTypes.idl

install-data-local:
	rm -rf $(DESTDIR)$(pythondir)/ossie/cf
	mkdir -p $(DESTDIR)$(pythondir)
	cp -R ossie $(DESTDIR)$(pythondir)
	
	

distclean:
	rm -rf ossie

clean:
	rm -rf ossie

