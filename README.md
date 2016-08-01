# sugar
Python 3 functional programing experiments.

## Abandoned

I drop this project because:
- The special lambda function are hard to debug.
- The library have too many hacks to work and the implementation is
  unintuitive.
- If ocur an error, the traceback will show the information in the mapped
  function. Such thing is useless because the function is defined dinamically
  in another place of the source.
- Don't have a good way to implement generators, coroutines or async functions.
- Don't support full python expression. E.g. if/else expression, or/and
  operators, try/except blocks.
- The most simple real life function looks ugly and is hard to understand. See
  the `electric_force` function in the example below.
- There are only few cases that can benefit with recursivity. Loops are the
  best solution for most common cases. Loops also are a powerfull tool mixed
  with generators.
- Nested functions are less redable. See `_compose_two` example.
- Lamda returns the expression by default. No obvious way to yield or await a
  value.
- Lamda functions can't be annotated with type hints. Maybe arguments and
  returned value can be checked with assertions but is an runtime solution. An
  static analyzer (like mypy) can't infer types.
- PEP 8 must be unfollowed to improve the redability of lamda functions.
  Linters warns for PEP 8 errors.
- No elegant way to decorate a lambda funcion.
- No ovious way to add docstring.
- No clear way to handle exceptions.
- Functional programming is not a good idea in general.

## examples

Bellow are examples that show how to define a function with sugar and then
with vanilla python.

### Minimal Function

```python
from sugar import Let

basic = Let("basic", lambda: {None})

def basic():
    pass
```

### Mathematical expression

```python
from sugar import Let

add = Let("add", lambda x, y: {x + y})

# ------------------------------------

def add(x, y):
    return x + y
```

### Exceptions

```python
from sugar import Let, Raise

exception = Let("exception", lambda: {
    Raise(ValueError, 'description')
})

# ------------------------------------

def exception():
    raise ValueError('description')
```

### Wards

```python
from sugar import Let, Raise, OTHERWISE

is_positive = sugar.Let("is_positive", lambda x: {
    x > 0    : True,
    x < 0    : False,
    OTHERWISE: Raise(ValueError, "Zero is unsigned."),
})

# ----------------------------------------------------

def is_positive(x):
    if x > 0:
        return True
    elif x < 0:
        return False
    else:
        raise ValueError("Zero is unsigned.")
```

### Define constants

```python
from sugar import Let, Raise, Where

electric_force = Let("electric_force", lambda charge, radious: {
    (charge*elemental_charge)/(4*pi*vacuum_permittivity*radious**2)
}&where(
    pi = 3.142,
    elemental_charge = 1.602e-19,
    vacuum_permittivity = 8.854e-12,
))

# ------------------------------------------------------------------------

def electric_force(charge, radious):
    pi = 3.142
    elemental_charge = 1.602e-19
    vacuum_permittivity = 8.854e-12
    return (charge*elemental_charge)/(4*pi*vacuum_permittivity*radious**2)
```

### Nested functions


```python
from sugar import Let, functools

# Takes two functions as arguments (first and second)
# and returns a function representing their composition.
_compose_two = Let("_compose_two", lambda first, second: {
    _call_nested
}&where(
    _call_nested = Let("_call_nested", lambda argument: {
        first(second(argument))
    })
))

# Take an indefinite number of functions and
# returns a function that compose all them.
compose = Let("compose", lambda *functions: {
    functools.reduce(_compose_two, functions)
})

# ---------------------------------------------------------

def _compose_two(first, second):
    """Takes two functions as arguments (first and second)
    and returns a function representing their composition.
    """
    def _call_nested(argument):
        return first(second(argument))
    return _call_nested

def compose(*functions):
    """Take an indefinite number of functions and
     returns a function that compose all them.
     """
    return functools.reduce(_compose_two, functions)
```
