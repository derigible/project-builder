'''
Created on Feb 8, 2015

@author: derigible
'''
import os
from tests.base_test import BaseTest as base
from template2html import testdata
from template2html.structure import Template
from string import Template as stemp

class Template2HtmlTest(base):
    '''
    Tests the functionality of the template2html module.
    '''
    test_dir = __test_data_dir__ = testdata.__path__[0]
    working_templates = os.path.join(test_dir, "templates")
    nonworking_templates = os.path.join(test_dir, "badtemplates")
    allowed_additional_words = ('inherit', 'keepnested')
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
            #global-engage-header {padding-top: 25px;}
            h1 {
                padding-top: .5em;
                padding-bottom: 0;
                margin-bottom: 0;
            }
            h2 {
                font-size: 1.5em;
                padding-bottom: 0;
                margin-bottom: 0;
            }
        </style>'''
    
    def test_template_extension_from_remote_directory(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.nonworking_templates)
        self.assertCountEqual(3, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertListEqual(template.dependency, self.working_templates +"/template_test_single_section.html")
        
    def test_template_extension_from_local_directory(self):
        html = '''
        {% extends template_test_single_section.html %}
        '''
        h = html
        template = Template(h, self.working_templates)
        self.assertCountEqual(3, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")
            
    def test_block_inheritance(self):
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header inherits %}
        $newhtml
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates, newhtml = "<link rel='author' title='Test' href='#'>")
        template = Template(h, self.working_templates)
        self.assertCountEqual(3, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")
            
    def test_block_inheritance_inherits_found(self):  
        html = stemp('''
        {% extends $location/template_test_single_section.html %}
        {% block header inherits %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(3, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
            
    def test_block_keepnested_found(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header keepnested %}
        {% block css %}
        
        {% endblock css %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_keepnested_parent_html_removed(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header keepnested %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "<link rel='author' title='Test' href='#'>{css}") #a template keeps track of the html it has by linking the html of another template by its block name
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_inherit_keeps_html(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "{parent}<link rel='author' title='Test' href='#'>") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_inherit_keeps_html_with_parent_tag_after(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %}
        <link rel='author' title='Test' href='#'>
        {parent}
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "<link rel='author' title='Test' href='#'>{parent}") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_inherit_keeps_html_with_parent_tag_before(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %} 
        {parent}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "{parent}<link rel='author' title='Test' href='#'>") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")  
         
    def test_block_inherit_keeps_html_with_parent_tag_and_redefine_block_before(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %}
        {parent}
        {% block css %}
        <link rel='author' title='Test' href='#'>
        {% endblock css %}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "{parent}{css}<link rel='author' title='Test' href='#'>") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_inherit_keeps_html_with_parent_tag_and_redefine_block_after(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %}
        {% block css %}
        <link rel='author' title='Test' href='#'>
        {% endblock css %}
        <link rel='author' title='Test' href='#'>
        {parent}
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "{css}<link rel='author' title='Test' href='#'>{parent}") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_inherit_keeps_html_with_parent_tag_and_redefine_block_inbetween(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %}
        {% block css %}
        <link rel='author' title='Test' href='#'>
        {% endblock css %}
        {parent}
        <link rel='author' title='Test' href='#'>
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "{css}{parent}<link rel='author' title='Test' href='#'>") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
        
    def test_block_inherit_keeps_html_with_parent_tag_and_redefine_block_html_first(self):  
        html = stemp('''
        {% extends $location/template_test_single_section_with_nested.html %}
        {% block header inherits %}
        <link rel='author' title='Test' href='#'>
        {% block css %}
        <link rel='author' title='Test' href='#'>
        {% endblock css %}
        {parent}
        {% endblock header %}
        ''')
        h = html.substitute(location = self.working_templates)
        template = Template(h, self.working_templates)
        self.assertCountEqual(4, len(template.sections))
        self.assertCountEqual(1, len(template.dependency))
        self.assertMultiLineEqual(template.sections["header"]["html"], "<link rel='author' title='Test' href='#'>{css}{parent}") #a template keeps track of the html in the parent by marking parent
        self.assertMultiLineEqual(template.dependency, "/template_test_single_section.html")   
            
    