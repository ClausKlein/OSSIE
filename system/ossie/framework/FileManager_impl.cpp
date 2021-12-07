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

#include <iostream>

#include "ossie/cf.h"
#include "ossie/FileManager_impl.h"

    using namespace std;

FileManager_impl::FileManager_impl ():FileSystem_impl ()
{
    numMounts = 0;
    mount_table = new CF::FileManager::MountSequence(5);

    rootFileSys_serv = new FileSystem_impl ();
    rootFileSys = rootFileSys_serv->_this();

    mount ("/", rootFileSys);

}

FileManager_impl::~FileManager_impl()

{

}

void
FileManager_impl::mount (const char *mountPoint,
CF::FileSystem_ptr _fileSystem)
throw (CORBA::SystemException, CF::InvalidFileName,
CF::FileManager::InvalidFileSystem,
CF::FileManager::MountPointAlreadyExists)
{
    if (CORBA::is_nil (_fileSystem))
        throw CF::FileManager::InvalidFileSystem ();

    if (!checkValidFileName (mountPoint))
        throw CF::InvalidFileName ();

    CF::FileManager::MountType _mt;

    for (unsigned int i=0; i < mount_table->length(); i++) {
	if (strcmp(mountPoint, mount_table[i].mountPoint) == 0)
	    throw CF::FileManager::MountPointAlreadyExists ();
    }

    numMounts++;
    mount_table->length(numMounts);

    mount_table[numMounts-1].mountPoint = CORBA::string_dup(mountPoint);
    mount_table[numMounts-1].fs = _fileSystem;


    if (strcmp (mountPoint, "/test") == 0)
      cout <<  mountPoint << endl;
}


void
FileManager_impl::unmount (const char *mountPoint)
throw (CORBA::SystemException, CF::FileManager::NonExistentMount)
{
    for (unsigned int i = 0; i < mount_table->length(); i++)
    {
	///\todo Finish fixing code Look at bit in book for sequence element deletion
        if (strcmp (mount_table[i].mountPoint, mountPoint) == 0)
        {
            CF::FileManager::MountType _del = mount_table[i];
            _del.mountPoint = CORBA::string_dup ("");
            _del.fs = NULL;

            return;
        }
    }

    throw CF::FileManager::NonExistentMount ();
}


void
FileManager_impl::remove (const char *fileName)
throw (CORBA::SystemException, CF::FileException, CF::InvalidFileName)
{
    CF::FileManager::MountType _mt = getMountTypeByFile (fileName);

    if (_mt.fs->exists (fileName))
        _mt.fs->remove (fileName);
}


void
FileManager_impl::copy (const char *sourceFileName,
const char *destinationFileName)
throw (CORBA::SystemException, CF::InvalidFileName, CF::FileException)
{
    char *_mountSource = getRelName (sourceFileName);

    char *_mountDestination = getRelName (destinationFileName);

    CF::FileManager::MountType _mtSource = getMountType (_mountSource);

    if (!_mtSource.fs->exists (sourceFileName))
        throw CF::InvalidFileName ();

    if (strcmp (_mountSource, _mountDestination) == 0)
    {
        _mtSource.fs->copy (sourceFileName, destinationFileName);
        return;
    }

    CF::File_var _srcFile = _mtSource.fs->open (sourceFileName, true);

    CORBA::ULong _srcSz = _srcFile->sizeOf ();

    if (_srcSz == 0)
    {
        _srcFile->close ();
        throw CF::FileException ();
    }

    CF::FileManager::MountType _mtDestination =
        getMountType (_mountDestination);

    if (!_mtDestination.fs->exists (destinationFileName))
        _mtDestination.fs->create (destinationFileName);

    CF::File_var _destFile =
        _mtDestination.fs->open (destinationFileName, false);

    CF::OctetSequence_var data;

    _srcFile->read (data, _srcSz);

    _destFile->write (data);
}


CORBA::Boolean FileManager_impl::exists (const char *fileName)
throw (CORBA::SystemException, CF::InvalidFileName)
{
    for (unsigned int i = 0; i < mount_table->length(); i++)
    {
        if (mount_table[i].fs->exists (fileName))
            return true;
    }

    return false;
}


CF::FileSystem::FileInformationSequence *
FileManager_impl::list (const char *pattern) throw (CORBA::SystemException,
CF::FileException,
CF::InvalidFileName)
{

    int numFiles = 0;

    CF::FileSystem::FileInformationSequence_var result = new CF::FileSystem::FileInformationSequence(10);

    for (unsigned int i = 0; i < mount_table->length(); i++)
    {

        CF::FileSystem::FileInformationSequence_var _fis = mount_table[i].fs->list (pattern);

        if (_fis->length() > 0)
        {

	    result->length(result->length() + _fis->length());

            for (unsigned int j = 0; j < _fis->length (); j++) {
		string s(mount_table[i].mountPoint);
		s += _fis[j].name;
		result[numFiles].name = CORBA::string_dup(s.c_str());;

		result[numFiles].kind = _fis[j].kind;
                result[numFiles].size = _fis[j].size;
		result[numFiles].fileProperties = _fis[j].fileProperties;

		numFiles++;
            }

        }
    }
    return result._retn();
}


