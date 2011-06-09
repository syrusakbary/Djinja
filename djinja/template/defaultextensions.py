from djinja.template.base import Library
from jinja2.ext import Extension
import traceback
from django.utils.safestring import mark_safe
from jinja2 import nodes

register = Library()

class CsrfExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['csrf_token'])

    def __init__(self, environment):
        self.environment = environment

    def parse(self, parser):
        try:
            token = parser.stream.next()
            return nodes.Output([self.call_method('_render', [nodes.Name('csrf_token','load')])]).set_lineno(token.lineno)

        except:
            traceback.print_exc()

    def _render(self, csrf_token):
        """Helper callback."""
        if csrf_token:
            if csrf_token == 'NOTPROVIDED':
                return mark_safe(u"")
            else:
                return mark_safe(u"<div style='display:none'><input type='hidden' name='csrfmiddlewaretoken' value='%s' /></div>" % (csrf_token))
        else:
            # It's very probable that the token is missing because of
            # misconfiguration, so we raise a warning
            from django.conf import settings
            if settings.DEBUG:
                import warnings
                warnings.warn("A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.")
            return u''

register.extension(CsrfExtension)

class SpacelessExtension(Extension):
    """Removes whitespace between HTML tags, including tab and
    newline characters.

    Works exactly like Django's own tag.
    """

    tags = set(['spaceless'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(['name:endspaceless'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method('_strip_spaces', [], [], None, None),
            [], [], body
        ).set_lineno(lineno)

    def _strip_spaces(self, caller=None):
        from django.utils.html import strip_spaces_between_tags
        return strip_spaces_between_tags(caller().strip())

register.extension(SpacelessExtension)
        
class LoadExtension(Extension):
    """Changes auto escape rules for a scope."""
    tags = set(['load'])

    def parse(self, parser):
        node = nodes.ExprStmt(lineno=next(parser.stream).lineno)
        modules = []
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if modules:
                parser.stream.expect('comma')
            expr = parser.parse_expression()
            module = expr.as_const()
            modules.append(module)

        assignments = []
        from djinja.template.defaultfunctions import Load
        for m in modules:
            target = nodes.Name(m,'store')
            func = nodes.Call(nodes.Name('load', 'load'), [nodes.Const(m)],
                              [], None, None)
            assignments.append(nodes.Assign(target, func, lineno=lineno))
                
            for i in Load(m).globals.keys():
                target = nodes.Name(i,'store')
                f = nodes.Getattr(nodes.Name(m,'load'), i, 'load')
            
                assignments.append(nodes.Assign(target, f, lineno=lineno))

        return assignments
register.extension(LoadExtension)


