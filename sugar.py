"""Python 3 functional programing experiments."""


import collections
import itertools
import inspect
import opcode
import types


__all__ = ["Let", "Do", "Expression", "Raise"]


def _make_closure_cell(value):
    """The types.FunctionType class ned a cell variable in the
    closure argument. This function create such type with the value.
    """
    def nested():
        return value
    return nested.__closure__[0]


def _change_op_code(position, op_code, instruction, old_names, new_constants,
                    custom_co_code, custom_co_names, custom_co_consts):

    # NOTE: ensure that bellow variables are list because I need to mutate them
    assert type(custom_co_code) is list
    assert type(custom_co_names) is list
    assert type(custom_co_consts) is list

    if op_code == opcode.opmap[instruction]:
        op_code_argument = custom_co_code[position + 1] + \
                           (custom_co_code[position + 2] << 8)

        # Can't use the new_name variable directly because if I clean the
        # name position get an IndexError.
        name = old_names[op_code_argument]
        if name in new_constants:
            new_value = new_constants[name]
            for value_position, existent_value in enumerate(custom_co_consts):
                if new_value is existent_value:
                    break

            # Add the new_value to custom_co_consts if such value not exists.
            else:
                value_position = len(custom_co_consts)
                custom_co_consts.append(new_value)
                if instruction == 'LOAD_DEREF':
                    custom_co_names.remove(name)
            custom_co_code[position] = opcode.opmap['LOAD_CONST']
            custom_co_code[position + 1] = value_position & 0xFF
            custom_co_code[position + 2] = value_position >> 8


def _inject_constants(function, new_constants):
    """Return a copy of of the `function` parameter. This copy have
    the new_constants defined in the `new_constants` map. If a key of
    `new_constants` share the same name than a global or local object,
    then replace such global or local by the value defined in the
    `new_constants` argument.
    """
    # Store in list because I need to mutate them.
    custom_co_code     = list(function.__code__.co_code)
    custom_co_consts   = list(function.__code__.co_consts)
    custom_co_freevars = list(function.__code__.co_freevars)
    custom_co_names    = list(function.__code__.co_names)

    # Walk the list of instructions and change 'custom_co_code',
    # 'custom_co_consts', 'custom_co_freevars' and 'custom_co_names'.
    enumerate_custom_co_code = enumerate(custom_co_code)
    for position, op_code in enumerate_custom_co_code:

        # Replace global lookups by the values defined in *new_constants*.
        # function.__code__.co_names store names of all global variables.
        _change_op_code(position, op_code, 'LOAD_GLOBAL',
                        function.__code__.co_names, new_constants,
                        # bellow variables are mutated by the function
                        custom_co_code, [], custom_co_consts)

        # Replace local lookups by the values defined in *new_constants*.
        # function.__code__.co_freevars store names of all local variables
        _change_op_code(position, op_code, 'LOAD_DEREF',
                        function.__code__.co_freevars, new_constants,
                        # bellow variables are mutated by the function
                        custom_co_code, custom_co_freevars, custom_co_consts)

        if op_code >= opcode.HAVE_ARGUMENT:
            next(enumerate_custom_co_code)
            next(enumerate_custom_co_code)

    # create a new 'code object' (like function.__code__)
    custom_code = types.CodeType(function.__code__.co_argcount,
                                 function.__code__.co_kwonlyargcount,
                                 function.__code__.co_nlocals,
                                 function.__code__.co_stacksize,
                                 function.__code__.co_flags,
                                 bytes(custom_co_code),
                                 tuple(custom_co_consts),
                                 tuple(custom_co_names),
                                 function.__code__.co_varnames,
                                 function.__code__.co_filename,
                                 function.__code__.co_name,
                                 function.__code__.co_firstlineno,
                                 function.__code__.co_lnotab,
                                 tuple(custom_co_freevars),
                                 function.__code__.co_cellvars)

    # Customize the argument of the function object
    _code    = custom_code
    _globals = function.__globals__
    _name    = function.__name__
    _argdef  = function.__defaults__
    _closure = tuple(_make_closure_cell(variable) for variable in \
                     custom_co_freevars)

    # Make and return the new function
    return types.FunctionType(_code, _globals, _name, _argdef, _closure)


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
    """Return a function that make an expression
    string with a binary left operator.
    """
    def operator(self, other):
        result = Expression("")
        if hasattr(other, '__expr__'):
            result.__expr__ = template % (self.__expr__, other.__expr__)
        else:
            result.__expr__ = template % (self.__expr__, repr(other))
        return result
    return operator


