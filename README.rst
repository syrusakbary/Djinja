======
Djinja
======

`Djinja <http://github.com/syrusakbary/djinja>` tries to integrate `Jinja2
<http://jinja.pocoo.org/2/>` in `Django <http://www.djangoproject.com/>`. The aim is to replace
completely the Django's template system, **including administration**.

Currently, the following templating modules have been written and are working:

- Django administration
- Django Debug Toolbar

Also, is planned to implement one Django management command (**NOT CURRENTLY**):

- `compiletemplates`: Compile the Jinja2 templates for completely fast views in your website.

If you have ideas please let us know.

Installation
============

#. Add the `djinja` directory to your Python path.

#. Add the following template loader to your project's `settings.py` file:

	``'djinja.template.loaders.Loader',``

   Tying into template loaders allows Djinja to manage automatically **ALL**
   the templates with Jinja2 (including Django templates)

   Note: If you don't install djinja.contrib.admin when you try to access
   to the Django administration you will get an error, this is caused because
   the Django administration templates are not adapted for Jinja2.
   
#. That's all! ;)

Configuration
=============

No configuration for now, but is expected in next releases. 

Administration
==============

For install the Django administration Jinja2 templating just add
'djinja.contrib.admin' before 'django.contrib.admin' in your INSTALLED_APPS
in `settings.py`.

Example:
	INSTALLED_APPS = (
	    ...
	    'djinja.contrib.admin',
	    'django.contrib.admin',
	    ...
	)

Django Debug Toolbar
====================

For install the Django Debug Toolbar Jinja2 templating just add
'djinja.contrib.debug_toolbar' before 'debug_toolbar' in your INSTALLED_APPS
in `settings.py`.

Example:
	INSTALLED_APPS = (
	    ...
	    'djinja.contrib.debug_toolbar',
	    'debug_toolbar',
	    ...
	)
	
TODOs and BUGS
==============
See: http://github.com/syrusakbary/djinja/issues