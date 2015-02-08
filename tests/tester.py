'''
Created on Feb 8, 2015

@author: derigible
'''
from argparse import ArgumentParser
from . import TESTS

if __name__ == '__main__':
    parser = ArgumentParser(description="Run the Builder test suite.")
    parser.add_argument(
        '-r', '--run', action='store_true', dest='run_tests', default=False,
        help='Tells tester to run the tests for builder.')
    
    #write test gather and execution code later