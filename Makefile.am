include $(srcdir)/doxygen.am

EXTRA_DIST = COPYING

ACLOCAL_AMFLAGS = -I m4

lib_LTLIBRARIES = libmyemslarchive.la
libmyemslarchive_la_SOURCES = id2filename.c posixfiles.c
libmyemslarchive_la_LDFLAGS = $(LIBHPSS_LIBS)
libmyemslarchive_la_CFLAGS = $(LIBHPSS_CFLAGS)

check_PROGRAMS = test-id2filename test-posixfiles
TESTS = $(check_PROGRAMS)

test_id2filename_SOURCES = test-id2filename.c
test_id2filename_LDADD = libmyemslarchive.la
test_id2filename_CFLAGS = $(GLIB_CFLAGS)
test_id2filename_LDFLAGS = $(GLIB_LIBS)
test_posixfiles_SOURCES = test-posixfiles.c
test_posixfiles_LDADD = libmyemslarchive.la
test_posixfiles_CFLAGS = $(GLIB_CFLAGS)
test_posixfiles_LDFLAGS = $(GLIB_LIBS)
