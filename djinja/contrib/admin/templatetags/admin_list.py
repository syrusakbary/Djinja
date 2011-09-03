from django.contrib.admin.templatetags.admin_list import paginator_number,pagination,result_list, date_hierarchy, search_form, admin_list_filter, admin_actions
from djinja import template
import jinja2 

register = template.Library()
register.tag(paginator_number)

register.inclusion_tag('admin/pagination.html', pagination)
register.inclusion_tag('admin/change_list_results.html', result_list)
register.inclusion_tag('admin/date_hierarchy.html', date_hierarchy)
register.inclusion_tag('admin/search_form.html', search_form)
register.inclusion_tag('admin/filter.html', admin_list_filter)
register.inclusion_tag('admin/actions.html', admin_actions, True)