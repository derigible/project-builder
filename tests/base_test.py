__doc__ = '''
Created on Feb 8, 2015

@author: derigible

This class is for common test case inheritance. This class will be built over time.
'''
import unittest, os, random


class BaseTest(unittest.TestCase):

    # Used to point the TestCase to the relevant testdata of the module.
    __test_data_dir__ = None
    
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def assertIsInstance(self, obj, cls):
        super(BaseTest, self).assertIsInstance(obj, cls,
            "Object {!r} is not equal to class {!r}.".format(obj, cls))
        
    def _get_random_file(self, path):
        '''
        Gets a random file from the directory defined in the path variable.
        '''
        return random.choice(os.listdir(path=path))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()