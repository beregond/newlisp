import sys
from ply import lex, yacc

from parser import *


lex.lex()
yacc.yacc()

filename = sys.argv[-1]

with open(filename) as source:
    codebase = source.read()
    result = yacc.parse(codebase)
    if result:
        result.execute()
