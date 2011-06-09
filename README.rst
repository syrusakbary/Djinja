======
Djinja
======

Djinja tries to **integrate Jinja2 in Django**. The aim is to replace
completely the Django's template system, **including administration**.

Currently, the following templating modules have been written and are working:

- Django administration
- Django Debug Toolbar

In a near future, you could convert **Django templates syntax to Jinja2 syntax**, isn't awesome?

If you have ideas please let us know.

Installation
============

#. Add the `djinja` directory to your Python path.

#. Add the following template loader (**AT TOP OF TEMPLATE_LOADERS**) to your project's `settings.py` file:

	``'djinja.template.loaders.Loader',``

   Tying into template loaders allows Djinja to manage automatically **ALL**
   the templates with Jinja2 (including Django templates)

   Note: If you don't install djinja.contrib.admin when you try to access
   to the Django administration you will get an error, this is caused because
   the Django administration templates are not adapted for Jinja2.
   
#. That's all! ;)


**IMPORTANT**: You have to adapt your website templates to Jinja2 or you
will get an error when rendering (until the djinja converser is ready).

Custom filters and extensions
=============================

Djinja uses the same templatetag library approach as Django, meaning
your app has a ``templatetags`` directory, and each of it's modules
represents a "template library", providing new filters and tags.

A custom ``Library`` class in ``djinja.template.Library`` can be used
to register Jinja-specific components.

Djinja can automatically make your existing Django filters usable in
Jinja, but not your custom tags - you need to rewrite those as Jinja
extensions manually.

Example for a Jinja-enabled template library::

    from djinja import template
    register = template.Library()

    register.filter(plenk, 'plenk')   		# Filter function
    register.extension(FooExtension)        	# Jinja version of the tag
    register.tag(my_function_name) 		# A global function/object
    register.set(a='hello') 			# A context variable (named a)

You may also define additional extensions, filters, tests, and globas via your ``settings.py``::

    JINJA2_FILTERS = (
        'path.to.myfilter',
    )
    JINJA2_EXTENSIONS = (
        'jinja2.ext.do',
    )

HAML
====

Djinja can render HAML pages (having installed ``HamlPy`` - https://github.com/jessemiller/HamlPy), and is as just simple as put the .haml extension to your template and adding ``'djinja.template.extensions.haml'`` in the JINJA2_EXTENSIONS variable of your settings::


   JINJA2_EXTENSIONS = (
	...
        'djinja.template.extensions.haml',
	...
    )

**HAML templates can also include,extend,etc HTML templates and viceversa.**

Administration
==============

For install the Django administration Jinja2 templating just add ``'djinja.contrib.admin',`` before 'django.contrib.admin' in your INSTALLED_APPS in `settings.py`.

Example configuration::

	INSTALLED_APPS = (
	    ...
	    'djinja.contrib.admin',
	    'django.contrib.admin',
	    ...
	)


Benchmarking
------------

Running tests::
	
	ab -n100 http://localhost/admin/
		
In Django
		
	Requests per second:    67.93 [#/sec] (mean)
	Time per request:       14.721 [ms] (mean)

With Jinja2 (Djinja)
		
	Requests per second:    202.16 [#/sec] (mean)
	Time per request:       4.947 [ms] (mean)


**3x performance using Jinja2 instead of Django templating in administration**

Django Debug Toolbar
====================

For install the Django Debug Toolbar Jinja2 templating just  add ``'djinja.contrib.debug_toolbar',`` before 'debug_toolbar' in your INSTALLED_APPS in `settings.py`.

Example configuration::

	INSTALLED_APPS = (
	    ...
	    'djinja.contrib.debug_toolbar',
	    'debug_toolbar',
	    ...
	)

TODOs and BUGS
==============
See: http://github.com/syrusakbary/djinja/issues