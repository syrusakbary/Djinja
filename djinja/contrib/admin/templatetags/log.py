from djinja import template
from django.contrib.admin.models import LogEntry
import jinja2 


register = template.Library()

@jinja2.contextfunction
def get_admin_log(context,limit,user=None):
    if user is None:
        return LogEntry.objects.all().select_related('content_type', 'user')[:limit]
    else:
        #user_id = user
        user_id = user.id
        #raise Exception(context['user'])
        return LogEntry.objects.filter(user__id__exact=user_id).select_related('content_type', 'user')[:limit]

register.tag(get_admin_log)