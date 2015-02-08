'''
Created on Feb 8, 2015

@author: derigible
'''
from argparse import ArgumentParser
import os, sys

#taken from django unit tests as an example, need to modify

if __name__ == "__main__":
    parser = ArgumentParser(description="Run the Django test suite.")
    parser.add_argument('modules', nargs='*', metavar='module',
        help='Optional path(s) to test modules; e.g. "i18n" or '
             '"i18n.tests.TranslationTests.test_lazy_objects".')
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
    parser.add_argument(
        '--noinput', action='store_false', dest='interactive', default=True,
        help='Tells Django to NOT prompt the user for input of any kind.')
    parser.add_argument(
        '--failfast', action='store_true', dest='failfast', default=False,
        help='Tells Django to stop running the test suite after first failed '
             'test.')
    parser.add_argument(
        '-k', '--keepdb', action='store_true', dest='keepdb', default=False,
        help='Tells Django to preserve the test database between runs.')
    parser.add_argument(
        '--settings',
        help='Python path to settings module, e.g. "myproject.settings". If '
             'this isn\'t provided, either the DJANGO_SETTINGS_MODULE '
             'environment variable or "test_sqlite" will be used.')
    parser.add_argument('--bisect',
        help='Bisect the test suite to discover a test that causes a test '
             'failure when combined with the named test.')
    parser.add_argument('--pair',
        help='Run the test suite in pairs with the named test to find problem '
             'pairs.')
    parser.add_argument('--reverse', action='store_true', default=False,
        help='Sort test suites and test cases in opposite order to debug '
             'test side effects not apparent with normal execution lineup.')
    parser.add_argument('--liveserver',
        help='Overrides the default address where the live server (used with '
             'LiveServerTestCase) is expected to run from. The default value '
             'is localhost:8081.')
    parser.add_argument(
        '--selenium', action='store_true', dest='selenium', default=False,
        help='Run the Selenium tests as well (if Selenium is installed)')
    parser.add_argument(
        '--debug-sql', action='store_true', dest='debug_sql', default=False,
        help='Turn on the SQL query logger within tests')
    options = parser.parse_args()

    # mock is a required dependency
    try:
        from django.test import mock  # NOQA
    except ImportError:
        print(
            "Please install test dependencies first: \n"
            "$ pip install -r requirements/py%s.txt" % sys.version_info.major
        )
        sys.exit(1)

    # Allow including a trailing slash on app_labels for tab completion convenience
    options.modules = [os.path.normpath(labels) for labels in options.modules]

    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    else:
        if "DJANGO_SETTINGS_MODULE" not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'test_sqlite'
        options.settings = os.environ['DJANGO_SETTINGS_MODULE']

    if options.liveserver is not None:
        os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options.liveserver

    if options.selenium:
        os.environ['DJANGO_SELENIUM_TESTS'] = '1'
