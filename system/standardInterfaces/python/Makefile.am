IDL_BIN = $(shell which omniidl)

all:
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../realChar.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../realShort.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../realLong.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../realFloat.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../realDouble.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../complexShort.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../complexFloat.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../complexDouble.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../complexChar.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../complexLong.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../Radio_Control.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../FM_Control.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../soundControl.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../stereoSound.idl
	$(IDL_BIN) -bpython $(IDL_FLAGS) -I/usr/local/include -Wbpackage=ossie.standardinterfaces -Wbinline ../sampleRateConvertorControl.idl

install-data-local:
	rm -rf $(DESTDIR)$(pythondir)/ossie/standardinterfaces
	mkdir -p $(DESTDIR)$(pythondir)/ossie/standardinterfaces
	cp -R ossie/standardinterfaces $(DESTDIR)$(pythondir)/ossie

distclean:
	rm -rf ossie

clean:
	rm -rf ossie

