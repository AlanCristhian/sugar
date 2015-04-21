# Decompiler notes

## Scope

- Maybe the `lambda function` never store locals variables.
- Don't worry about \_\_builtin\_\_ namespace, just put the name of the variable
  in the `.globals_name` property. If a name cannot found in the global namespace
  python automatically find in the \_\_builtin\_\_ namespace.
