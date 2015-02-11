__doc__ = '''
Register all module tests here. This will then be used to run the tests.

To run all tests, use 

tester.py -r

Registering tests is as follows:

If not inside the builder folder, then the name must be the dotted path to the
module.

EXAMPLE:

TESTS = ["templater", "pythonpath.to.module"]

You can also register tests in the build_project.py file under the TESTS list.
'''

from versioner import get_version


VERSION = (0, 0, 0, 'alpha', 0)

__version__ = get_version(VERSION)

TESTS = ["templater"]

from build_project import TESTS as additional_tests

TESTS += additional_tests