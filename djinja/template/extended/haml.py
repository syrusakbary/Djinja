from hamlpy.nodes import *
from hamlpy import hamlpy
def create_node(haml_line):
    stripped_line = haml_line.strip()
    
    if not stripped_line:
        return None
        
    if stripped_line[0] == HAML_ESCAPE:
        return HamlNode(haml_line.replace(HAML_ESCAPE, '', 1))
        
    if stripped_line[0] in ELEMENT_CHARACTERS:
        return ElementNode(haml_line)
    
    if stripped_line[0] == HTML_COMMENT:
        return CommentNode(haml_line)
    
    if stripped_line.startswith(HAML_COMMENT):
        return HamlCommentNode(haml_line)
    
    if stripped_line[0] == VARIABLE:
        return VariableNode(haml_line)
    
    if stripped_line[0] == TAG:
        return JinjaTagNode(haml_line)
    
    if stripped_line == JAVASCRIPT_FILTER:
        return JavascriptFilterNode(haml_line)
    
    if stripped_line == CSS_FILTER:
        return CssFilterNode(haml_line)
    
    if stripped_line == PLAIN_FILTER:
        return PlainFilterNode(haml_line)
    
    return HamlNode(haml_line)

class JinjaTagNode(TagNode):
    self_closing = {'for':'endfor',
                    'if':'endif',
                    'block':'endblock',
                    'filter':'endfilter',
                    'autoescape':'endautoescape',
                    'with':'endwith',
                    'macro':'endmacro',
                    'call':'endcall',
                    'trans':'endtrans'
    }
    may_contain = {'if':['else','elif'], 'for':['empty'], 'with':['with'],'trans':['pluralize']}
    def should_contain(self, node):
        return isinstance(node,TagNode) and node.tag_name in self.may_contain.get(self.tag_name,[])

class Compiler(hamlpy.Compiler):
    def process_lines(self, haml_lines):
        root = RootNode()
        for line in haml_lines:
            haml_node = create_node(line)
            root.add_node(haml_node)
        return root.render()