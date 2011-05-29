from djinja.template.base import Library
from django.utils.importlib import import_module
from django.conf import settings
import jinja2

register = Library()

# def execute (lib,function,*args,**kwargs):
#     l = import_module(lib)
#     #raise Exception(args)
#     f = getattr(l,function)
#     return f(*args,**kwargs)
# register.tag(execute)
# 
# @jinja2.contextfunction
# def execute_context (context,lib,function,*args,**kwargs):
#     l = import_module(lib)
#     #raise Exception(args)
#     context_dict = {}
#     for d in context.keys():
#         context_dict[d] = context.get(d)
#     f = getattr(l,function)
#     return f(context_dict,*args,**kwargs)
# 
# register.tag(execute_context)


def url(view_name, *args, **kwargs):
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        try:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            return reverse(project_name + '.' + view_name,
                           args=args, kwargs=kwargs)
        except NoReverseMatch:
            return ''
register.tag(url)

class Load(object):
    def __init__(self,module):
        from django.template import get_library
        self._module = get_library(module)
        #raise Exception(self._module.globals)

    @property
    def globals(self):
        return self._module.globals

    def __getitem__ (self,key):
        return self.globals[key]
register.tag(Load,name='load')
