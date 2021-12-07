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
#include <sys/types.h>
#include <sys/stat.h>

#ifdef HAVE_UNISTD_H
	#include <unistd.h>
#endif

#include "ossie/File_impl.h"


  /// \todo the File class needs work
/// \todo use intialization

File_impl::File_impl (const char *_fileName, int _fileDescriptor)
{
    this->myfileName = new char[strlen (_fileName) + 1];
    strcpy (myfileName, _fileName);
    this->fileDescriptor = _fileDescriptor;
    this->myfilePointer = 0;
}


File_impl::~File_impl ()
{
    delete myfileName;
    myfileName = NULL;
}


void
File_impl::read (CF::OctetSequence_out data, CORBA::ULong length)
throw (CORBA::SystemException, CF::File::IOException)
{
    CORBA::Octet * buf = CF::OctetSequence::allocbuf (length);
    int check = ::read (fileDescriptor, buf, length);

    data = new CF::OctetSequence;
    data->length (length);

    if (check <= 0)
    {
        throw CF::File::IOException (CF::CFEIO,
            "[File_impl::read] Error reading from file\n");
    }
    else
    {
        for (CORBA::ULong i = 0; i < length; i++)
            data[i] = buf[i];
        myfilePointer = myfilePointer + check;

        delete[]buf;

        buf = NULL;
    }

}


void
File_impl::write (const CF::OctetSequence & data)
throw (CORBA::SystemException, CF::File::IOException)
{
    CORBA::ULong length = data.length ();
    char *buf = new char[length + 1];

    for (unsigned int i = 0; i < length; i++)
        buf[i] = data[i];
    buf[length] = '\0';

	int check = ::write (fileDescriptor, buf, length);

    if (check <= 0)
        throw (CF::File::
            IOException (CF::CFEIO,
            "[File_impl::write] Error writing to file\n"));

    myfilePointer = myfilePointer + check;

    delete[]buf;

    buf = NULL;

}


CORBA::ULong File_impl::sizeOf ()throw (CORBA::SystemException,
CF::FileException)
{
    struct stat st;

    int
        check = stat (this->myfileName, &st);

    if (check != 0)
        throw
            CF::FileException (CF::CFENFILE,
            "[File_impl::sizeof] Sizeof failed ... file does not exist\n");

    return st.st_size;
}


void
File_impl::close ()
throw (CORBA::SystemException, CF::FileException)
{
	int check = ::close (fileDescriptor);

    if (check != 0)
        throw CF::FileException (CF::CFENFILE,
            "[File_impl::close] Error closing file ... file does not exist\n");
}


void
File_impl::setFilePointer (CORBA::ULong _filePointer)
throw (CORBA::SystemException, CF::File::InvalidFilePointer,
CF::FileException)
{
    if (_filePointer > this->sizeOf ())
    {
        throw CF::File::InvalidFilePointer ();
    }
    else
    {
        int check = lseek (fileDescriptor, _filePointer, SEEK_SET);

        if (check == -1)
        {
            throw CF::FileException (CF::CFEIO,
                "[File_impl::setFilePointer] Invalid file pointer\n");
        }
        else
            this->myfilePointer = _filePointer;
    }
}
