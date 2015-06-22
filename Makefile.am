EXTRA_DIST = COPYING

ACLOCAL_AMFLAGS = -I m4

lib_LTLIBRARIES = libmyemslarchive.la
libmyemslarchive_la_SOURCES = id2filename.c
libmyemslarchive_la_LDFLAGS = $(LIBHPSS_LIBS)
libmyemslarchive_la_CFLAGS = $(LIBHPSS_CFLAGS)

check_PROGRAMS = test
TESTS = $(check_PROGRAMS)

test_SOURCES = test.c
test_LDADD = libmyemslarchive.la
test_CFLAGS = $(GLIB_CFLAGS)
test_LDFLAGS = $(GLIB_LIBS)
