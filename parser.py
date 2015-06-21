from expressions import *
from exc import *

reserved = (
    'print', 'let', 'defun', 'len', 'if', 'val', 'zero', 'first', 'rest',
    'empty', 'defexc', 'raise', 'try', 'except')

tokens = reserved + (
    "id", "iconst", "fconst", "sconst", "cconst",
    "apostrophe",
    "comma",
    'plus', 'minus', 'times', 'divide', 'mod',
    'lt', 'le', 'gt', 'ge', 'eq', 'ne',
    "lparen", "rparen")

t_iconst = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
t_cconst = r'(L)?\'([^\\\n]|(\\.))*?\''
t_fconst = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
t_sconst = r'\"([^\\\n]|(\\.))*?\"'

t_apostrophe = r"\'"
t_print = 'print'
t_let = 'let'
t_defun = 'defun'
t_len = 'len'
t_if = 'if'
t_val = 'val'
t_zero = 'zero'
t_first = 'first'
t_rest = 'rest'
t_empty = 'empty'
t_defexc = 'defexc'
t_raise = 'raise'
t_try = 'try'
t_except = 'except'

t_lparen           = r'\('
t_rparen           = r'\)'
t_comma            = r','

t_plus             = r'\+'
t_minus            = r'-'
t_times            = r'\*'
t_divide           = r'/'
t_mod              = r'%'

t_lt               = r'<'
t_gt               = r'>'
t_le               = r'<='
t_ge               = r'>='
t_eq               = r'=='
t_ne               = r'!='

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r


def t_space(t):
    r'\ +'
    pass


def t_newline(t):
    r'\n+'
    t.lineno += t.value.count("\n")


def t_id(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "id")
    return t

def t_error(t):
    print t


def p_error(p):
    print p


def p_expr_list_2(p):
    r'''expr_list : expr_list expr'''
    p[0] = p[1] + [p[2]]


def p_expr_list(p):
    r'''expr_list : expr'''
    p[0] = Expressions(p[1])


def p_expr(p):
    r'''expr : print_expr
             | let_expr
             | function_definition
             | function_call
             | calculation
             | len_expr
             | comparison
             | conditional
             | val_expr
             | first_expr
             | rest_expr
             | exception_definition
             | raise_exception
             | try_except'''
    p[0] = p[1]


def p_try_except(p):
    r'''try_except : lparen try lparen expr_list rparen except id lparen expr_list rparen rparen'''
    p[0] = TryExcept(p[4], p[7], p[9])


def p_raise(p):
    r'''raise_exception : lparen raise id rparen'''
    p[0] = RaiseExpression(p[3])


def p_raise_2(p):
    r'''raise_exception : lparen raise id value rparen'''
    p[0] = RaiseExpression(p[3], p[4])


def p_exc_def(p):
    r'''exception_definition : lparen defexc id rparen'''
    p[0] = ExceptionDefinition(p[3])


def p_rest_expr(p):
    r'''rest_expr : lparen rest value rparen'''
    p[0] = RestExpr(p[3])


def p_first_expr(p):
    r'''first_expr : lparen first value rparen'''
    p[0] = FirstExpr(p[3])


def p_val_expr(p):
    r'''val_expr : lparen val value rparen'''
    p[0] = ValueExpression(p[3])


def p_if_expr(p):
    r'''conditional : lparen if comparison expr rparen'''
    p[0] = Conditional(p[3], Expressions(p[4]))


def p_if_expr_2(p):
    r'''conditional : lparen if comparison lparen expr_list rparen rparen'''
    p[0] = Conditional(p[3], p[5])


def p_if_expr_3(p):
    r'''conditional : lparen if comparison expr expr rparen'''
    p[0] = Conditional(p[3], Expressions(p[4]), Expressions(p[5]))


def p_if_expr_4(p):
    r'''conditional : lparen if comparison lparen expr_list rparen expr rparen'''
    p[0] = Conditional(p[3], p[5], Expressions(p[7]))


