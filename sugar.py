"""Python 3 functional programing experiments."""


import itertools
import inspect
import opcode
import types


__all__ = ["Let", "Do", "OTHERWISE", "Expression", "Raise"]


def _make_closure_cell(val):
    """a nested function just for creating a closure"""
    def nested():
        return val
    return nested.__closure__[0]


def _change_op_code(i, op_code, constant_code, old_names, constants, new_code,
                    new_names, new_consts):
    # NOTE: remember that list are mutable
    assert type(new_code) is list
    assert type(new_names) is list
    assert type(new_consts) is list

    if op_code == opcode.opmap[constant_code]:
        oparg = new_code[i + 1] + (new_code[i + 2] << 8)
        # can't use the new_name variable directly because if I clean the
        # name i get an IndexError.
        name = old_names[oparg]
        if name in constants:
            value = constants[name]
            # pos is the position of the new const
            for pos, v in enumerate(new_consts):
                if v is value:
                    # do nothing  if the value is already stored
                    break
            # add the value to new_consts if such value not exists
            else:
                pos = len(new_consts)
                new_consts.append(value)
                if constant_code == 'LOAD_DEREF':
                    new_names.remove(name)
            new_code[i] = opcode.opmap['LOAD_CONST']
            new_code[i + 1] = pos & 0xFF
            new_code[i + 2] = pos >> 8


def _inject_constants(function, constants):
    """Return a copy of of the `function` parameter. This copy have
    the constants defined in the `constants` map. If a key of
    `constants` share the same name than a global or local object,
    then replace such global or local by the value defined in the
    `constants` argument."""
    # NOTE: all vars with the *new_* name prefix are custom versions of
    # the original attributes of the function.
    old_code = function.__code__
    # store in list because I need to mutate them
    new_code = list(old_code.co_code)
    new_consts = list(old_code.co_consts)
    new_freevars = list(old_code.co_freevars)
    new_names = list(old_code.co_names)

    i = 0
    # through the list of instructions
    while i < len(new_code):
        op_code = new_code[i]
        # Replace global lookups by the values defined in *constants*.
        # The names of all global variables are stored in old_code.co_names
        _change_op_code(i, op_code, 'LOAD_GLOBAL', old_code.co_names,
                        constants, new_code, [], new_consts)

        # Replace local lookups by the values defined in *constants*.
        # The names of all local variables are stored in old_code.co_freevars
        _change_op_code(i, op_code, 'LOAD_DEREF', old_code.co_freevars,
                        constants, new_code, new_freevars, new_consts)

        i += 1
        if op_code >= opcode.HAVE_ARGUMENT:
            i += 2

    # NOTE: the lines comented whit the *CUSTOM:* tag mean that such argument
    # is a custom version of the original object

    # create a new *code object* (like function.__code__)
    code_object = types.CodeType(
        old_code.co_argcount,
        old_code.co_kwonlyargcount,
        old_code.co_nlocals,
        old_code.co_stacksize,
        old_code.co_flags,
        bytes(new_code),        # CUSTOM function.__code__.old_code.co_code
        tuple(new_consts),      # CUSTOM function.__code__.old_code.co_consts
        tuple(new_names),       # CUSTOM function.__code__.old_code.co_names
        old_code.co_varnames,
        old_code.co_filename,
        old_code.co_name,
        old_code.co_firstlineno,
        old_code.co_lnotab,
        tuple(new_freevars),    # CUSTOM function.__code__.old_code.co_freevars
        old_code.co_cellvars)

    # Customize the argument of the function object
    _code    = code_object
    _globals = function.__globals__
    _name    = function.__name__
    _argdef  = function.__defaults__
    _closure = tuple(_make_closure_cell(var) for var in new_freevars)

    # Make and return the new function
    return types.FunctionType(_code, _globals, _name, _argdef, _closure)


def _pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


_LEFT_OPERATOR = [
    ('__add__', '%s+(%s)'),
    ('__and__', '%s&(%s)'),
    ('__div__', '%s/(%s)'),
    ('__eq__', '%s==(%s)'),
    ('__floordiv__', '%s//(%s)'),
    ('__ge__', '%s>=(%s)'),
    ('__gt__', '%s>(%s)'),
    ('__le__', '%s<=(%s)'),
    ('__lshift__', '%s<<(%s)'),
    ('__lt__', '%s<(%s)'),
    ('__matmul__', '%s@(%s)'),
    ('__mod__', '%s%%(%s)'),
    ('__mul__', '%s*(%s)'),
    ('__ne__', '%s!=(%s)'),
    ('__or__', '%s|(%s)'),
    ('__pow__', '%s**(%s)'),
    ('__rshift__', '%s>>(%s)'),
    ('__sub__', '%s-(%s)'),
    ('__truediv__', '%s/(%s)'),
    ('__xor__', '%s^(%s)'),
]

