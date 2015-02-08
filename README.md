template2html is inspired by the Django jinja templating framework (and other similar templating systems). However, 
unlike templating systems inside of most frameworks, this will output static html pages from a template. There are several
systems already available to do this, but none of them are made to fit into an overall suite of project creation. This
module is part of a core suite of modules that aims to automate the creation, testing, and building of web projects.

The main philosophy behind this approach stems from the fact that too much time is spent in web development translating
work done by developers into actionable tests and resources for quality assurance and/or other developers to use. Several
tools focus on automating the documentation process, but they all fall short of really automating the process since
developers end up having to write the documentation, tests, and so forth for things several times over, creating poor
communication and missed testing opportunities.

To resolve some of the pain of development to test creation, and also from development to documentation and deployment,
this framework seeks to strictly enforce certain conventions. These include:

	1) Every public function has a docstring with the appropriate @params, @returns, and @raises documenation.
	2) Common artifacts are given a similar name by convention (i.e. ui button named button_*)
	3) At least one unittest per public function
	
If the following conventions are not met (at least in those areas where the system can detect a break from convention) the
build will fail and point developers to all non-conforming areas.

Each module will define the conventions used in the __init__.py file. Also in this __init__.py file there should be a
two methods: run_convention_checks() and build(). If run_convention_checks() has not been run, then build() should raise
and error (or run_convention_checks()).

++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HOW TO USE
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Each module should define a public interface for other projects to build their projects. Inside of the __init__.py should
be a function (i.e. register()) that is called to store the location of any inheriting classes. An example of this is as follows:

Say that you have an html project that you want to build using the template2html module. You could create a project structure
as follows:

	-templates
		|
		 - register.py
		 - base.html
		 - page1.html
		 - page2.html
		
Inside each file you will do the following:
	1) Inside register.py import template2html.
	2) Put "add /path/to/file/" ("add .../templates/base.html") to each file.
	3) Inside register.py, create a function that gets all other non .py files in the current directory and checks for the "add"
	   keyword at the start of the file.
	4) Add the absolute path to the build.py file for your project (more on this below).

Note that this is specific to template2html; check each modules __init__.py doc for how to register a file.

Now that you have done those steps, use build_project.py /path/to/build.py -r build. To run the convention checks, use build_project.py /path/to/build.py -r convention_check.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++
PROJECT CONFIGURATION
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

As ironic as it is that project builder depends on a configuration file despite its insistence on convention, configuration
makes things a lot easier when not many configurations are needed. That being said, the build.py file can actually be
named any legal python file name.

So what does the build.py file look like? It is simply a tuple with paths to the project's directories that are
included in the build process. This tuple is called BUILD.

To illustrate using the example above, we would have a build.py file like the following:

BUILD = (".../templates",)

That's it. Plug away and enjoy the builder do its stuff.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++
CUSTOMIZATION
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The builder module will not allow a build to complete if the aforementioned conventions are not met. However, it is possible
to build one aspect of the builder without wasting time on the others. For example, you want to build and run the testsuite
for your projects but don't want to build the docs. You would do the following:

build_project.py /path/to/build.py -r build -t -x

The -t will tell builder.py to build only the tests, and the -x tells builder.py to execute those tests. Builder was also
inspired by other great testing frameworks, such as py.test; so naturally you can run a subset of tests using keywords:

build_project.py /path/to/build.py -r build -t -x "keywords,as,csv"

Pass any any number of keywords as a csv and builder.py will run those selected tests. Other options are forthcoming, but
that is the gist of the current customization options.

BUILD_PROJECT.PY

This is the runner for the entire project builder system. This will have a tuple of tuples and 2-tuples that define
what builder modules are being used and where they are located. This tuple will be called MODULES. As an example:

To add the template2html module, you will have MODULES assigned to the following:

MODULES = (("template2html"),)

Since template2html is already defined in the builder project, it will search the directories within the builder project
for template2html, throwing an ImportError if not found. Now let's say you define a builder module that is not found inside
the builder default project. Simply edit the MODULES tuple as follows:

MODULES = (("template2html"), ("othermodule", "/absolute/path/to/othermodule"))

The path must be absolute. In later versions this will likely just search the python path (and so must be an importable
module on the pythonpath, but I don't want to worry about that right now).

++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ENFORCING AND CREATING DOCUMENTATION
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The module pydocs is used to create the documentation. It is encouraged when creating a builder module to start
all module level docstrings with the __doc__ attribute. All other docstrings should follow the instructions given in the
pydocs help page (https://docs.python.org/3.4/library/pydoc.html#module-pydoc).