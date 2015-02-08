'''
Created on Feb 8, 2015

@author: derigible
'''
import os
from .base_test import BaseTest as base
from template2html import testdata
from template2html.discovery import Loader as loader
from template2html.structure import Template

class Template2HtmlTest(base):
    '''
    Tests the functionality of the template2html module.
    '''
    test_dir = __test_data_dir__ = testdata.__file__
    working_templates = os.path.join(test_dir, "templates")
    nonworking_templates = os.path.join(test_dir, "badtemplates")
    
    def test_template_creation(self):
        path = self._get_random_file(self.working_templates)
        template = Template()
        self.assertEqual(template.path, path)
        self.assertNotEqual(template.sections, None)
        
    def test_template_section_creation(self):    
    
    def test_template_load(self):
        for f in os.listdir(path=self.working_templates):
            with self.subTest(f=f):
                template = loader.load_template(f)
                self.assertIs(template, Template)
                self.assertEquals(loader.get_template(f), template)
                
    def test_template_load_error(self):
        for f in os.listdir(path=self.nonworking_templates):
            with self.subTest(f=f):
                with self.assertRaises(ImportError):
                    loader.load_template(f)
    
    