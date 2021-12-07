/****************************************************************************

Copyright 2006, Virginia Polytechnic Institute and State University

This file is part of the OSSIE Core Framework.

OSSIE Core Framework is free software; you can redistribute it and/or modify
it under the terms of the Lesser GNU General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

OSSIE Core Framework is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with OSSIE Core Framework; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

****************************************************************************/

#ifndef COMPLEXSHORT_P_H
#define COMPLEXSHORT_P_H

#include <string>
#include <vector>

#include <standardinterfaces/complexShort.h>

namespace complexShort {
  class providesPort;
}

namespace standardInterfaces_i {
  class complexShort_p {
    friend class complexShort::providesPort;

  public:
    complexShort_p(const char* portName, unsigned int bufLen = 5);
    complexShort_p(const char* portName, const char* domainName, unsigned int bufLen = 5);
    ~complexShort_p();

    CORBA::Object_ptr getPort(const char* portName);

    void getData(PortTypes::ShortSequence* &I, PortTypes::ShortSequence* &Q);
    void bufferEmptied();

  private:
    complexShort_p();
    complexShort_p(const complexShort_p &);

    std::string portName;

    // Provides port
    complexShort::providesPort *data_servant;
    standardInterfaces::complexShort_var data_servant_var;

    // Buffer storage
    unsigned int bufferLength;
    unsigned int rdPtr;
    unsigned int wrPtr;
    std::vector <PortTypes::ShortSequence> I_buf;
    std::vector <PortTypes::ShortSequence> Q_buf;
 
    // Semaphores for synchronization
    omni_semaphore *data_ready;  // Ready to process data
    omni_semaphore *ready_for_input; // Ready to receive more data

 };

}

namespace complexShort {

  class providesPort : public POA_standardInterfaces::complexShort {
  public:
    providesPort(standardInterfaces_i::complexShort_p* _base);
    ~providesPort();

    void pushPacket(const PortTypes::ShortSequence &I, const PortTypes::ShortSequence &Q);

  private:
    standardInterfaces_i::complexShort_p* base;
  };
}


#endif
