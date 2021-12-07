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

#ifdef HAVE_SYS_TYPES_H
#include <sys/types.h>
#endif
#ifdef HAVE_SYS_STAT_H
#include <sys/stat.h>
#endif
#include <fcntl.h>

#ifdef HAVE_STRING_H
#include <string.h>
#endif
#ifdef HAVE_DIRENT_H
#include <dirent.h>
#endif
#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

#include <iostream>
#include <string>
#include <stdio.h>

#include "ossie/FileSystem_impl.h"


FileSystem_impl::FileSystem_impl ()
{
    root = new char[MAX_CWD_LEN];
    root = getcwd (root, MAX_CWD_LEN);

    init ();
}


FileSystem_impl::FileSystem_impl (char *_root)
{
    root = new char[MAX_CWD_LEN];
    root = getcwd (root, MAX_CWD_LEN);

    if (_root != NULL)
    {
        if (_root[0] != ROOT_DIR)
            root = strcat (this->root, ROOT_DIR_STR);
        root = strcat (this->root, _root);
    }
    init ();
}


FileSystem_impl::FileSystem_impl (const FileSystem_impl & _fsi)
{
    this->root = new char[strlen (_fsi.root) + 1];
    strcpy (this->root, _fsi.root);
    init ();
};

void
FileSystem_impl::init ()
{

};

FileSystem_impl FileSystem_impl::operator= (FileSystem_impl _fsi)
{
    this->root = new char[strlen (_fsi.root) + 1];
    strcpy (this->root, _fsi.root);
    return *this;
};

FileSystem_impl::~FileSystem_impl ()
{
    delete root;
    root = NULL;
};

void
FileSystem_impl::remove (const char *fileName)
throw (CORBA::SystemException, CF::FileException, CF::InvalidFileName)
{
    if (!this->checkValidFileName (fileName))
        throw (CF::
            InvalidFileName (CF::CFEINVAL,
            "[FileSystem_impl::remove] Invalid file name ... error removing file from file system"));

    char *fname = this->appendFileName (root, fileName);

    int check = unlink (fname);

    if (check != 0)
        throw (CF::
            FileException (CF::CFEEXIST,
            "[FileSystem_impl::remove] Error removing file from file system"));

    delete fname;
    fname = NULL;
};

void
FileSystem_impl::copy (const char *sourceFileName,
const char *destinationFileName)
throw (CORBA::SystemException, CF::InvalidFileName, CF::FileException)
{
    CF::File_var fileSource = this->open (sourceFileName, true);

    CORBA::ULong len = fileSource->sizeOf ();

    if (len == 0)
    {
        fileSource->close ();
        CORBA::Boolean check = exists (destinationFileName);
        if (!check)
            throw CF::FileException ();
    }
    else
    {
        CF::File_var fileDestin = this->open (destinationFileName, false);

        CF::OctetSequence_var data;

        fileSource->read (data, len);
        fileDestin->write (data);

        fileSource->close ();
        fileDestin->close ();
    }
};

CORBA::Boolean FileSystem_impl::exists (const char *fileName)
throw (CORBA::SystemException, CF::InvalidFileName)
{
    return true; ///\todo Fix FileSystem::exists

    bool _validFileName = this->checkValidFileName (fileName);
    if (_validFileName == false)
        throw
            CF::InvalidFileName (CF::CFEINVAL,
            "[FileSystem_impl::exists] Invalid file name");

    CF::FileSystem::FileInformationSequence_var _fis = list (fileName);

    if (_fis->length() == 0)
        return false;

    char *relpath; /// \todo appendFileName needs mm re-thinking
    for (unsigned int i = 0; i < _fis->length (); i++) {
	relpath = appendFileName (root, _fis[i].name);
	if (strstr (relpath, fileName) != NULL)
	    {
		delete []relpath;
		return true;
	    }
	delete []relpath;    
    }
    return false;
}


