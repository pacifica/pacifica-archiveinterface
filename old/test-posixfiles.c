/********************************************************************
 * \brief Test harness for the posixfiles method.
 *
 * This is the test harness for the posixfiles method. This is using
 * the glib2 test framework 
 * (https://developer.gnome.org/glib/stable/glib-Testing.html) and
 * integrated with automake using `make check`.
 *******************************************************************/
#include <glib.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "myemslarchive.h"

/**
 * \brief Fake test fixture struct.
 *
 * The glib2 testing infrastructure requires this test figure struct
 * for passing intermediate state between tests. As posixfiles is
 * has no state we have a basic struct with just an integer.
 */
typedef struct {
  int test;
  int fd;
  int id;
} MyEMSLTestFixture;

/**
 * \brief Constructor for test fixture.
 *
 * Set the internal state of the test fixture.
 */
static void myemsl_test_fixture_set_up_putfile (MyEMSLTestFixture *fixture,
                            gconstpointer user_data)
{
  setenv ("POSIXFILES_PREFIX_PATH", "/home/chrisExamples", 1);
  fixture->fd = open("fwritetest.txt", O_RDWR | O_CREAT, 777);
  fixture->id = 1;
  fixture->test = 0;
}

/**
 * \brief Destructor for test fixture.
 *
 * Nothing to destroy just return.
 */
static void myemsl_test_fixture_tear_down_putfile (MyEMSLTestFixture *fixture,
                               gconstpointer user_data)
{
  remove ("fwritetest.txt");
  return;
}

/**
 * \brief Test to verify functionality of posixfiles
 *
 * This just checks a random value to see that it works.
 */
static void test_posixfileput_basic (MyEMSLTestFixture *fixture,
                                    gconstpointer user_data)
{
  int test = posix_put_file(fixture->fd, fixture->id);
  g_assert_cmpint (test, ==, 0); //since no bytes to write
}



/**
 * \brief Main method.
 *
 * Setup glib testing framework and create the tests.
 */
int main(int argc, char * argv[])
{
  setlocale (LC_ALL, "");

  g_test_init (&argc, &argv, NULL);
  g_test_bug_base ("http://bugzilla.emsl.pnl.gov/show_bug.cgi?id=");

  // Define the tests.
  g_test_add ("/myemsl/basictest", MyEMSLTestFixture, NULL,
              myemsl_test_fixture_set_up_putfile, test_posixfileput_basic,
              myemsl_test_fixture_tear_down_putfile);
  
  return g_test_run ();
}
