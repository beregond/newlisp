from exc import *

built_in_exceptions = {
    'COMP_ERR': 'computation_error'
}


def get_exc(name):
    return built_in_exceptions[name]


class Environment(object):

    def __init__(self, parent_env=None):
        self.env = {}
        self.parent_env = parent_env

    def __setitem__(self, key, value):
        self.env[key] = value

    def __getitem__(self, key):
        try:
            return self.env[key]
        except KeyError:
            if self.parent_env:
                return self.parent_env[key]
            else:
                raise


class Id(object):

    def __init__(self, name):
        self.name = name

    def execute(self, env):
        return env[self.name]


class LetExpession(object):

    def __init__(self, id_, value):
        self.id_ = id_
        self.value = value

    def execute(self, env):
        value = evaluate_in_env([self.value], env)[0]
        env[self.id_] = value


class PrintExpression(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        try:
            self.value.execute
        except AttributeError:
            print self.value
        else:
            print self.value.execute(env)


class Expressions(object):

    def __init__(self, expr):
        self._expressions = [expr]

    def __add__(self, expressions):
        self._expressions += expressions
        return self

    def execute(self, env=None):
        env = env or Environment()
        for expr in self._expressions:
            ret_val = expr.execute(env)
        return ret_val


class FunctionDefinition(object):

    def __init__(self, name, args, expressions):
        self.name = name
        self.args = args
        self.expressions = expressions

    def execute(self, env):
        env[self.name] = self

    def call(self, env, call_args):
        if len(self.args) != len(call_args):
            raise RuntimeError('Give proper number of arguments!')
        call_args = evaluate_in_env(call_args, env)
        variables = dict(zip(self.args, call_args))
        call_env = Environment(env)
        for name, variable in variables.items():
            call_env[name] = variable
        return self.expressions.execute(call_env)


def evaluate_in_env(args, env):

    result = []
    for arg in args:
        try:
            arg.execute
        except AttributeError:
            value = arg
        else:
            value = arg.execute(env)

        if isinstance(value, list):
            value = evaluate_in_env(value, env)
        result.append(value)

    return result


class FunctionCall(object):

    def __init__(self, name, call_args=[]):
        self.name = name
        self.call_args = call_args

    def execute(self, env):
        function = env[self.name]
        if not isinstance(function, FunctionDefinition):
            raise RuntimeError('"{}" is not callable.'.format(self.name))
        return function.call(env, self.call_args)


class Calculation(object):

    functions = {
        '%': lambda x, y: x % y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
    }

    def __init__(self, operator, call_args):
        if len(call_args) != 2:
            raise RuntimeError("You must give exactly 2 arguments!")
        self.operator = operator
        self.call_args = call_args

    def execute(self, env):
        func = self.functions[self.operator]
        call_args = evaluate_in_env(self.call_args, env)
        try:
            return func(*call_args)
        except TypeError:
            raise ProgramException(get_exc('COMP_ERR'),
                                   'wrong argument types')


class LenExpression(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        value = evaluate_in_env([self.value], env)[0]
        if not isinstance(value, list):
            raise RuntimeError("Given value must be instance of list!")
        return len(value)


class Comparison(object):

    functions = {
        '<': lambda x, y: x < y,
        '>': lambda x, y: x > y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
    }

    def __init__(self, value1, operator, value2):
        self.value1 = value1
        self.value2 = value2
        self.operator = operator

    def execute(self, env):
        values = evaluate_in_env([self.value1, self.value2], env)
        func = self.functions[self.operator]
        return func(*values)


class Conditional(object):

    def __init__(self, conditional, success_expr, fail_expr=None):
        self.conditional = conditional
        self.success_expressions = success_expr
        self.failure_expressions = fail_expr

    def execute(self, env):
        if self.conditional.execute(env):
            return self.success_expressions.execute(env)
        elif self.failure_expressions:
            return self.failure_expressions.execute(env)


class ValueExpression(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        return evaluate_in_env([self.value], env)[0]


class ZeroComparison(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        return evaluate_in_env([self.value], env)[0] == 0


class EmptyComparison(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        value = evaluate_in_env([self.value], env)[0]
        if not isinstance(value, list):
            raise RuntimeError('Only lists are allowed!')
        return len(value) == 0


class FirstExpr(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        value = evaluate_in_env([self.value], env)[0]
        if not isinstance(value, list):
            raise RuntimeError('Only lists are allowed!')
        return value[0]


class RestExpr(object):

    def __init__(self, value):
        self.value = value

    def execute(self, env):
        value = evaluate_in_env([self.value], env)[0]
        if not isinstance(value, list):
            raise RuntimeError('Only lists are allowed!')
        return value[1:]


class RaiseExpression(object):

    def __init__(self, type, message=None):
        self.type = type
        self.message = message

    def execute(self, env):
        try:
            exc = env[self.type]
        except KeyError:
            exc = self.type

        conditions = [
            not isinstance(exc, ExceptionDefinition),
            exc not in built_in_exceptions.values(),
        ]

        if all(conditions):
            raise RuntimeError('Wrong exception id!', self.type)

        raise ProgramException(self.type, self.message)


class TryExcept(object):

    def __init__(self, expr_list, exc_type, exc_expr_list):
        self.expr_list = expr_list
        self.exc_type = exc_type
        self.exc_expr_list = exc_expr_list

    def execute(self, env):
        try:
            return self.expr_list.execute(env)
        except ProgramException as exc:
            if exc.type != self.exc_type:
                raise
            return self.exc_expr_list.execute(env)
