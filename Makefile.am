EXTRA_DIST = COPYING

lib_LTLIBRARIES = libmyemslarchive.la
libmyemslarchive_la_SOURCES = id2filename.c
libmyemslarchive_la_LDFLAGS = $(LIBHPSS_LIBS)
libmyemslarchive_la_CFLAGS = $(LIBHPSS_CFLAGS)

check_PROGRAMS = test

test_SOURCES = libmyemslarchive.la test.c