def _right_operator(template):
    """Return a function that make an expression string with
    an binary operator placed at the right of the variable.
    """
    def operator(self, other):
        result = Expression("")
        if hasattr(other, '__expr__'):
            result.__expr__ = template % (other.__expr__, self.__expr__)
        else:
            result.__expr__ = template % (repr(other), self.__expr__)
        return result
    return operator


def _unary_operator(template):
    """Return a function that make an
    expression string with an unary operator.
    """
    def operator(self):
        result = Expression("")
        result.__expr__ = template % self.__expr__
        return result
    return operator

# The __call__ method difer of the other special methods in the serparator
# variable. So, I add such variable as default argument.
def _built_in_function(template, separator=', '):
    """Return a function that make an
    expression with an built in function.
    """
    def function(self, *args, **kwds):
        formated_kwds, formated_args = "", ""
        if args != ():
            formated_args = separator + repr(args)[1:][:-2]
        if kwds != {}:
            add_equal = ('%s=%r' % (key, value) for key, value in kwds.items())
            formated_kwds = ', ' + ', '.join(add_equal)
        result = Expression("")
        result.__expr__ = template % (self.__expr__, formated_args,
                                      formated_kwds)
        return result
    return function


class _DefineAllOperatorsMeta(type):
    """All operators of the new class will
    return an instance of the Expression class.
    """
    def __new__(cls, name, bases, namespace):
        namespace.update({function: _left_operator(template) for \
                          function, template in _LEFT_OPERATOR})
        namespace.update({function: _right_operator(template) for \
                          function, template in _RIGHT_OPERATOR})
        namespace.update({function: _unary_operator(template) for \
                          function, template in _UNARY_OPERATOR})
        namespace.update({function: _built_in_function(template) for \
                          function, template in _BUILT_IN_FUNCTIONS})
        call_method = _built_in_function(template='%s(%s%s)', separator="")
        namespace.update({'__call__': call_method})
        new_class = super().__new__(cls, name, bases, namespace)
        return new_class


class Expression(metaclass=_DefineAllOperatorsMeta):
    """Create an object that store all
    math operations in which it is involved.
    """
    def __init__(self, name, bases=()):
        self.__expr__ = name

    def __repr__(self):
        return self.__expr__

    def __getattr__(self, attr):
        result = Expression("")
        result.__expr__ = '(%s).%s' % (self.__expr__, attr)
        return result

    def __getitem__(self, attr):
        result = Expression("")
        result.__expr__ = '(%s)[%r]' % (self.__expr__, attr)
        return result

    def __hash__(self):
        return hash(self.__expr__)


class _Body:
    def __init__(self, expression):
        self.environ = {"docstring": "", "arguments": "", "expression": "",
                        "constants": "", "pattern": ""}

    def where(self, **constants):
        """Inject constatns in the function."""
        formated = '\n'.join("    %s = %r" % (key, value) for \
                             key, value in constants.items()) + '\n'
        self.environ["constants"] = formated
        return self


class Do(_Body):
    def __init__(self, body):
        super().__init__(body)
        self.body = body


class Match(_Body):
    def __init__(self, patterns):
        pattern = collections.OrderedDict(patterns)
        super().__init__(pattern)
        self.pattern = pattern


