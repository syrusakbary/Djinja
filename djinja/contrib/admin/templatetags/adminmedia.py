from djinja import template
from django.utils.encoding import iri_to_uri
from django.conf import settings


register = template.Library()
# def admin_media_prefix ():
#     try:
#         from django.conf import settings
#     except ImportError:
#         prefix = ''
#     else:
#         prefix = iri_to_uri(getattr(settings, 'ADMIN_MEDIA_PREFIX', ''))
#     return prefix

register.set(admin_media_prefix=iri_to_uri(settings.ADMIN_MEDIA_PREFIX))