"""Python 3 functional programing experiments."""

import inspect


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

def _format_positional_arguments(args):
    formated_args = ', ' + repr(args)[1:][:-1]


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
        return self._expression

    def __getattr__(self, attr):
        result = Expression('')
        result.__expr__ = '(%s).%s' % (self.__expr__, attr)
        return result

    def __getitem__(self, attr):
        result = Expression('')
        result.__expr__ = '(%s)[%s]' % (self.__expr__, repr(attr))
        return result


class Define:
    """Provide a declarative API to define a function."""
    def __init__(self, docstring):
        self.docstring = docstring

    def __call__(self, *args, **kwds):
        raise TypeError("'Define' object is not callable: missing '.end' at "
                        "the ending of the function definition.")

    def let(self, **parameters):
        self._parameters = tuple(parameters)
        self._globals = inspect.currentframe().f_back.f_globals
        self._globals.update(parameters)
        return self

    @property
    def end(self):
        for name in self._parameters:
            del self._globals[name]
