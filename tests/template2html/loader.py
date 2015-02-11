'''
Created on Feb 8, 2015

@author: derigible
'''
import os
from tests.base_test import BaseTest as base
from templater import testdata
import templater.discovery
from templater.structure import Template
from templater.parser import approved_block_types

class TemplaterTest(base):
    '''
    Tests the functionality of the templater module.
    '''
    test_dir = __test_data_dir__ = testdata.__path__[0]
    working_templates = os.path.join(test_dir, "templates")
    nonworking_templates = os.path.join(test_dir, "badtemplates")
    allowed_additional_words = approved_block_types
    not_allowed_additional_words = ("the", "keep", "nested", "inhert", "extend", "extends")
    header = '''<meta charset="ISO-8859-1">
        <title>Wilkins</title>
        <link href="https://edge.fscdn.org/assets/docs/fs_logo_favicon.ico" rel="icon" type="image/x-icon" />
        
<!--         <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap.min.css" rel="stylesheet" media="screen"> -->
        <link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
<!--         <link href='https://edge.fscdn.org/assets/css/responsive-166fbb8fd4a3f5207a500bdf6c2d9186.css' rel='stylesheet' media='screen'>  -->
        <link href='/static/css/responsive-166fbb8fd4a3f5207a500bdf6c2d9186.css' rel='stylesheet' media='screen'> 
<!--         <link href='https://edge.fscdn.org/assets/css/layout/theme-engage-8e8aed919ce18a2f4b2a470bfc58b928.css' rel='stylesheet' media='screen'> -->
        <link href='/static/css/theme-engage-8e8aed919ce18a2f4b2a470bfc58b928.css' rel='stylesheet' media='screen'>
        <style type="text/css">    
            #global-engage-header !css padding-top: 25px;}
            h1 !css
                padding-top: .5em;
                padding-bottom: 0;
                margin-bottom: 0;
            }
            h2 !css
                font-size: 1.5em;
                padding-bottom: 0;
                margin-bottom: 0;
            }
        </style>'''
        
#     def test_template_load(self):
#         for f in os.listdir(path=self.working_templates):
#             with self.subTest(f=os.path.join(self.working_templates,f)):
#                 template = loader.load_template(f)
#                 self.assertIs(template, Template)
#                 self.assertEquals(loader.get_template(f), template)
#                  
#     def test_template_load_error(self):
#         for f in os.listdir(path=self.nonworking_templates):
#             with self.subTest(f=os.path.join(self.nonworking_templates,f)):
#                 with self.assertRaises(ImportError):
#                     loader.load_template(f)
    
    