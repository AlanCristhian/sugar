"""A module that let you define a function with the following sintax:

cylinder = sugar.Let(lambda:
    "A function that calculate" # [1]: docstring
    "the area the cylinder."
    takes(                      # [2]: parameters
        d, h
    ).do(                       # [3]: body
        (PI*d**2)/2 + PI*d*h
    ).where(                    # [4]: constants
        PI = 3.14
    ))

where [1] is the docstring of the function, [2] define the arguments of the
function, [3] be the body and [3] determine the constants used in the body.

That expession is equivalent to:

def cylinder(d, h):
    "A function that calculate" \
    "the area the cylinder."
    PI = 3.14
    yield (PI*d**2)/2 + PI*d*h
"""


import ast
import dis


# FIRST: store the bytecode information
# in an object that facilitates their handling


class Code:
    """Store all valid scopes and the code object
    """
    def __init__(self, function):
        self.bytecode = dis.Bytecode(function.__code__)
        # properties that store all valid scopes in a lambda function
        self.constants = function.__code__.co_consts
        self.enclosed_names = function.__code__.co_freevars
        self.global_names = function.__code__.co_names


# SECOND: make a docstring


class Decompile(Code):
    """Make an AST with the byte code and the scope of the lambda
    function.
    """
    def __init__(self, function):
        super().__init__(function)
        self.arguments_node = ast.arguments(args=[], vararg=None,
                                            kwonlyargs=[], kw_defaults=[],
                                            kwarg=None, defaults=[])
        self.function_node = ast.FunctionDef(name='f',
                                             args=self.arguments_node,
                                             body=[], decorator_list=[],
                                             returns=None)
        self.module_node = ast.Module(body=[self.function_node])
        self.docstring_node = self.make_docstring()
        if self.docstring_node is not None:
            self.function_node.body.append(self.docstring_node)

    def make_docstring(self):
        "Check if the expession have a docstring"
        instruction = next(iter(self.bytecode))
        if instruction.opname == 'LOAD_CONST' and \
                type(instruction.argval) is str and \
                instruction.arg == 1:
            str_node = ast.Str(s=instruction.argval)
            return ast.Expr(value=str_node)
        else:
            return None