_RIGHT_OPERATOR = [
    ('__radd__', '(%s)+%s'),
    ('__rand__', '(%s)&%s'),
    ('__rdiv__', '(%s)/%s'),
    ('__rfloordiv__', '(%s)//%s'),
    ('__rlshift__', '(%s)<<%s'),
    ('__rmatmul__', '(%s)@%s'),
    ('__rmod__', '(%s)%%%s'),
    ('__rmul__', '(%s)*%s'),
    ('__ror__', '(%s)|%s'),
    ('__rpow__', '(%s)**%s'),
    ('__rrshift__', '(%s)>>%s'),
    ('__rsub__', '(%s)-%s'),
    ('__rtruediv__', '(%s)/%s'),
    ('__rxor__', '(%s)^%s'),
]

_UNARY_OPERATOR = [
    ('__invert__', '~(%s)'),
    ('__neg__', '-(%s)'),
    ('__pos__', '+(%s)'),
]

_BUILT_IN_FUNCTIONS = [
    ('__abs__', 'abs(%s%s%s)'),
    ('__round__', 'round(%s%s%s)'),
    ('__reversed__', 'reversed(%s%s%s)'),

    # FIXME: folowing methods did not work. View FailedExpressionBehaviours
    # class in the tests/test_suger.py module.

    # ('__instancecheck__', 'isinstance(%s%s%s)'),
    # ('__subclasscheck__', 'issubclass(%s%s%s)'),
    # ('__contains__', 'contains(%s%s%s)'),
    # ('__len__', 'len(%s%s%s)'),
    # ('__iter__', 'iter(%s%s%s)'),

    # TODO:
    # ('__bytes__', 'bytes(%s%s%s)'),
    # ('__format__', 'format(%s%s%s)'),
    # ('__hash__', 'hash(%s%s%s)'),
    # ('__bool__', 'bool(%s%s%s)'),
    # ('__setattr__', 'setattr(%s%s%s)'),
    # ('__delattr__', 'delattr(%s%s%s)'),
    # ('__dir__', 'dir(%s%s%s)'),
]


def _left_operator(template):
    """Return a function that make an expression string with a binary
    left operator."""
    def operator(self, other):
        result = Expression('')
        if hasattr(other, '__expr__'):
            result.__expr__ = template % (self.__expr__, other.__expr__)
        else:
            result.__expr__ = template % (self.__expr__, repr(other))
        return result
    return operator


def _right_operator(template):
    """Return a function that make an expression string with an
    binary operator placed at the right of the variable."""
    def operator(self, other):
        result = Expression('')
        if hasattr(other, '__expr__'):
            result.__expr__ = template % (other.__expr__, self.__expr__)
        else:
            result.__expr__ = template % (repr(other), self.__expr__)
        return result
    return operator


def _unary_operator(template):
    """Return a function that make an expression string with an
    unary operator."""
    def operator(self):
        result = Expression('')
        result.__expr__ = template % self.__expr__
        return result
    return operator


def _built_in_function(template):
    """Return a function that make an expression with an
    built in function."""
    def function(self, *args, **kwds):
        formated_kwds, formated_args = '', ''
        if args != ():
            formated_args = ', ' + repr(args)[1:][:-2]
        if kwds != {}:
            add_equal = ('%s=%s' %  (key, repr(value)) for \
                         key, value in kwds.items())
            formated_kwds = ', ' + ', '.join(add_equal)
        result = Expression('')
        result.__expr__ = template % (self.__expr__, formated_args,
                                      formated_kwds)
        return result
    return function


class _DefineAllOperatorsMeta(type):
    """All operators of the new class will return an instance of the
    Expression class."""
    def __new__(cls, name, bases, namespace):
        namespace.update({function: _left_operator(template) for \
                          function, template in _LEFT_OPERATOR})
        namespace.update({function: _right_operator(template) for \
                          function, template in _RIGHT_OPERATOR})
        namespace.update({function: _unary_operator(template) for \
                          function, template in _UNARY_OPERATOR})
        namespace.update({function: _built_in_function(template) for \
                          function, template in _BUILT_IN_FUNCTIONS})
        new_class = super().__new__(cls, name, bases, namespace)
        return new_class


