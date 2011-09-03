from django.contrib.admin.templatetags.admin_modify import submit_row,prepopulated_fields_js
from djinja import template
import jinja2 

register = template.Library()
register.inclusion_tag('admin/submit_line.html', submit_row,True)
register.inclusion_tag('admin/prepopulated_fields_js.html', prepopulated_fields_js,True)