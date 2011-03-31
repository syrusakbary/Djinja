"""
See http://docs.djangoproject.com/en/dev/ref/templates/api/#using-an-alternative-template-language

"""

from django.template.loaders import app_directories
from django.conf import settings
from django.template import TemplateDoesNotExist
from jinja2 import nodes
from djinja.template import Environment
import jinja2


app_template_dirs = app_directories.app_template_dirs + settings.TEMPLATE_DIRS


from djinja.template import Template
from djinja.template.defaultfunctions import url

class Loader(app_directories.Loader):
    is_usable = True
    env = Environment(loader=jinja2.FileSystemLoader(app_template_dirs),extensions=['jinja2.ext.i18n'])
    
    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)



def make_jinja2_tag(node,*args,**kwargs):
    def f(*args,**kwargs):
        return node(*args,**kwargs).render({})
    return f