CF::File_ptr FileManager_impl::create (const char *fileName) throw (CORBA::
SystemException,
CF::
InvalidFileName,
CF::
FileException)
{
    char *
        _mountPoint = getRelName (fileName);

    try
    {
        CF::FileManager::MountType _mt = getMountType (_mountPoint);

        delete[]_mountPoint;
        _mountPoint = NULL;
        return _mt.fs->create (fileName);
    }
    catch (CF::FileManager::NonExistentMount & _nem)
    {
        delete[]_mountPoint;
        _mountPoint = NULL;
        throw _nem;
    }
}


CF::File_ptr FileManager_impl::open (const char *fileName,
CORBA::Boolean read_Only) throw (CORBA::
SystemException,
CF::
InvalidFileName,
CF::
FileException)
{
    try
    {
        CF::FileManager::MountType _mt = getMountType (getRelName (fileName));
        return _mt.fs->open (fileName, read_Only);
    }
    catch (CF::InvalidFileName & _ifn)
    {
        throw _ifn;
    }
}


void
FileManager_impl::mkdir (const char *directoryName)
throw (CORBA::SystemException, CF::FileException, CF::InvalidFileName)
{
    char *_mountPoint = getRelName (directoryName);

    try
    {
        CF::FileManager::MountType _mt = getMountType (_mountPoint);

        delete[]_mountPoint;
        _mountPoint = NULL;
        _mt.fs->mkdir (directoryName);
    } catch (CF::FileManager::NonExistentMount & _nem)
    {
        delete[]_mountPoint;
        _mountPoint = NULL;
        throw _nem;
    }
}


void
FileManager_impl::rmdir (const char *directoryName)
throw (CORBA::SystemException, CF::FileException, CF::InvalidFileName)
{
    char *_mountPoint = getRelName (directoryName);

    try
    {
        CF::FileManager::MountType _mt = getMountType (_mountPoint);

        delete[]_mountPoint;
        _mountPoint = NULL;
        _mt.fs->rmdir (directoryName);
    } catch (CF::FileManager::NonExistentMount & _nem)
    {
        delete[]_mountPoint;
        _mountPoint = NULL;
        throw _nem;
    }
}


void
FileManager_impl::query (CF::Properties & fileSysProperties)
throw (CORBA::SystemException, CF::FileSystem::UnknownFileSystemProperties)
{
    bool check;

    for (unsigned int i = 0; i < fileSysProperties.length (); i++)
    {
        check = false;

        if (strcmp (fileSysProperties[i].id, CF::FileSystem::SIZE) == 0)
        {
            CORBA::Long totalSize, temp;
            totalSize = 0;

            for (unsigned int j = 0; j < mount_table->length(); j++)
            {
                CF::DataType dt;
                dt.id = CORBA::string_dup ("SIZE");
                CF::Properties pr (2, 1, &dt, 0);

                mount_table[j].fs->query (pr);

                CF::DataType * _dt = pr.get_buffer ();

                for (unsigned int k = 0; k < pr.length (); k++)
                {
                    _dt->value >>= temp;
                    totalSize = totalSize + temp;
                    _dt++;
                }

                fileSysProperties[i].value >>= temp;
                fileSysProperties[i].value <<= totalSize + temp;

                check = true;
            }
        }

        if (strcmp (fileSysProperties[i].id,
            CF::FileSystem::AVAILABLE_SIZE) == 0)
        {
            CORBA::Long totalSize;
            totalSize = 0;

            for (unsigned int i = 0; i < mount_table->length(); i++)
            {
            }

            check = true;
        }

        if (!check)
            throw CF::FileSystem::UnknownFileSystemProperties ();

// TODO
// Add functionality to query ALL FileManager properties
    }
}


CF::FileManager::MountType& FileManager_impl::
getMountType (const char *_mountPoint)
{

    for (unsigned int i = 0; i < mount_table->length(); i++)
    {
        if (strcmp (mount_table[i].mountPoint, _mountPoint) == 0) {
            return mount_table[i];
	}
    }

    throw CF::FileManager::NonExistentMount ();
}


CF::FileManager::MountType & FileManager_impl::
getMountTypeByFile (const char *_fullPath)
{
    for (unsigned int i = 0; i < mount_table->length(); i++)
    {
        if (mount_table[i].fs->exists (_fullPath))
            return mount_table[i];
    }

    throw CF::InvalidFileName ();
}


char *
FileManager_impl::getRelName (const char *_inputName)
{
    const char *loc = strrchr (_inputName, ROOT_DIR);
    if (loc == NULL)
        throw CF::InvalidFileName ();

    int len = (*(loc) - *(_inputName));
    if (len == 0)
        len++;
    char *mountName = new char[len + 1];
    strncpy (mountName, _inputName, len);
    mountName[len] = '\0';
    return mountName;
}


CF::FileManager::MountSequence*
FileManager_impl::getMounts ()throw (CORBA::SystemException)
{
    return mount_table._retn();
}
