from sly import Lexer

class OLexer(Lexer):
    """
    Darija language Lexer
    """
    tokens = {ID, INT, FLOAT, ASSIGN, STRING, LET,
              IF, ELSE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, WHILE,
              FOR, FN, RETURN, TRUE, FALSE,
              AND, OR, INC, DEC, PLUSASGN,
              MINUSASGN, STARASGN, SLASHASGN, MODULOASGN,
              INT_TYPE, FLOAT_TYPE, BOOL_TYPE,
              STRING_TYPE}
    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    #Literals are checked after all of the defined regular expression rules
    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':',
                '.'} #terminaux

    INC = r'\+\+'
    DEC = r'--'
    PLUSASGN = r'\+='
    MINUSASGN = r'-='
    STARASGN = r'\*='
    SLASHASGN = r'/='
    MODULOASGN = r'%='
    LESSEQ = r'<='
    GREATEREQ = r'>='
    LESS = r'<'
    GREATER = r'>'
    NOTEQ = r'!='
    EQEQ = r'=='
    ASSIGN = r'='
    SEP = r';'

    # mots reserves: terminaux
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['mtghyr'] = LET
    ID['ila'] = IF
    ID['w_ilala'] = ELSE
    ID['ma7d'] = WHILE
    ID['lkol'] = FOR
    ID['dalla'] = FN
    ID['rj3'] = RETURN
    ID['s7i7'] = TRUE
    ID['ghalet'] = FALSE
    ID['w'] = AND
    ID['wla'] = OR
    ID['sa7i7'] = INT_TYPE
    ID['_3achari'] = FLOAT_TYPE
    ID['klma'] = STRING_TYPE
    ID['mnte9i'] = BOOL_TYPE


    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("kayn ghalat '%s' f had str %d" % (t.value[0], self.lineno))
        self.index += 1