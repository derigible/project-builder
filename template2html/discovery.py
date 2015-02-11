__doc__ = '''
Created on Feb 8, 2015

@author: derigible

The discovery module is used to find and load templates. It is also responsible for dictating the inheritance tree
for each template.
'''

class Loader(object):
    '''
    Discovers the templates files that will create the static html files.
    '''
    
    _templates = dict()

    def __init__(self, params):
        '''
        Constructor
        '''
     
    def load_template(self, path):
        '''
        Attempts to load the template and create a Template class instance. It will then add it to the _templates
        dictionary of this Loader. The templates key is the absolute path to the template.
        
        @param path the path to the template file
        
        @return a Template class instance
        '''
        raise NotImplementedError()   
    
    def get_template(self, key):
        '''
        Returns the Template specified by the key passed in.
        
        @param key the key to the template file
        
        @return the template associated with the key
        
        @raise KeyError: When the specified key is not found.
        '''
        return self._templates[key]
    
    def add_template(self, template):
        '''
        Add a template to the loader dictionary.
        
        @param template the template to add
        '''
        self._templates[template.path] = template