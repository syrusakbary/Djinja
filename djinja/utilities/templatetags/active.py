from djinja import template
from django.core.urlresolvers import resolve

import jinja2
register = template.Library()
@jinja2.contextfunction
def active (context,*args):
    match = resolve(context['request_path'])
    return (match.url_name in args)
    #if context['request_path'] in ( reverse(url) for url in args ):
    #    return True
    #return False
    
register.tag(active)
