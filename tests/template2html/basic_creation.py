'''
Created on Feb 8, 2015

@author: derigible
'''
import os
from tests.base_test import BaseTest as base
from templater import testdata
from templater.structure import Template
from string import Template as stemp
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
    
    def test_template_creation(self):
        html = stemp('''<!DOCTYPE html>
<html>
    {% block header %}
    <head>
    $var
    </head>
    {% endblock header %}
    <body>
    </body>
</html>''').substitute(var = self.header)
        template = Template(html, self.working_templates)
        self.assertMultiLineEqual(template.html, html)
        
    def test_template_section_creation(self):
        html = stemp('''<!DOCTYPE html>
<html>
    {% block header %}
    <head>
    $var
    </head>
    {% endblock header %}
    <body>
    </body>
</html>''').substitute(var = self.header)
        template = Template(html, self.working_templates)
        self.assertEqual(3, len(template.sections))
        self.assertEqual(template.sections["header"], r"<head><meta charset=\"ISO-8859-1\"><title>Wilkins</title><link href=\"https://edge.fscdn.org/assets/docs/fs_logo_favicon.ico\" rel=\"icon\" type=\"image/x-icon\" /><!--<link href=\"http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap.min.css\" rel=\"stylesheet\" media=\"screen\">--><link href=\"/static/css/bootstrap.min.css\" rel=\"stylesheet\" media=\"screen\"><!--<link href='https://edge.fscdn.org/assets/css/responsive-166fbb8fd4a3f5207a500bdf6c2d9186.css' rel='stylesheet' media='screen'>--><link href='/static/css/responsive-166fbb8fd4a3f5207a500bdf6c2d9186.css' rel='stylesheet' media='screen'> <!--<link href='https://edge.fscdn.org/assets/css/layout/theme-engage-8e8aed919ce18a2f4b2a470bfc58b928.css' rel='stylesheet' media='screen'>--><link href='/static/css/theme-engage-8e8aed919ce18a2f4b2a470bfc58b928.css' rel='stylesheet' media='screen'><style type=\"text/css\">#global-engage-header{padding-top: 25px;}h1{padding-top:.5em;padding-bottom:0;margin-bottom:0;}h2{font-size:1.5em;padding-bottom:0;margin-bottom:0;}</style></head>")        
    
    def test_section_creation_maintains_order(self):
        html = stemp('''<!DOCTYPE html>
<html>
    {% block header %}
    <head>
    $var
    </head>
    {% endblock header %}
    {% block end %}
    {% endblock end %}
    <body>
    </body>
</html>''').substitute(var = self.header)
        template = Template(html, self.working_templates)
        self.assertEqual(4, len(template.sections))
        self.assertListEqual(['parent', 'header', 'end', 'foot'], list(template.sections.keys()))
        