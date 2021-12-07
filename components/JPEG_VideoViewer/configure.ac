AC_INIT(JPEG_VideoViewer, 0.6.2)
AM_INIT_AUTOMAKE

AC_PREFIX_DEFAULT("/sdr")

AC_PROG_CXX
AC_PROG_INSTALL
AC_PROG_MAKE_SET

AC_HEADER_SYS_WAIT

AC_FUNC_FORK

AC_LANG_PUSH([C++])

AC_CHECK_LIB([omniORB4], [main], [], [AC_MSG_ERROR([cannot find omniORBi4 library])])
AC_CHECK_LIB([omniDynamic4], [main], [], [AC_MSG_ERROR([cannot find omniDynamic4 library])])
AC_CHECK_HEADERS([omniORB4/CORBA.h], [], [AC_MSG_ERROR([cannot find omniORB4 header files])])
AC_CHECK_LIB([SDL],[main], [], [AC_MSG_ERROR([cannot find SDL library])])
AC_CHECK_HEADERS([SDL/SDL.h], [], [AC_MSG_ERROR([cannot find SDL header files])])
AC_CHECK_HEADERS([SDL/SDL_thread.h], [], [AC_MSG_ERROR([cannot find SDL header files])])
AC_CHECK_HEADERS([SDL/SDL_audio.h], [], [AC_MSG_ERROR([cannot find SDL header files])])
AC_CHECK_HEADERS([SDL/SDL_timer.h], [], [AC_MSG_ERROR([cannot find SDL header files])])

AC_LANG_POP

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig"
PKG_CHECK_MODULES(OSSIE, ossie >= 0.6.2,,exit)
CXXFLAGS="$CXXFLAGS $OSSIE_CFLAGS"
IDL_FLAGS="$OSSIE_CFLAGS"
AC_SUBST(IDL_FLAGS)

PKG_CHECK_MODULES(SI, standardInterfaces >= 0.6.2,,exit)
SI_PATH=`pkg-config --variable=includedir standardInterfaces`
AC_SUBST(SI_PATH)

LIBS="$LIBS $OSSIE_LIBS $SI_LIBS"

AC_CONFIG_FILES(Makefile)

AC_OUTPUT
