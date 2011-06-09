from jinja2.ext import Extension
class haml(Extension):
    def __init__(self, environment):
        super(haml, self).__init__(environment)

        environment.extend(
            hamlish_mode='compact',
            hamlish_file_extensions=('.haml',),
            hamlish_indent_string='    ',
            hamlish_newline_string='\n',
            hamlish_debug=False,
            hamlish_enable_div_shortcut=False,
        )


    def preprocess(self, source, name, filename=None):
        import os
        if not os.path.splitext(name)[1] in \
            self.environment.hamlish_file_extensions:
            return source
        from extended import haml as _haml
        c = _haml.Compiler()
        return c.process(source)
