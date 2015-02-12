__doc__ = '''
Created on Feb 8, 2015

@author: derigible

The loader module is used to find and load templates. It is also responsible for dictating the inheritance tree
for each template.
'''

templates = dict()
 
def load_template(path):
    '''
    Attempts to load the template and create a Template class instance. It will then add it to the _templates
    dictionary of this Loader. The templates key is the absolute path to the template. If this path has already been
    parsed will return that template object.
    
    @param path the path to the template file
    
    @return a Template class instance
    '''
    from templater.structure import Template
    if path in templates:
        return templates[path]
    with open(path, 'r') as f:
        template = Template(f.read(), path)
        templates[path] = template
        return template

def get_template(key):
    '''
    Returns the Template specified by the key passed in.
    
    @param key the key to the template file
    
    @return the template associated with the key
    
    @raise KeyError: When the specified key is not found.
    '''
    return templates[key]

def add_template(template):
    '''
    Add a template to the loader dictionary. If already added, will raise a key error. In theory this shouldn't ever
    have to raise a KeyError, but it is there to prevent it from wiping out an already created template.
    
    @param template the template to add
    @raise KeyError: template is already loaded
    '''
    if template.path in templates:
        raise KeyError("Template exists with current path already.")
    templates[template.path] = template
    
if __name__ == '__main__':
    import os
    import templater.testdata as testdata
    test_dir = __test_data_dir__ = testdata.__path__[0]
    working_templates = os.path.join(test_dir, "templates")
    nonworking_templates = os.path.join(test_dir, "badtemplates")
    l = load_template(os.path.join(nonworking_templates, 'template_test_single_section.html'))