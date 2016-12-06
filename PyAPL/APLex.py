import ply.lex as lex
from PyAPL.__init__ import apl
import numpy as np
from collections import namedtuple
APLobj = namedtuple('Data', 'value, shape')

class APLexer(object):

    # List of token names
    tokens = (
        'NUMBERLIT',
        'LPAREN',
        'RPAREN',
        'LBRACK',
        'RBRACK',
        'PRIMFUNC',
        'ASSIGN',
        'VECTORLIT',
        'FUNCARG',
        'NAME'
    )

    # Regular expression rules for simple tokens
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACK  = r'\{'
    t_RBRACK  = r'\}'
    t_PRIMFUNC = r'[\+\-×÷*⍟⌊⌈\|\!○<≤\=>≥≠∧∨⍲⍱~\?⍴⍳∊↑↓⍪⍋⍒⌽⍉⊖∪⊃⊂∩⍎⍕⌷⊣⊢≡≢¤\$\/\\⌿⍀]'
    t_ASSIGN = r'←'
    t_FUNCARG = r'[⍺⍵]'
    t_NAME = r'\w+'

    def t_VECTORLIT(self,t):     # Matches vector literals (i.e. '234 23 11')
        r'[\d\.¯]+([^\S\n]+[\d\.¯]+)+'
        t.value = list(map(float, t.value.replace('¯','-').split(' ')))  # Turn it into a list of the numbers
        t.value = np.array(t.value)  # Turn it into an array
        return t

    # A regular expression rule with some action code
    def t_NUMBERLIT(self,t):
        r'[\d\.¯]+'
        t.value = t.value.replace('¯','-')
        t.value = float(t.value)
        t.value = np.array([t.value])
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


    def inp(self, data):
        self.lexer.input(data)
        returndat = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            returndat.append(tok)
        return returndat

# m = APLexer()
# m.build()  # Build the lexer
# print(m.inp("3 4 2 + 1442"))
# print(m.inp("avg←{(+⌿⍵)÷≢⍵}"))