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


def _left_operator(template):
    """Return a function that make an expression string with a binary
    left operator."""
    def operator(self, other):
        result = Expression('')
        if hasattr(other, 'expression'):
            result.expression = template % \
                (self.expression, other.expression)
        else:
            result.expression = template % \
                (self.expression, repr(other))
        return result
    return operator


def _right_operator(template):
    """Return a function that make an expression string with an
    binary operator placed at the right of the variable."""
    def operator(self, other):
        result = Expression('')
        if hasattr(other, 'expression'):
            result.expression = template % \
                (other.expression, self.expression)
        else:
            result.expression = template % \
                (repr(other), self.expression)
        return result
    return operator

def _unary_operator(template):
    """Return a function that make an expression string with an
    unary operator."""
    def operator(self):
        result = Expression('')
        result.expression = template % self.expression
        return result
    return operator


class _DefineAllOperatorsMeta(type):
    """All operators of the new class will return an string that
    represent the mathematical expression."""
    def __new__(cls, name, bases, namespace):
        namespace.update({function: _left_operator(template) for \
                          function, template in _LEFT_OPERATOR})
        namespace.update({function: _right_operator(template) for \
                          function, template in _RIGHT_OPERATOR})
        namespace.update({function: _unary_operator(template) for \
                          function, template in _UNARY_OPERATOR})
        new_class = super().__new__(cls, name, bases, namespace)
        return new_class


class Expression(metaclass=_DefineAllOperatorsMeta):
    """Create an symbolic variable."""
    def __init__(self, name):
        self.expression = name

    def __repr__(self):
        return self.expression
