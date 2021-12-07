
/****************************************************************************

Copyright 2008, Virginia Polytechnic Institute and State University

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

/* SCA */
#ifndef FILE_IMPL_H
#define FILE_IMPL_H

/* Include files */
#include "ossiecf.h"

#include <omniORB4/CORBA.h>

#include "cf.h"

class OSSIECF_API File_impl:public virtual
POA_CF::File
{
    public:File_impl (const char *_fileName, int _fileDescriptor);
    ~
        File_impl ();
    char *
        fileName ()
        throw (CORBA::SystemException)
    {
        return CORBA::string_dup(myfileName);
    }
    void
        read (CF::OctetSequence_out data, CORBA::ULong length)
        throw (CF::File::IOException, CORBA::SystemException);

    void
        write (const CF::OctetSequence & data)
        throw (CF::File::IOException, CORBA::SystemException);

    void
        close ()
        throw (CF::FileException, CORBA::SystemException);

    void
        setFilePointer (CORBA::ULong _filePointer)
        throw (CF::FileException,
        CF::File::InvalidFilePointer, CORBA::SystemException);
    CORBA::ULong filePointer ()throw (CORBA::SystemException)
    {
        return myfilePointer;
    };
    CORBA::ULong sizeOf ()throw (CF::FileException, CORBA::SystemException);

    private:
        char * myfileName;
        int fileDescriptor;
        CORBA::ULong myfilePointer;

 };                                                /* END CLASS DEFINITION File */
#endif                                            /* __FILE_IMPL__ */
