#include <glib.h>
#include <locale.h>

typedef struct {
  int test;
} MyEMSLTestFixture;

#include "myemslarchive.h"

static void myemsl_test_fixture_set_up (MyEMSLTestFixture *fixture,
                            gconstpointer user_data)
{
  fixture->test = 0;
}

static void myemsl_test_fixture_tear_down (MyEMSLTestFixture *fixture,
                               gconstpointer user_data)
{
  return;
}


static void test_id2filename_basic (MyEMSLTestFixture *fixture,
                                    gconstpointer user_data)
{
  g_assert_cmpstr (id2filename(1234), ==, "/d2/4d2");
}

static void test_id2filename_coverage (MyEMSLTestFixture *fixture,
                                  gconstpointer user_data)
{
  g_assert_cmpstr (id2filename(-1), ==, "/ff/ff/ff/ffffffff");
  g_assert_cmpstr (id2filename(0), ==, "/file.0");
  g_assert_cmpstr (id2filename(1), ==, "/file.1");
  g_assert_cmpstr (id2filename((32*1024)-1), ==, "/ff/7fff");
  g_assert_cmpstr (id2filename((32*1024)), ==, "/00/8000");
  g_assert_cmpstr (id2filename((32*1024)+1), ==, "/01/8001");
}


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
