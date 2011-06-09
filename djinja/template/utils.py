from django.template.base import *
from django.template.defaulttags import *
from django.templatetags.i18n import TranslateNode, BlockTranslateNode
from django.template.loader_tags import ExtendsNode,IncludeNode,ConstantIncludeNode,BlockNode

#l = Library()
#l.simple_tag(lambda x:x)
#SimpleNode = (l.tags['<lambda>'].func_closure[0].cell_contents[3])
#
#del l
#print SimpleNode
class DjinjaAdapterException(Exception):
    pass
class DjinjaAdapter:
    def __init__ (self,template):
        self.template = template
        
    def process (self):
        return self.convert_node(self.template.nodelist)
    
    def convert_expression (self,expr):
        from django.utils.safestring import SafeString,SafeUnicode
        expr_type = type(expr)
        if expr_type in (SafeString, SafeUnicode, unicode): return '"'+expr.replace('"','\\"')+'"'
        elif type(expr) is Variable:
            if expr.literal is not None: return "'"+str(expr.literal).replace('"','\\"')+'"'
            return expr.var.replace('forloop.','loop.')
        #'"'+str(expr.literal).replace('"','\\"')+'"'
        filters = [self.convert_expression(expr.var)]
        for filter in expr.filters:
            name= filter[0].func_name
            args = filter[1]
            filters.append( str(name)+'('+', '.join(map(lambda x:self.convert_expression(x[1]),args))+')')
        return '|'.join(filters)
    
    def jinja_block (self,tag):
        return '{% '+tag+' %}'
    
    def jinja_var (self,var):
        return '{{ '+var+' }}'
    
    def convert_for_node (self,node):
        return self.jinja_block("for %s in %s" % (', '.join(node.loopvars), node.sequence)) +\
            self.convert_node(node.nodelist_loop) +\
            ((self.jinja_block("else")+self.convert_node(node.nodelist_empty)) if node.nodelist_empty else '') +\
            self.jinja_block("endfor")
            
    def convert_text_node (self,node):
        return node.s
    
    def convert_variable_node (self,node):
        return self.jinja_var(self.convert_expression(node.filter_expression))
    
    def convert_extends_node (self,node):
        parent_name = node.parent_name_expr if node.parent_name_expr else node.parent_name
        return self.jinja_block("extends %s" % self.convert_expression(parent_name)) + self.convert_node(node.nodelist)
    
    def convert_trans_node (self,node):
        return self.jinja_var("_(%s)" % self.convert_expression(node.filter_expression))
    
    def convert_tokens (self,tokens):
        from django.template import TOKEN_TEXT, TOKEN_VAR
        result = []
        for token in tokens:
            if token.token_type == TOKEN_TEXT:
                result.append(token.contents)
            elif token.token_type == TOKEN_VAR:
                result.append(self.jinja_var("%s" % token.contents))
        return ''.join(result)
    
    def convert_blocktrans_node (self,node):
        extra = node.extra_context
        if node.countervar:
            extra[node.countervar] = node.counter
        vars = ', '.join([str(key)+'='+self.convert_expression(value) for key,value in extra.iteritems()])
        return self.jinja_block("trans %s"%vars) +\
            self.convert_tokens(node.singular) +\
            (self.jinja_block("pluralize %s"% (node.countervar if node.countervar else ''))+self.convert_tokens(node.plural) if node.plural else '' ) +\
            self.jinja_block("endtrans")
            
    def get_source (self,node):
        init, final = node.source[1]
        return node.source[0].source[init:final]

    def convert_load_node (self,node):
        source = self.get_source(node)
        return source
    
    def convert_block_node (self,node):
        return self.jinja_block("block %s"%self.convert_expression(node.name)) +\
            self.convert_node(node.nodelist) +\
            self.jinja_block("endblock")
            
    def convert_filter_node (self,node):
        return self.jinja_block("filter %s"%node.filter_expr.filters[0][0].func_name) +\
            self.convert_node(node.nodelist) +\
            self.jinja_block("endfilter")
            
    def convert_autoescape_node (self,node):
        return self.jinja_block("autoescape %s"% ('true' if node.setting else 'false')) +\
            self.convert_node(node.nodelist) +\
            self.jinja_block("endautoescape")
            
    def jinja_set (self,vars):
        return self.jinja_block("set %s=%s"% (', '.join(vars.keys()),', '.join([str(value) for value in vars.values()])))
    
    def convert_cycle_node (self,node):
        vars = ' ,'.join([self.convert_expression(e) for e in node.cyclevars])
        loop_cycle = 'loop.cycle(%s)' % vars
        if node.silent:
            if node.cyclevars:
                return self.jinja_set({node.variable_name:loop_cycle})
            else:
                return ''
