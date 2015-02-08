__doc__ = '''
Register all module tests here. This will then be used to run the tests.

To run all tests, use 

tester.py -r

Registering tests is as follows:

If not inside the builder folder, then add a 2-tuple to the tuple TESTS.

TESTS = ("template2html", ("othermodule", "/absolute/path/to/other/module")
'''

from versioner import get_version

VERSION = (0, 0, 0, 'alpha', 0)

__version__ = get_version(VERSION)

TESTS = ("template2html")