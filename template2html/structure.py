__doc__ = '''
Created on Feb 8, 2015

@author: derigible
'''

from collections import OrderedDict
from utils import lazy_property

class Template(object):
    '''
    This is the structure for a template. Templates are lazy, meaning they are not really created until evaluated. Once
    evaluated, the Template becomes immutable. If there is an extends in the template, than the dependency is also evaluated.
    '''
    html = None
    dependency = None
    template = None
    path = None
    

    def __init__(self, html, path):
        '''
        The constructor for the template object. Recieves a string of html and the path to the directory for the template.
        
        @param html: a string that represents the template in raw form
        @param path: the path to the directory the template is found
        '''
        self.html = html
        self.path = path
        
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
        