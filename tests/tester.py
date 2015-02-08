'''
Created on Feb 8, 2015

@author: derigible
'''
from argparse import ArgumentParser
from . import TESTS as tests
from unittest import TestLoader, TextTestRunner

if __name__ == '__main__':
    parser = ArgumentParser(description="Run the Builder test suite.")
    parser.add_argument(
        '-r', '--run', action='store_true', dest='run_tests', default=False,
        help='Tells tester to run the tests for builder.')
    
    
    args = parser.parse_args()
    #write test gather and execution code later
    if args.run_tests:
        loader = TestLoader()
        suite = loader.loadTestsFromNames(tests)
        suite.run(TextTestRunner())