def p_if_expr_5(p):
    r'''conditional : lparen if comparison expr lparen expr_list rparen rparen'''
    p[0] = Conditional(p[3], Expressions(p[4]), p[6])


def p_comparison(p):
    r'''comparison : lparen value comparison_operator value rparen'''
    p[0] = Comparison(p[2], p[3], p[4])


def p_zero_comparison(p):
    r'''comparison : lparen zero value rparen'''
    p[0] = ZeroComparison(p[3])


def p_empty_comparison(p):
    r'''comparison : lparen empty value rparen'''
    p[0] = EmptyComparison(p[3])


def p_len_expr(p):
    r'''len_expr : lparen len value rparen'''
    p[0] = LenExpression(p[3])


def p_calculation(p):
    r'''calculation : lparen operator function_call_args rparen'''
    p[0] = Calculation(p[2], p[3])


def p_function_call(p):
    r'''function_call : lparen id lparen rparen rparen'''
    p[0] = FunctionCall(p[2])


def p_function_call_2(p):
    r'''function_call : lparen id lparen function_call_args rparen rparen'''
    p[0] = FunctionCall(p[2], p[4])


def p_function_call_args(p):
    r'''function_call_args : function_call_arg'''
    p[0] = [p[1]]


def p_function_call_args_2(p):
    r'''function_call_args : function_call_args comma function_call_arg'''
    p[0] = p[1] + [p[3]]


def p_function_call_arg(p):
    r'''function_call_arg : value'''
    p[0] = p[1]


def p_defun_expr(p):
    r'''function_definition : lparen defun id function_args_def expr_list rparen'''
    p[0] = FunctionDefinition(p[3], p[4], p[5])


def p_function_args_def(p):
    r'''function_args_def : lparen function_args rparen'''
    p[0] = p[2]


def p_function_args_def_2(p):
    r'''function_args_def : lparen rparen'''
    p[0] = []


def p_func_args(p):
    r'''function_args : function_args comma function_arg'''
    p[0] = p[1] + [p[3]]


def p_func_args_2(p):
    r'''function_args : function_arg'''
    p[0] = [p[1]]


def p_func_arg(p):
    r'''function_arg : id'''
    p[0] = p[1]


def p_print_expr(p):
    r'''print_expr : lparen print value rparen'''
    p[0] = PrintExpression(p[3])


def p_let_expr(p):
    r'''let_expr : lparen let id value rparen'''
    p[0] = LetExpession(p[3], p[4])


def p_value(p):
    r'''
        value : primitive
        value : list
        value : expr
    '''
    p[0] = p[1]


def p_id_value(p):
    r'''
        value : id
    '''
    p[0] = Id(p[1])


def p_value_list(p):
    r'''list : apostrophe lparen list_args rparen'''
    p[0] = p[3]


def p_value_list_2(p):
    r'''list : apostrophe lparen rparen'''
    p[0] = []


def p_list_args_2(p):
    r'''list_args : list_args comma list_arg'''
    p[0] = p[1] + [p[3]]


def p_list_args(p):
    r'''list_args : list_arg'''
    p[0] = [p[1]]

def p_list_arg(p):
    r'''list_arg : value'''
    p[0] = p[1]


def p_int_value(p):
    r'''primitive : iconst'''
    p[0] = int(p[1])


def p_float_value(p):
    r'''primitive : fconst'''
    p[0] = float(p[1])


def p_char_value(p):
    r'''primitive : cconst'''
    p[0] = str(p[1]).strip("'")


def p_string_value(p):
    r'''primitive : sconst'''
    p[0] = str(p[1]).strip('"')


def p_comparison_operator(p):
    r'''comparison_operator : lt
                            | gt
                            | le
                            | ge
                            | eq
                            | ne'''
    p[0] = p[1]


def p_operator(p):
    r'''operator : plus
                 | minus
                 | times
                 | divide
                 | mod'''
    p[0] = p[1]
