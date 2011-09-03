import os
import warnings

from django import dispatch
from jinja2 import Environment as Jinja2Environment, Template as Jinja2Template, loaders, TemplateSyntaxError, FileSystemLoader
from django.utils.importlib import import_module
from django.conf import settings
from django.template import TemplateDoesNotExist, Origin, InvalidTemplateLibrary
from django.utils.module_loading import module_has_submodule

__all__ = [
    'env',
]

builtins = []

_JINJA_I18N_EXTENSION_NAME = 'jinja2.ext.i18n'

from django.template.context import BaseContext
def dict_from_context (context):
    if isinstance(context,BaseContext):
        d = {}
        for i in reversed(list(context)):
            d.update(dict_from_context(i))
        return d
    else:
        return dict(context)


class Template(Jinja2Template):
    def render(self, context):
        context_dict = dict_from_context(context)
        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)
    
        return super(Template, self).render(context_dict)

class Environment(Jinja2Environment):
    def __init__(self, filters={}, globals={}, tests={}, loader=None, extensions=[], **kwargs):
        #if not loader:
        #    loader = loaders.ChoiceLoader(self._get_loaders())
        all_ext = self._get_all_extensions()
        
        extensions.extend(all_ext['extensions'])
        #raise Exception(all_ext)
        super(Environment, self).__init__(extensions=extensions, loader=loader, **kwargs)
        self.filters.update(filters)
        self.filters.update(all_ext['filters'])
        self.globals.update(globals)
        self.globals.update(all_ext['globals'])
        self.tests.update(tests)
        #self.tests.update(all_ext['tests'])
        
        if settings.USE_I18N:
            from django.utils import translation
            self.install_gettext_translations(translation)
        else:
            self.install_null_translations(newstyle=False)
            
        self.template_class = Template
        
#    def _get_loaders(self):
#        """Tries to translate each template loader given in the Django settings
#        (:mod:`django.settings`) to a similarly-behaving Jinja loader.
#        Warns if a similar loader cannot be found.
#        Allows for Jinja2 loader instances to be placed in the template loader
#        settings.
#        """
#        loaders = []
#        
#        #from coffin.template.loaders import jinja_loader_from_django_loader
#
#        from django.conf import settings
#        for loader in settings.TEMPLATE_LOADERS:
#            if isinstance(loader, basestring):
#                #loader_obj = jinja_loader_from_django_loader(loader)
#                if loader_obj:
#                    loaders.append(loader_obj)
#                else:
#                    warnings.warn('Cannot translate loader: %s' % loader)
#            else: # It's assumed to be a Jinja2 loader instance.
#                loaders.append(loader)
#        return loaders


    def _get_templatelibs(self):
        """Return an iterable of template ``Library`` instances.

        Since we cannot support the {% load %} tag in Jinja, we have to
        register all libraries globally.
        """
        from django.conf import settings
        from django.template import get_library, InvalidTemplateLibrary

        libs = []
        for a in settings.INSTALLED_APPS:
            try:
                path = __import__(a + '.templatetags', {}, {}, ['__file__']).__file__
                path = os.path.dirname(path)  # we now have the templatetags/ directory
            except ImportError:
                pass
            else:
                for f in os.listdir(path):
                    if f == '__init__.py':
                        continue
                    if f.endswith('.py'):
                        try:
                            # TODO: will need updating when #6587 lands
                            # libs.append(get_library(
                            #     "django.templatetags.%s" % os.path.splitext(f)[0]))
                            libs.append(get_library(os.path.splitext(f)[0]))
                            
                        except InvalidTemplateLibrary:
                            pass
        return libs

    def _get_all_extensions(self):

        from django.core.urlresolvers import get_callable

        extensions, filters, globals, tests = [], {}, {}, {}

        # start with our builtins
        for lib in builtins:
            extensions.extend(getattr(lib, 'extensions', []))
            filters.update(getattr(lib, 'filters', {}))
            globals.update(getattr(lib, 'globals', {}))
            tests.update(getattr(lib, 'tests', {}))
        

        if settings.USE_I18N:
            extensions.append(_JINJA_I18N_EXTENSION_NAME)

        # add the globally defined extension list
        extensions.extend(list(getattr(settings, 'JINJA2_EXTENSIONS', [])))

        def from_setting(setting):
            retval = {}
            setting = getattr(settings, setting, {})
            if isinstance(setting, dict):
                for key, value in setting.iteritems():
                    retval[key] = callable(value) and value or get_callable(value)
            else:
                for value in setting:
                    value = callable(value) and value or get_callable(value)
                    retval[value.__name__] = value
            return retval

        filters.update(from_setting('JINJA2_FILTERS'))
        globals.update(from_setting('JINJA2_GLOBALS'))
        tests.update(from_setting('JINJA2_TESTS'))

        # add extensions defined in application's templatetag libraries
        djinja_settings = from_setting('DJINJA')
        
        if getattr(djinja_settings,'autoload',False):
            for lib in self._get_templatelibs():
                extensions.extend(getattr(lib, 'extensions', []))
                filters.update(getattr(lib, 'filters', {}))
                globals.update(getattr(lib, 'globals', {}))
                tests.update(getattr(lib, 'tests', {}))
        
        return dict(
            extensions=extensions,
            filters=filters,
            globals=globals,
            tests=tests,
        )
