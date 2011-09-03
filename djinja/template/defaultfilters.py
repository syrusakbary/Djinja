"""Jinja2-ports of many of Django's default filters.

TODO: Most of the filters in here need to be updated for autoescaping.

TAKED FROM COFFIN: https://github.com/cdleary/coffin
(and adapted for djinja library)
"""

from djinja.template.base import Library
from jinja2.runtime import Undefined
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.conf import settings
register = Library()

@register.filter
def url(view_name, *args, **kwargs):
    url = ''
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        url = reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        projectname = settings.SETTINGS_MODULE.split('.')[0]
        try:
            url = reverse(projectname + '.' + view_name,
                          args=args, kwargs=kwargs)
        except NoReverseMatch:
            raise

    return url


@register.filter
def timesince(value, *arg):
    if value is None or isinstance(value, Undefined):
        return u''
    from django.utils.timesince import timesince
    return timesince(value, *arg)

@register.filter
def date(value, arg=None):
    if value is None or isinstance(value, Undefined):
        return u''
    from django.conf import settings
    from django.utils.dateformat import format
    if arg is None:
        arg = settings.DATETIME_FORMAT
    return format(value, arg)

@register.filter
def time(value, arg=None):
    if value is None or isinstance(value, Undefined):
        return u''
    from django.conf import settings
    from django.utils.dateformat import time_format
    if arg is None:
        arg = settings.TIME_FORMAT
    return time_format(value, arg)

@register.filter
def truncatewords(value, length):
    # Jinja2 has it's own ``truncate`` filter that supports word
    # boundaries and more stuff, but cannot deal with HTML.
    from django.utils.text import truncate_words
    return truncate_words(value, int(length))

@register.filter
def truncatewords_html(value, length):
    from django.utils.text import truncate_html_words
    return truncate_html_words(value, int(length))


@register.filter
def pluralize(value, s1='s', s2=None):
    """Like Django's pluralize-filter, but instead of using an optional
    comma to separate singular and plural suffixes, it uses two distinct
    parameters.

    It also is less forgiving if applied to values that do not allow
    making a decision between singular and plural.
    """
    if s2 is not None:
        singular_suffix, plural_suffix = s1, s2
    else:
        plural_suffix = s1
        singular_suffix = ''

    try:
        if int(value) != 1:
            return plural_suffix
    except TypeError: # not a string or a number; maybe it's a list?
        if len(value) != 1:
            return plural_suffix
    return singular_suffix

@register.filter
def firstof(vars):
    for var in vars:
        if var:
            return var
    return ''

from django.utils.safestring import SafeUnicode, SafeData, EscapeData
from jinja2 import Markup, environmentfilter

#Taked from coffin.interop https://github.com/cdleary/coffin/blob/master/coffin/interop.py
def django_filter_to_jinja2(filter_func):
    def _convert(v):
        if isinstance(v, SafeData):
            return Markup(v)
        if isinstance(v, EscapeData):
            return Markup.escape(v)       # not 100% equivalent, see mod docs
        return v
    def conversion_wrapper(*args, **kwargs):
        result = filter_func(*args, **kwargs)
        return _convert(result)
    if hasattr(filter_func, 'needs_autoescape'):
        @environmentfilter
        def autoescape_wrapper(environment, *args, **kwargs):
            kwargs['autoescape'] = environment.autoescape
            return conversion_wrapper(*args, **kwargs)
        return autoescape_wrapper
    else:
        return conversion_wrapper


@register.filter
def floatformat(value, arg=-1):
    """Builds on top of Django's own version, but adds strict error
    checking, staying with the philosophy.
    """
    from django.template.defaultfilters import floatformat
    arg = int(arg)  # raise exception
    result = django_filter_to_jinja2(floatformat)(value, arg)
    if result == '':  # django couldn't handle the value
        raise ValueError(value)
    return result

@register.filter
def jsencode (value):
    import urllib
    value = 'document.write("%s")' % value
    encoded = urllib.quote(unicode(value).encode('utf-8'))
    return '<script>eval(decodeURIComponent("%s"));</script>'% encoded

from djinja.template.base import import_library
django_filters = import_library('django.template.defaultfilters').filters
for _filter in django_filters.keys():
    register.filter(django_filter_to_jinja2(django_filters[_filter]),name=_filter)