/// \todo: modify to search the pattern as a regular expression //
/// \todo Check back and see if this function leaks memory
CF::FileSystem::FileInformationSequence*
FileSystem_impl::list (const char *pattern) throw (CORBA::SystemException,
CF::FileException,
CF::InvalidFileName)
{
    CF::FileSystem::FileInformationSequence_var result = listDir (root, pattern);
    // Chop the base path of the returned file names
    for (unsigned int i=0; i < result->length(); i++) {
	std::string s(result[i].name);
	s.erase(0,strlen(root));
	result[i].name = CORBA::string_dup(s.c_str());
    }
    return result._retn();
}


CF::File_ptr FileSystem_impl::create (const char *fileName) throw (CORBA::
SystemException,
CF::
InvalidFileName,
CF::
FileException)
{
    bool _validFileName = this->checkValidFileName (fileName);
    if (_validFileName == false)
        throw
            CF::InvalidFileName (CF::CFEINVAL,
            "[FileSystem_impl::create] Invalid file name ... failed to create file\n");

/* designate hard-coded security permissions, may need something else here */
    
    int fp = creat (fileName, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);

    if (fp >= 0)
    {
        File_impl *
            myimplptr =
            new File_impl (this->appendFileName (this->root, fileName), fp);
        return myimplptr->_this ();
    }
    else
        throw CF::FileException (CF::CFEMFILE,
            "[FileSystem_impl::create] Failed to create file\n");

    return CF::File::_nil ();
}


CF::File_ptr FileSystem_impl::open (const char *fileName,
CORBA::Boolean read_Only) throw (CORBA::
SystemException,
CF::
InvalidFileName,
CF::
FileException)
{
    bool _validFileName = this->checkValidFileName (fileName);

    if (_validFileName == false)
        throw
            CF::InvalidFileName (CF::CFEINVAL,
            "[FileSystem_impl::open] Invalid file name ... failed to open file\n");

    int
        oFlag;

    if (read_Only)
        oFlag = O_RDONLY;
    else
        oFlag = O_WRONLY;

    int fp = ::open (fileName, oFlag);

    CF::File_ptr file = NULL;

    if (fp >= 0)
    {
        File_impl *
            myimplptr = new File_impl (fileName, fp);
        file = myimplptr->_this ();
    }
    else
        throw CF::FileException (CF::CFEEXIST,
            "[FileSystem_impl::open] Failed to open file\n");

    return file;
}


void
FileSystem_impl::mkdir (const char *directoryName)
throw (CORBA::SystemException, CF::FileException, CF::InvalidFileName)
{
    bool _validFileName = this->checkValidFileName (directoryName);

    if (_validFileName == false)
        throw CF::InvalidFileName (CF::CFEINVAL,
            "[FileSystem_impl::mkdir] Invalid file name\n");

    char *dname = this->appendFileName (this->root, directoryName);

	int check = ::mkdir (dname, 0755);

    delete dname;
    dname = NULL;

    if (check != 0)
        throw CF::FileException (CF::CFENFILE,
            "[FileSystem_impl::mkdir] Failed to make new directory\n");
}


void
FileSystem_impl::rmdir (const char *directoryName)
throw (CORBA::SystemException, CF::FileException, CF::InvalidFileName)
{
    bool _validFileName = this->checkValidFileName (directoryName);

    if (_validFileName == false)
        throw CF::InvalidFileName (CF::CFEINVAL,
            "[FileSystem_impl::rmdir] Invalid file name\n");

    char *dname = this->appendFileName (this->root, directoryName);

    int check = unlink (dname);

    delete dname;
    dname = NULL;

    if (check != 0)
        throw CF::FileException (CF::CFENFILE,
            "[FileSystem_impl::rmdir] Failed to remove directory\n");
}


void
FileSystem_impl::query (CF::Properties & fileSysProperties)
throw (CORBA::SystemException, CF::FileSystem::UnknownFileSystemProperties)
{
    bool check;

    for (unsigned int i = 0; i < fileSysProperties.length (); i++)
    {
        check = false;
        if (strcmp (fileSysProperties[i].id, CF::FileSystem::SIZE) == 0)
        {
            struct stat fileStat;
            stat (root, &fileStat);
//	    fileSysProperties[i].value <<= fileStat.st_size;  /// \bug FIXME
            check = true;
        }
        if (strcmp (fileSysProperties[i].id,
            CF::FileSystem::AVAILABLE_SIZE) == 0)
        {
//to complete
        }
        if (!check)
            throw CF::FileSystem::UnknownFileSystemProperties ();
    }
}


