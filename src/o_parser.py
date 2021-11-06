from sly import Parser
from o_lexer import OLexer


class OParser(Parser):
    """
    Parser for the Darija Language
    """
    tokens = OLexer.tokens

    precedence = (
        ('right', PLUSASGN, MINUSASGN, STARASGN, SLASHASGN,
         MODULOASGN),
        ('left', OR),
        ('left', AND),
        ('left', '|'),
        ('left', '^'),
        ('left', '&'),
        ('left', EQEQ, NOTEQ),
        ('left', LESS, LESSEQ, GREATER, GREATEREQ),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS', 'UPLUS', INC, DEC),
        ('right', '!'),
    )

    @_('statements')
    def program(self, p):
        return p.statements

    @_('empty')
    def program(self, p):
        return ()

    @_('statement')
    def statements(self, p):
        return (p.statement,)

    @_('statements statement')
    def statements(self, p):
        return p.statements + (p.statement,)

    @_('function_definition')
    def statement(self, p):
        return p.function_definition

    @_('return_statement')
    def statement(self, p):
        return p.return_statement

    @_('while_statement')
    def statement(self, p):
        return p.while_statement

    @_('for_statement')
    def statement(self, p):
        return p.for_statement

    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('var_define SEP')
    def statement(self, p):
        return p.var_define

################################################

    @_('INT_TYPE')
    def var_type(self, p):
        return 'sa7i7'

    @_('FLOAT_TYPE')
    def var_type(self, p):
        return '_3achari'

    @_('STRING_TYPE')
    def var_type(self, p):
        return 'klma'

    @_('BOOL_TYPE')
    def var_type(self, p):
        return 'mnte9i'

#################################################################

    @_('FN ID "(" params ")" block')
    def function_definition(self, p):
        return ('dalla', p.ID, ('params', p.params), ('block', p.block))

    @_('LET var ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.var, p.expr)

    @_('LET var ":" var_type SEP')
    def statement(self, p):
        return ('var_define_no_expr', p.var, p.var_type)

    @_('RETURN expr SEP')
    def return_statement(self, p):
        return ('rj3', p.expr)

##################################################################

    @_('var_assign SEP')
    def statement(self, p):
        return p.var_assign

    @_('var ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, p.expr)

    @_('var PLUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), p.expr))

    @_('var MINUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), p.expr))

    @_('var STARASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('*', ('var', p.var), p.expr))

    @_('var SLASHASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('/', ('var', p.var), p.expr))

    @_('var MODULOASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('%', ('var', p.var), p.expr))

#####################################################################################3

    @_('IF expr block ELSE block')
    def if_statement(self, p):
        return ('ila', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IF expr block')
    def if_statement(self, p):
        return ('ila', ('condition', p.expr), ('block', p.block), None)

    @_('WHILE expr block')
    def while_statement(self, p):
        return ('ma7d', ('condition', p.expr), ('block', p.block))

    @_('FOR var_assign SEP expr SEP var_assign block')
    def for_statement(self, p):
        return (p.var_assign0, ('ma7d', ('condition', p.expr), ('block', p.block + (p.var_assign1,)))) #p[0]=tuple

    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('?:', p.expr0, p.expr1, p.expr2)

    @_('ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))

#########################################################################

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('==', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ('!=', p.expr0, p.expr1)

    @_('expr LESSEQ expr')
    def expr(self, p):
        return ('<=', p.expr0, p.expr1)

    @_('expr GREATEREQ expr')
    def expr(self, p):
        return ('>=', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('w', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ('wla', p.expr0, p.expr1)

    @_('expr LESS expr')
    def expr(self, p):
        return ('<', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def expr(self, p):
        return ('>', p.expr0, p.expr1)

    @_('expr "&" expr')
    def expr(self, p):
        return ('&', p.expr0, p.expr1)

    @_('expr "^" expr')
    def expr(self, p):
        return ('^', p.expr0, p.expr1)

    @_('expr "|" expr')
    def expr(self, p):
        return ('|', p.expr0, p.expr1)

    @_('expr SEP')
    def statement(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('neg', p.expr)

    @_('"+" expr %prec UPLUS')
    def expr(self, p):
        return p.expr

    @_('"!" expr')
    def expr(self, p):
        return ('!', p.expr)

    @_('INC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), 1))

    @_('DEC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), 1))

    @_('expr "+" expr')
    def expr(self, p):
        return ('+', p.expr0, p.expr1)
            #'+', ('var', p.var), 1
            #expr0+expr1
            #p.var+1

    @_('expr "-" expr')
    def expr(self, p):
        return ('-', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('*', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('/', p.expr0, p.expr1)

    @_('expr "%" expr')
    def expr(self, p):
        return ('%', p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('INT') #terminal
    def expr(self, p):
        return p.INT

    @_('FLOAT') #terminal
    def expr(self, p):
        return p.FLOAT

    @_('STRING') #terminal
    def expr(self, p):
        return p.STRING

    @_('TRUE') #terminal
    def expr(self, p):
        return True

    @_('FALSE') #terminal
    def expr(self, p):
        return False

    @_('var') #terminal
    def expr(self, p):
        return ('var', p.var)

    @_('ID') #terminal
    def var(self, p):
        return p.ID

    @_('') #terminal
    def empty(self, p):
        pass

    @_('"{" program "}"')
    def block(self, p):
        return p.program

    @_('statement')
    def block(self, p):
        return (p.statement,)

    @_('params "," param')
    def params(self, p):
        return p.params + [p.param]

    @_('param') #terminal
    def params(self, p):
        return [p.param]

    @_('empty')
    def params(self, p):
        return []

    @_('ID ":" var_type')
    def param(self, p):
        return (p.ID, p.var_type)

    @_('args "," arg')
    def args(self, p):
        return p.args + [p.arg]

    @_('arg')
    def args(self, p):
        return [p.arg]

    @_('empty')
    def args(self, p):
        return []

    @_('expr')
    def arg(self, p):
        return p.expr

    debugfile = 'parser.out' #generer le fichier de grammaire
