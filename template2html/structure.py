__doc__ = '''
Created on Feb 8, 2015

@author: derigible
'''

from collections import OrderedDict
from utils import lazy_property

class Template(object):
    '''
    This is the structure for a template. Templates are lazy, meaning they are not really created until evaluated. Once
    evaluated, the Template becomes immutable.
    '''
    path = None
    dependency = None
    template = None
    

    def __init__(self, params):
        '''
        Constructor
        '''
    @lazy_property
    def sections(self):    
        '''
        Upon evaluation will create the sections attribute, which is an OrderedDict of the sections found in the template.
        It will then replace itself with the new ordereddict and all subsequent calls to this property will return that dict.
        '''
        return self._evaluate_sections()
    
    def _evaluate_sections(self):
        '''
        Evaluates the template attribute and creates a section object. It then deletes the template attribute, thus
        ensuring that Template becomes an immutable object. Calling this method after sections has been evaluated will
        do nothing.
        '''
        if hasattr(self, "template"):
            pass
        else:
            return
        