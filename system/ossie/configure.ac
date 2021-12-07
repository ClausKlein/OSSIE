AC_INIT(ossie, 0.6.2)
AC_PREREQ(2.59)

AM_INIT_AUTOMAKE(nostdinc)

AC_PROG_CXX
AC_PROG_INSTALL
AC_PROG_MAKE_SET
AC_PROG_LIBTOOL
AC_CONFIG_MACRO_DIRS([m4])

AC_LANG_PUSH([C++])
AC_CHECK_LIB([xerces-c], [main], [], [AC_MSG_ERROR([cannot find xerces-c library.])])
AC_CHECK_HEADERS([xercesc/util/PlatformUtils.hpp], [], [AC_MSG_ERROR([cannot find xerces-c header file.])])

AC_CHECK_LIB([omniORB4], [main], [], [AC_MSG_ERROR([cannot find omniORB library])])
AC_CHECK_LIB([omnithread], [main], [], [AC_MSG_ERROR([cannot find omnithread library])])
AC_CHECK_HEADERS([omniORB4/CORBA.h], [], [AC_MSG_ERROR([cannot find omniORB4 header files])])
AC_CHECK_PROG([IDL], [omniidl], [AC_MSG_ERROR([cannot find omniidl program])])

AM_PATH_PYTHON([2.7])

AC_LANG_POP

AC_HEADER_SYS_WAIT
AC_CHECK_HEADERS(time.h)
AC_HEADER_DIRENT

AC_FUNC_FORK

if test "$ac_cv_func_fork_works" != yes; then
   AC_MSG_ERROR([working fork test failed. Try running /sbin/ldconfig.])
fi

AC_CONFIG_FILES(Makefile ossie.pc idl/Makefile idl/cpp/Makefile idl/python/Makefile parser/Makefile framework/Makefile include/Makefile include/ossie/Makefile)
AC_OUTPUT
