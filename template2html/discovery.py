__doc__ = '''
Created on Feb 8, 2015

@author: derigible

The discovery module is used to find and load templates. It is also responsible for dictating the inheritance tree
for each template.
'''

from .structure import Template

class Loader(object):
    '''
    Discovers the templates files that will create the static html files.
    '''
    
    __templates__ = dict()

    def __init__(self, params):
        '''
        Constructor
        '''
     
    def load_template(self, path):
        '''
        Attempts to load the template and create a Template class instance. It will then add it to the __templates__
        dictionary of this Loader. The templates key is the absolute path to the template.
        
        @param path the path to the template file
        
        @return a Template class instance
        '''
        raise NotImplementedError()   
    
    def get_template(self, template):
        '''
        Returns the Template
        '''