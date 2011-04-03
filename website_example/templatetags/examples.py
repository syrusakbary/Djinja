from djinja import template
from django.utils.encoding import iri_to_uri


register = template.Library()

@register.tag #You can use this form
def basic_tag():
    return 'Basic tag!'

def reverse(a): 
    return a[::-1]
    
register.filter(reverse) #Or this! As you can see, you can set the same function as tag or filter :D
register.tag(reverse)

register.set(var_example='Example variable')