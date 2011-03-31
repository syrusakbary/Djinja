"""
See http://docs.djangoproject.com/en/dev/ref/templates/api/#using-an-alternative-template-language

Use:
 * {{ url_for('view_name') }} instead of {% url view_name %},
 * <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
   instead of {% csrf_token %}.

"""

from django.template.loader import BaseLoader
from django.template.loaders.app_directories import app_template_dirs
from django.conf import settings
from django.template import TemplateDoesNotExist
import jinja2
app_template_dirs += settings.TEMPLATE_DIRS


from django.template.loaders import app_directories
#print app_template_dirs

from jinja2 import nodes
from django.utils.safestring import mark_safe







from djinja.template import Environment

from djinja.template.defaultextensions import CsrfExtension

from djinja.template.base import Library
from jinja2.ext import Extension
import traceback
from django.utils.safestring import mark_safe

from djinja.template.defaultextensions import CsrfExtension

#register = Library()

# class CsrfExtension(Extension):
#     # a set of names that trigger the extension.
#     tags = set(['csrf_token'])
# 
#     def __init__(self, environment):
#         self.environment = environment
# 
#     def parse(self, parser):
#         try:
#             token = parser.stream.next()
#             return nodes.Output([self.call_method('_render', [nodes.Name('csrf_token','load')])]).set_lineno(token.lineno)
# 
#         except:
#             traceback.print_exc()
# 
#     def _render(self, csrf_token):
#         """Helper callback."""
#         if csrf_token:
#             if csrf_token == 'NOTPROVIDED':
#                 return mark_safe(u"")
#             else:
#                 return mark_safe(u"<div style='display:none'><input type='hidden' name='csrfmiddlewaretoken' value='%s' /></div>" % (csrf_token))
#         else:
#             # It's very probable that the token is missing because of
#             # misconfiguration, so we raise a warning
#             from django.conf import settings
#             if settings.DEBUG:
#                 import warnings
#                 warnings.warn("A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.")
#             return u''

from djinja.template import Template
from djinja.template.defaultfunctions import url
class Loader(app_directories.Loader):
    is_usable = True
    
    #env = djenv
    #env.loader = jinja2.FileSystemLoader(app_template_dirs)
    env = Environment(loader=jinja2.FileSystemLoader(app_template_dirs),extensions=['jinja2.ext.i18n'])
    #env = jinja2.Environment(loader=jinja2.FileSystemLoader(app_template_dirs),extensions=['jinja2.ext.i18n',CsrfExtension])
    #env.install_null_translations(newstyle=False)
    #env.template_class = Template
    #env.install_null_translations(newstyle=False)
    # These are available to all templates.
    env.globals['url'] = url
    #env.globals['MEDIA_URL'] = settings.MEDIA_URL
    #env.globals['STATIC_URL'] = settings.STATIC_URL
    

    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)






#Loader.env.globals['url'] = rev

def make_jinja2_tag(node,*args,**kwargs):
    def f(*args,**kwargs):
        return node(*args,**kwargs).render({})
    return f

from jinja2 import Markup


def sprite_class(url):
    return 'sprite_'

from django.core.urlresolvers import reverse



from mediasync.templatetags.media import *
Loader.env.globals['media_url'] = make_jinja2_tag(MediaUrlTagNode)
Loader.env.globals['css'] = make_jinja2_tag(CssTagNode)
Loader.env.globals['js'] = make_jinja2_tag(JsTagNode)

#Loader.env.globals['media_url'] = lambda x:x
#Loader.env.globals['css'] = lambda x:x
#Loader.env.globals['js'] = lambda x:x

#def csrf_token(csrf_token=""):
#    from django.template.defaulttags import CsrfTokenNode
#    return CsrfTokenNode().render({'csrf_token': csrf_token})
#Loader.env.globals['csrf_tokena'] = csrf_token
#from djinja.template.defaultfunctions import execute, execute_context
#Loader.env.globals['sprite_class'] = sprite_class
#Loader.env.globals['execute'] = execute
#Loader.env.globals['execute_context'] = execute_context
#Loader.env.globals['active'] = active