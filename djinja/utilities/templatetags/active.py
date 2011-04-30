from djinja import template
from django.core.urlresolvers import reverse

import jinja2
register = template.Library()
@jinja2.contextfunction
def active (context,*args):
    if context['request_path'] in ( reverse(url) for url in args ):
        return True
    return False
    
register.tag(active)
