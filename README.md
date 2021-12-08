# OSSIE

## An Open Source Software Defined Radio Platform for Education and Research

OSSIE is an initiative started by the Mobile Portable and Radio Research Group (MPRG) at Virginia Tech University to
provide an open source, C++ based SCA compliant architecture that could be used for research and development of SDRs [1].

The major goals set about for creating OSSIE are to create a design environment with a quick learning curve, to create a
design environment capable of supporting multiple radio interfaces (AM, FM, GSM, 802.11, etc), and to provide an interface
for sharing SDR research and development among different institutions [8].

OSSIE is written in C++ for Linux based operating systems and uses open source supporting software to include CORBA and
Xerces. The first version was released in the summer of 2004 and the latest version (0.6.0) was recently released in the
fall of 2006.


[1] “Software Defined Radio (SDR) with OSSIE Open Source SCA,” OSSIE website, http://ossie.mprg.org. Retrieved February 2007.

[8] M. Robert, P. Balister, and J. DePriest, “SDR Design and the SCA,” unpublished presentation.

[11] M. Robert, J. H. Reed, and J. Smith, “The Joint Tactical Radio System (JTRS) Software Communications Architecture (SCA) Core Framework (CF): A Tutorial,” unpublished document.


## Build Dependencies

 * Boost
 * Python3
 * omniORB
 * xerces-c
 * autoconf
 * automake
 * libtools
 * pkg-config

```
brew install Python3 omniORB xerces-c autoconf automake libtool pkg-config boost
```