bool FileSystem_impl::checkValidFileName (const char *_fileName)
{
    int
        len = strlen (_fileName);

/// \bug implement a better file check bugzilla #27

    if (len < 1)
        return false;
    return true;
}


char *
FileSystem_impl::appendFileName (const char *_firstPart, const char *_secPart)
{
    int len = strlen (_firstPart) + strlen (_secPart) + 2;

    char *fname = new char[len];

    fname = strcpy (fname, _firstPart);

    fname = strcat (fname, ROOT_DIR_STR);

    fname = strcat (fname, _secPart);

    return fname;
}


CF::FileSystem::FileInformationSequence* FileSystem_impl::listDir (const char *_root, const char *_pattern)
{

    CF::FileSystem::FileInformationSequence_var result = new CF::FileSystem::FileInformationSequence(10);

    if (_root == NULL)
        return result._retn();

    CF::Properties prop;
    prop.length(3);

    DIR *dir;
    if (!(dir = opendir (_root))) {
	std::cout << "Bad directory name : " << _root << std::endl;
	return result._retn();
    }

    struct dirent *dp;
    int idx=0; //Index into return sequence

    while ((dp = readdir (dir)) != NULL) {
        if (dp->d_name[0] == '.') // Don't search hidden directories or . or ..
	    continue;

	struct stat fileStats;

        if (!checkValidFileName (dp->d_name))
            throw CF::InvalidFileName ();

	std::string full_name(_root);
	full_name += "/";
	full_name += dp->d_name;

/// \todo implement regex pattern matching
	int match = 0;
        if (_pattern == NULL)
	    match = 1;
        else if (strstr (dp->d_name, _pattern))
	    match = 1;

	if (match) {
	    match = 0;
	    result->length(idx+1);
            result[idx].name = CORBA::string_dup (full_name.c_str());
	    
	    if (stat (full_name.c_str(), &fileStats) < 0) {
		perror("Error stating file 1");
		std::cout << "Filename was : " << dp->d_name << std::endl;
	    }

#ifdef HAVE_UNISTD_H
            if (S_ISDIR(fileStats.st_mode))
#endif
		result[idx].kind = CF::FileSystem::DIRECTORY;
            else
                result[idx].kind = CF::FileSystem::PLAIN;

	    result[idx].size = fileStats.st_size;

            prop[0].id = CORBA::string_dup (CF::FileSystem::CREATED_TIME_ID);
            prop[0].value <<= fileStats.st_ctime;

            prop[1].id = CORBA::string_dup (CF::FileSystem::MODIFIED_TIME_ID);
            prop[1].value <<= fileStats.st_mtime;

            prop[2].id =
                CORBA::string_dup (CF::FileSystem::LAST_ACCESS_TIME_ID);
            prop[2].value <<= fileStats.st_atime;

            result[idx].fileProperties = prop;
	    ++idx;
        }


	if (stat (full_name.c_str(), &fileStats) < 0) {
	    perror("Error stating file 2");
	    std::cout << "Filename was : " << dp->d_name << std::endl;
	}
#ifdef HAVE_UNISTD_H
	if (S_ISDIR(fileStats.st_mode)) {
#endif
	    CF::FileSystem::FileInformationSequence_var dir_result = listDir (full_name.c_str(), _pattern);

	    idx = result->length();
	    result->length(result->length() + dir_result->length());
	    for (unsigned int j=0; j<dir_result->length(); j++, idx++) {
		result[idx].name = dir_result[j].name;
		result[idx].kind = dir_result[j].kind;
		result[idx].size = dir_result[j].size;
		result[idx].fileProperties = dir_result[j].fileProperties;
	    }

	}
	    
    }

    closedir (dir);

    return result._retn();
}