class Expression(metaclass=_DefineAllOperatorsMeta):
    """Create an object that store all mathematical operations
    in which it is involved."""
    def __init__(self, name, bases=()):
        self.__expr__ = name

    def __repr__(self):
        return self.__expr__

    def __getattr__(self, attr):
        result = Expression('')
        result.__expr__ = '(%s).%s' % (self.__expr__, attr)
        return result

    def __getitem__(self, attr):
        result = Expression('')
        result.__expr__ = '(%s)[%s]' % (self.__expr__, repr(attr))
        return result

    def __hash__(self):
        return hash(self.__expr__)


OTHERWISE = '__otherwise__'


class _Body:
    def __init__(self, expression):
        self.environ = {"docstring": "", "arguments": "", "expression": "",
                        "constants": "", "pattern": ""}

    def where(self, **constants):
        """Inject constatns in the function."""
        formated = '\n'.join(" %s = %s" % (key, repr(value)) for \
                             key, value in constants.items()) + '\n'
        self.environ["constants"] = formated
        return self


class Do(_Body):
    def __init__(self, body):
        super().__init__(body)
        self.body = body


class Match(_Body):
    def __init__(self, pattern):
        super().__init__(pattern)
        self.pattern = pattern


class Raise:
    def __init__(self, error):
        self.error = error


def _replace_globals_and_locals(function):
    "Replace defined locals and globals by an Expression object."
    globals_and_locals = itertools.chain(function.__code__.co_names,
                                         function.__code__.co_freevars)
    for var in globals_and_locals:
        if var in function.__code__.co_consts:
            # The first const everything is None. So I remove them
            consts = function.__code__.co_consts[1:]
            # Now I make a dictionary
            consts = {name: Expression(name) for name, _ in \
                      _pairwise(consts)}
            return _inject_constants(function, consts)
    return function


class Let:
    def __init__(self, lambda_func):
        assert type(lambda_func) is types.LambdaType
        self.template = "def function{arguments}:\n" \
                        "{docstring}" \
                        "{constants}" \
                        "{pattern}" \
                        "{expression}"
        self.lambda_func = _replace_globals_and_locals(lambda_func)
        self.make_expression()
        if isinstance(self.expression, Match):
            self.make_pattern()
        if isinstance(self.expression, Do):
            self.make_do_body()
        self.make_signature()
        self.source = self.template.format(**self.expression.environ)

    def make_expression(self):
        parameters = self.lambda_func.__code__.co_varnames
        arguments = tuple(Expression(arg) for arg in parameters)
        self.expression = self.lambda_func(*arguments)

    def make_do_body(self):
        if isinstance(self.expression, Expression):
            self.expression.environ["expression"] = " return %s\n" % \
                                              expression.__expr__
        elif isinstance(self.expression.body, Raise):
            self.expression.environ["expression"] = \
                " raise %s\n" % repr(self.expression.body.error)
        else:
            self.expression.environ["expression"] = \
                " return %s\n" % repr(self.expression.body)

    def make_pattern(self):
        if_expression = ''
        elif_expression = ''
        else_expression = ''
        for key, value in self.expression.pattern.items():
            if isinstance(value, Raise):
                new_value = repr(self.expression.pattern[key].error)
                self.expression.pattern[key] = "raise " + new_value
            else:
                self.expression.pattern[key] = "return " + repr(value)
        pattern = self.expression.pattern
        if '__otherwise__' in pattern and len(pattern) > 1:
            value = pattern.pop('__otherwise__')
            else_expression = " else:\n  %s\n" % value
        if len(pattern) == 1:
            if_expression = " if %s:\n  %s\n" % list(pattern.items())[0]
        else:
            iter_pattern = iter(pattern.items())
            if_expression = " if %s:\n  %s\n" % next(iter_pattern)
            elif_expression = ''. join(' elif %s:\n  %s\n' % \
                                       (key, value) for key, value in \
                                       iter_pattern)
        self.expression.environ["expression"] = (
            if_expression + elif_expression + else_expression)


    def make_signature(self):
        args = inspect.formatargspec(*inspect.getargspec(self.lambda_func))
        self.expression.environ["arguments"] = args
