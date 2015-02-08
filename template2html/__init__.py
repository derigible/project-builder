'''
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


'''