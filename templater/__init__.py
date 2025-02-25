__doc__ = '''
template2html is inspired by the jinja templating system used in Django, except that it will output static html documents
and, in build_project.py fashion, unit tests and documentation. It also enforces strict conventions that make testing html
pages much easier. The primary purpose of these conventions is to make element selection in frameworks like Selenium
output automatically into unit tests.

SELECTOR CONVENTION REASONING

By default, the unit tests for template2html assume Selenium web testing. You are free to alter the assumption by pointing
the template2html's settings.py variable TESTS equal to another test_builder.py instance using typical pythonpath notation
(i.e. module.is.here). Doing so will take tests creation out of the build_project frameworks hands and enforcing conventions
is up to the developer of the test_builder.py instance. 

Selenium was chosen as the default because it is commonly used and free. However, no matter what framework you
decide to use for the unit tests, template2html will output page objects that are agnostic to any web testing framework
(for more information on page objects, see http://selenium-python.readthedocs.org/en/latest/page-objects.html). This is a
good practice and standard and so will be applied to the unit tests being used. It will be up to the developer of
test_builder.py to determine what the underlying scripts will output.

TEMPLATING RULES AND SYNTAX

The jinja templating is pretty straightforward, and you enter blocks of html in between tags as follows:

{% block header %} {% endblock header %}

template2html does the same thing, and any pages that inherit from another page with blocks defined can override the
html inside the parent block by writing new (or nothing) into the block. Note that setting a block that has nest blocks
to empty will clear all nested blocks as well. However, if you wish to keep nested blocks, do the following:

{% block header keepnested %} {% endblock header %}

This means that any blocks that have been defined inside the header will be kept while clearing out the sibling html. If you want to 
keep the main block and add some html while also changing a nested block, do the following:

{% block header inherit%}
    ''some more html code
    {% block childblock inherit %} ''some more html code  {% endblock childblock %}
{% endblock header %}

or

{% block header inherit%}
    ''some more html code
    {% block childblock %} ''some more html code  {% endblock childblock %}
{% endblock header %}

Where the first example will inherit the child block from the parent block, and the second redefines the child block. This
will also keep all the nested blocks as they are.

To add html before or after the inherited parent block, you can do the following:

{% block header inherit%}
    ''some html code
    {parent}
{% endblock header %}

or

{% block header inherit%}
    {parent}
    ''some html code
{% endblock header %}


Nested blocks can be overridden in children templates in two ways:

To change the childblocks and remove the html from the parent block:

{% block header keepnested %} 
    {%block childblock %} {endblock childblock %} 
{% endblock header %}

or, if you wish to only change the nest block and keep the parent block:

{%block childblock %} {endblock childblock %}

or

{% block header inherit %} 
    {%block childblock %} {endblock childblock %} 
{% endblock header %}

The first one will look for any block that has been called childblock and will change the first one found (note that having two blocks of the same name
is a KeyError and will be treated as such). 

Templates that inherit from another template cannot add html without surrounding it with a block.

Adding blocks to a parent template will simply append the html to the bottom of the page unless the first parent block that should
come after the new block is defined as well. template2html will keep track of the order of all blocks and in what order they
are added.

Inheriting from a template is done as follows:

{% extends parent.html %}

The parent.html will only work if the template is in the same directory as the child. If it is not, you must use the
absolute path to the template.

Template Reserved Words

These words can't be used inside of the block tags as names.

parent
foot
names cannot contain the {, } or % characters

CSS tags

Css uses the { and } characters to contain its code inside html. Also, some js libraries use the { } in combination
with some other characters to denote a field. If your library does this, try to change the interpolation to {{ and }},
or do the following:

For CSS:

enclose all css tags with the opening !css

For js libraries:

change the interpolation of your js library to {{ and }}, or start the enclose of your js calls with !js and set the templater
interpolation variable to the opening field enclosing you wish.

The reason that the opening enclosure character is the only character that matters is that the parser only looks for the
{ character when opening and the % when closing a block. The characters next to these characters determine if it is a valid
opening or closing block.

ADDING LOGIC

In jinja, pages are made dynamically using logic based upon the values that the web server found for the page. This is not
relevant for static pages, but some logic can still be applied.

For example, if you want to create five sections of blocks that have pretty similar html that will change with javascript
on the client side, then do the following:

{{for 5 <unique_for_name>}}
    ''html here
    reference the loop by {{i}}
{{endfor <unique_for_name>}}

This is the only logic available for now.

CONVENTIONS TO FOLLOW

inputs

buttons

headers

navigation
    -urls
    -external urls
    
divs

javascript events

how to register custom conventions
'''
from versioner import get_version

VERSION = (0, 0, 0, 'alpha', 0)

__version__ = get_version(VERSION)

interpolation = '{{'