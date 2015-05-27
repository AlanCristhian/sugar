# sugar
Python 3 functional programing experiments.

## Abandoned

I drop this project because:
- The special lambda function are hard to debug.
- The library have too many hacks to work and the implementation is unintuitive.
- If ocur an error, the traceback will show the information in the mapped
  function. Such thing is useless because the function is defined dinamically
  in another place of the source.
- Don't have a good way to implement generators, coroutines or async functions.
- Don't support a ful python expression. E.g. if/else expression, or/and
  operators.
- The most simple real life function looks ugly and is hard to understand.
- There are only few cases that can benefit with recursivity. Loops are the
  best solution for most common cases.
- Nested functions are less redable.
- Lamda returns the expression by default. No obvious way to yield or await a value.
- Lamda functions can't be annotated with type hints. Maybe arguments and
  returned value can be checked with assertions but is an runtime solution. An
  static analyzer (like mypy) can't infer types.
- PEP 8 must be unfollowed to improve the redability of lamda functions. Linters
  warns for PEP 8 errors.
- No elegant way to decorate a lambda funcion.
- Functional programming is not a good idea in general.