#        if node.variable_name:
#            set = '{ set %s=%s}'%(node.variable_name,vars)
#            vars = node.variable_name
#        else:
#            set = None
#        return "%s{ loop.cycle(%s) }" % (set,vars)
        return self.jinja_var(loop_cycle)

    def convert_ifequal_node (self,node):
        return self.jinja_block("if %s==%s"% (node.var1,node.var2)) +\
            self.convert_node(node.nodelist_true) +\
            ((self.jinja_block("else") +self.convert_node(node.nodelist_false)) if node.nodelist_false else '') +\
            self.jinja_block("endif")
            
    def convert_operator (self,operator):
        if not hasattr(operator,'id'): return None
        if operator.id != 'literal':
            scnd = self.convert_operator(operator.second)
            fst = self.convert_operator(operator.first)
            if fst and scnd: return '%s %s %s' % (fst, operator.id,scnd)
            else: return '%s %s' % (operator.id,fst)
        else:
            return self.convert_expression(operator.value)
        
    def convert_args (self,args):
        ', '.join([self.convert_expression(e) for e in args])
        
    def convert_if_node (self,node):
        return self.jinja_block("if %s"% self.convert_operator(node.var)) +\
            self.convert_node(node.nodelist_true) +\
            ((self.jinja_block("else") +self.convert_node(node.nodelist_false)) if node.nodelist_false else '') +\
            self.jinja_block("endif")
            
    def convert_firstof_node (self,node):
        return self.jinja_var("(%s)|firstof" % ', '.join([self.convert_expression(e) for e in node.vars]))
    
    def convert_constantinclude_node (self,node):
       return (self.jinja_set(node.extra_context) if node.extra_context else '') +\
           self.jinja_block("include %s"%node.template.name)
           
    def convert_regroup_node (self,node):
        variable = node.target.var
        return self.jinja_set({node.var_name:'%s|regroup(by=%s)'% (node.target,self.convert_expression(node.expression))})
    
    def convert_url_node (self,node):
        vars = ', '.join([self.convert_expression(node.view_name)]+[self.convert_expression(arg) for arg in node.args]+[str(key)+'='+self.convert_expression(value) for key,value in node.kwargs.iteritems()])
        url = 'url(%s)' % vars
        return self.jinja_set({node.asvar:url}) if node.asvar else self.jinja_var(url)
    
    def convert_templatetag_node (self,node):
        return str(node.vars_to_resolve)
    
    def convert_node(self,node):
        node_type = type(node)
        if isinstance(node, TextNode):
            return self.convert_text_node(node)
        elif isinstance(node, NodeList):
            return ''.join([self.convert_node(n) for n in node])
        elif isinstance(node, ForNode):
            return self.convert_for_node(node)
        elif isinstance(node, ExtendsNode):
            return self.convert_extends_node(node)
        elif isinstance(node, IncludeNode):
            return self.convert_include_node(node)
        elif isinstance(node, ConstantIncludeNode):
            return self.convert_constantinclude_node(node)
        elif isinstance(node, VariableNode):
            return self.convert_variable_node(node)
        elif isinstance(node, LoadNode):
            return self.convert_load_node(node)
        elif isinstance(node, URLNode):
            return self.convert_url_node(node)
        elif isinstance(node, BlockNode):
            return self.convert_block_node(node)
        elif isinstance(node, FilterNode):
            return self.convert_filter_node(node)
        elif isinstance(node, TranslateNode):
            return self.convert_trans_node(node)
        elif isinstance(node, BlockTranslateNode):
            return self.convert_blocktrans_node(node)
        elif isinstance(node, IfNode):
            return self.convert_if_node(node)
        elif isinstance(node, IfEqualNode):
            return self.convert_ifequal_node(node)
        elif isinstance(node, AutoEscapeControlNode):
            return self.convert_autoescape_node(node)
        elif isinstance(node, FirstOfNode):
            return self.convert_firstof_node(node)
        elif isinstance(node, CycleNode):
            return self.convert_cycle_node(node)
        elif isinstance(node, RegroupNode):
            return self.convert_regroup_node(node)
        else:
            return self.convert_templatetag_node(node)
#            raise DjinjaAdapterException("Node not supported: %s ('%s')"%(node,self.get_source(node)))