class Raise:
    def __init__(self, error, message=None):
        self.error = error if message is None else error(message)


def _replace_outher_scope_vars(function):
    """Replace defined locals and globals by an Expression object."""
    globals_and_locals = itertools.chain(function.__code__.co_names,
                                         function.__code__.co_freevars)
    constants = {}
    for var in globals_and_locals:
        if var in function.__code__.co_consts:
            # The first const everything is None. So I remove them
            constant_list = function.__code__.co_consts[1:]
            # Now I make a dictionary
            constant_dict = {name: Expression(name) for name in \
                             constant_list if name == var}
            constants.update(constant_dict)
    # Closures also will be an Expression object
    constants.update({name: Expression(name) for name in \
                     function.__code__.co_freevars})
    function = _inject_constants(function, constants)
    return function


class Let:
    def __init__(self, *args):
        # define name and custom_function
        if len(args) == 2:
            self.name = args[0]
            custom_function = args[1]
        elif len(args) == 1:
            self.name = "function"
            custom_function = args[0]
        else:
            raise TypeError("__init__() takes 3 positional arguments but"
                            " {} were given".format(len(args)))
        assert type(custom_function) is types.LambdaType

        # define the template
        self.template = "def {name}{arguments}:\n" \
                        "{docstring}" \
                        "{constants}" \
                        "{pattern}" \
                        "{expression}"
        # Decide if is recursive or not
        if self.name in custom_function.__code__.co_names \
        or self.name in custom_function.__code__.co_freevars:
            self.is_recursive = True
            custom_function = _inject_constants(custom_function,
                               {self.name: Expression(self.name)})
        else:
            self.is_recursive = False

        # convert all globals and locals in Expression objects
        self.function = _replace_outher_scope_vars(custom_function)
        # create the expression property
        self.expression = self.make_expression()
        # fill the name of the funciton
        self.expression.environ["name"] = self.name
        if isinstance(self.expression, Match):
            self.make_pattern()
        if isinstance(self.expression, Do):
            self.make_do_body()
        self.make_signature()
        self.source = self.template.format(**self.expression.environ)

    def make_expression(self):
        parameters = self.function.__code__.co_varnames
        arguments = (Expression(arg) for arg in parameters)
        return self.function(*arguments)

    def make_do_body(self):
        if isinstance(self.expression, Expression):
            self.expression.environ["expression"] = "    return %s\n" % \
                                              expression.__expr__
        elif isinstance(self.expression.body, Raise):
            self.expression.environ["expression"] = \
                "    raise %r\n" % self.expression.body.error
        else:
            self.expression.environ["expression"] = \
                "    return %r\n" % self.expression.body

    def make_pattern(self):
        if_expression = elif_expression = else_expression = ""
        for key, value in self.expression.pattern.items():
            if isinstance(value, Raise):
                self.expression.pattern[key] = "raise %r" % value.error
            else:
                self.expression.pattern[key] = "return %r" % value
        pattern = self.expression.pattern
        if 'otherwise' in pattern and len(pattern) > 1:
            value = pattern.pop('otherwise')
            else_expression = "    else:\n        %s\n" % value
        if len(pattern) == 1:
            if_expression = "    if %s:\n        %s\n" % \
                            next(iter(pattern.items()))
        else:
            iter_pattern = iter(pattern.items())
            if_expression = "    if %s:\n        %s\n" % next(iter_pattern)
            elif_expression = "".join('    elif %s:\n        %s\n' % \
                                      (key, value) for key, value in \
                                      iter_pattern)
        self.expression.environ["expression"] = (if_expression +
                                                 elif_expression +
                                                 else_expression)

    def make_signature(self):
        arguments = inspect.getargspec(self.function)
        formated_arguments = inspect.formatargspec(*arguments)
        self.expression.environ["arguments"] = formated_arguments


def all(*items):
    return "__builtins__.all(%s)" % list(items)


def all(*items):
    return "__builtins__.all(%s)" % list(items)
