/********************************************************************
 * \brief Test harness for the id2filename method.
 *
 * This is the test harness for the id2filename method. This is using
 * the glib2 test framework 
 * (https://developer.gnome.org/glib/stable/glib-Testing.html) and
 * integrated with automake using `make check`.
 *******************************************************************/
#include <glib.h>
#include <locale.h>

#include "myemslarchive.h"

/**
 * \brief Fake test fixture struct.
 *
 * The glib2 testing infrastructure requires this test figure struct
 * for passing intermediate state between tests. As id2filename is
 * has no state we have a basic struct with just an integer.
 */
typedef struct {
  int test;
} MyEMSLTestFixture;

/**
 * \brief Constructor for test fixture.
 *
 * Set the internal state of the test fixture.
 */
static void myemsl_test_fixture_set_up (MyEMSLTestFixture *fixture,
                            gconstpointer user_data)
{
  fixture->test = 0;
}

/**
 * \brief Destructor for test fixture.
 *
 * Nothing to destroy just return.
 */
static void myemsl_test_fixture_tear_down (MyEMSLTestFixture *fixture,
                               gconstpointer user_data)
{
  return;
}

/**
 * \brief Test to verify functionality of id2filename.
 *
 * This just checks a random value to see that it works.
 */
static void test_id2filename_basic (MyEMSLTestFixture *fixture,
                                    gconstpointer user_data)
{
  char *test = id2filename(1234);
  g_assert_cmpstr (test, ==, "/d2/4d2");
  free(test);
}

/**
 * \brief Coverage tests for id2filename.
 *
 * Coverage tests make sure values around 0 work as expected. Also,
 * there is a requirement for paths to be generated without making
 * more than 32K directories in a directory. So 32K is also a 
 * coverage value to be checked.
 */
static void test_id2filename_coverage (MyEMSLTestFixture *fixture,
                                  gconstpointer user_data)
{
  char *test;
  test = id2filename(-1);
  g_assert_cmpstr(test, ==, "/ff/ff/ff/ffffffff");
  free(test);
  test = id2filename(0);
  g_assert_cmpstr(test, ==, "/file.0");
  free(test);
  test = id2filename(1);
  g_assert_cmpstr (test, ==, "/file.1");
  free(test);
  test = id2filename((32*1024)-1);
  g_assert_cmpstr(test, ==, "/ff/7fff");
  free(test);
  test = id2filename((32*1024));
  g_assert_cmpstr(test, ==, "/00/8000");
  free(test);
  test = id2filename((32*1024)+1);
  g_assert_cmpstr (test, ==, "/01/8001");
  free(test);
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
              myemsl_test_fixture_set_up, test_id2filename_basic,
              myemsl_test_fixture_tear_down);
  g_test_add ("/myemsl/coveragetest", MyEMSLTestFixture, "some-user-data",
              myemsl_test_fixture_set_up, test_id2filename_coverage,
              myemsl_test_fixture_tear_down);

  return g_test_run ();
}