env = None

def get_env():
    global env
    if env is None:
        from django.conf import settings
        from django.template.loaders import app_directories
        app_template_dirs = app_directories.app_template_dirs + settings.TEMPLATE_DIRS
        kwargs = {
            'autoescape': False,
            'loader':FileSystemLoader(app_template_dirs),
            'extensions':['jinja2.ext.i18n']
        }
        kwargs.update(getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {}))
        env = Environment(**kwargs)
    return env


        
class Library(object):
    def __init__(self):
        self.filters = {}
        self.extensions = []
        self.globals = {}
        self.tests = {}
    def tag(self, func,name=None):
        if name==None:
            name = getattr(func, "_decorated_function", func).__name__
        self.globals[name] = func

    def filter(self, func,name=None):
        if name==None:
            name = getattr(func, "_decorated_function", func).__name__
        self.filters[name] = func

    def extension(self, ext):
        self.extensions.append(ext)
    
    def set(self,*args,**kwargs):
        for k in kwargs.keys(): #is a object with a name
            self[k] = kwargs[k]
        for a in args:
            self.tag(a) #is a function
        
    def inclusion_tag(self,template,func,takes_context=False):
        if takes_context:
            import jinja2
            @jinja2.contextfunction
            def tag(context,*args,**kwargs):
                from django.template.loader import render_to_string
                return render_to_string(template, func(dict_from_context(context),*args,**kwargs))
            
        else:
            def tag(*args,**kwargs):
                from django.template.loader import render_to_string
                return render_to_string(template, func(*args,**kwargs))
        
        #raise Exception(getattr(func, "_decorated_function", func))
        self.tag(tag,name=getattr(func, "_decorated_function", func).__name__) 
    
    def __setitem__(self, item, value):
        self.globals[item] = value
    
    def __getitem__(self, item, value): #for reciprocity with __setitem__
        return globals[item]
    
def import_library(taglib_module):
    """Load a template tag library module.

    Verifies that the library contains a 'register' attribute, and
    returns that attribute as the representation of the library
    """
    app_path, taglib = taglib_module.rsplit('.',1)
    app_module = import_module(app_path)
    try:
        mod = import_module(taglib_module)
    except ImportError, e:
        # If the ImportError is because the taglib submodule does not exist, that's not
        # an error that should be raised. If the submodule exists and raised an ImportError
        # on the attempt to load it, that we want to raise.
        if not module_has_submodule(app_module, taglib):
            return None
        else:
            raise InvalidTemplateLibrary("ImportError raised loading %s: %s" % (taglib_module, e))
    try:
        return mod.register
    except AttributeError:
        raise InvalidTemplateLibrary("Template library %s does not have a variable named 'register'" % taglib_module)

def add_to_builtins(module):
    m = import_library(module)
    builtins.append(m)

#import  djinja.template.defaultfunctions
add_to_builtins('djinja.template.defaultfunctions')
add_to_builtins('djinja.template.defaultextensions')
add_to_builtins('djinja.template.defaultfilters')
#env = get_env()