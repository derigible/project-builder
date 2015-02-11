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

class Template2HtmlTest(base):
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
            
    def test_endblock_has_additional_words_found_raises_error(self):         
        html = stemp('''<!DOCTYPE html>
<html>
    {% block header %}
    <head>
    $var
    </head>
    {% endblock header end %}
    <body>
    </body>
</html>''').substitute(var = self.header)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_startblock_additional_words_found_without_extension_raises_error(self):         
        html = stemp('''<!DOCTYPE html>
<html>
    {% block header $word %}
    <head>
    $var
    </head>
    {% endblock header end %}
    <body>
    </body>
</html>''')
        for word in self.allowed_additional_words:
            h = html.substitute(word = word, var = self.header)
            with self.subTest():
                template = Template(h, self.working_templates)
                with self.assertRaises(ImportError):
                    template.sections
            
    def test_startblock_additional_words_found_not_allowed_without_extension_raises_error(self):         
        html = stemp('''<!DOCTYPE html>
<html>
    {% block header $word%}
    <head>
    $var
    </head>
    {% endblock header end %}
    <body>
    </body>
</html>''')
        for word in self.not_allowed_additional_words:
            h = html.substitute(word = word, var = self.header)
            with self.subTest():
                template = Template(h, self.working_templates)
                with self.assertRaises(ImportError):
                    template.sections
                    
    def test_extends_found_twice_raises_error(self):         
        html = stemp('''{% extends $location/template_test_single_section.html %}
        {% extends $location/template_test_single_section.html %}
        ''').substitute(var = self.header)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
        
    def test_template_extension_from_remote_directory_not_found_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.nonworking_templates)
        self.assertCountEqual(3, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertListEqual(template.dependency, self.working_templates +"/template_test_single_section.html")
        
    def test_template_extension_from_local_directory_not_found_raises_error(self):
        html = '''
        {% extends template_test_single_section_.html %}
        '''
        h = html
        template = Template(h, self.working_templates)
        with self.assertRaises(ImportError):
            template.sections
                    
    def test_block_inheritance_block_not_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header inherits %}
        $newhtml
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates, newhtml = "<link rel='author' title='Test' href='#'>")
        template = Template(h, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_nested_block_edit_without_parent_block_defined_in_parent_raises_error(self):  
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block css %}
        {% endblock css %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        with self.assertRaises(KeyError):
            template.sections    
            
    def test_startblock_additional_words_found_not_allowed_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header $word %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        for word in self.not_allowed_additional_words:
            h = html.substitute(location = self.working_templates, word = word)
            with self.subTest():
                template = Template(h, self.working_templates)
                with self.assertRaises(SyntaxError):
                    template.sections
                    
#Making sure that the inherited blocks and adding blocks in inherited blocks still throws an error
    def test_in_childblock_endblock_without_startblock_found_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}

        {% endblock css %}
        {% endblock header %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_startblock_without_endblock_found_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}

        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_startblock_missing_first_modulo_found_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        { block css %}
        {% endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_startblock_missing_second_modulo_found_raises_error(self):  
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css }
        {% endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
    
    def test_in_childblock_startblock_block_spelled_wrong_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% blok css %}
        {% endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_startblock_missing_starting_brace_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        % block css %}
        {% endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_startblock_missing_ending_brace_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %
        {% endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_endblock_missing_first_modulo_found_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}
        { endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_endblock_missing_second_modulo_found_raises_error(self):  
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}
        {% endblock css }
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
    
    def test_in_childblock_endblock_block_spelled_wrong_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}
        {% endblok css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_endblock_missing_starting_brace_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}
        % endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
            
    def test_in_childblock_endblock_missing_ending_brace_found_raises_error(self):         
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}
        {% endblock css %
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections
       
    def test_in_childblock_same_section_key_defined_twice_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
        {% block css %}
        {% endblock css %}
        {% block css %}
        {% endblock css %}
        {% endblock header %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(KeyError):
            template.sections
            
    def test_same_section_key_defined_twice_raises_error(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header %}
            {% block css %}
            {% endblock css %}
        {% endblock header %}
        {% block css %}
        {% endblock css %}
        ''')
        html = html.substitute(location = self.working_templates)
        template = Template(html, self.working_templates)
        with self.assertRaises(KeyError):
            template.sections
    
    def test_block_inherit_with_parent_tag_without_inherits_raises_error(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header %}
        {parent}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections   
            
    def test_block_keepnested_with_parent_tag_raises_error(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header keepnested%}
        {parent}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        with self.assertRaises(SyntaxError):
            template.sections   