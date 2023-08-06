# `gicd`

`gicd` contains a Python function that provides a decorator that will automatcially create an issue on GitHub if a decorated function throws an exception. That's it!

## Requirements

* The GitHub CLI (`gh`)

## Usage

Decorate a function with it:

```python
from gicd import gicd

@gicd("zmarffy", "test-repo", issue_label="explosion", exception_types=[IndexError, ValueError])
def error_prone_function():
    if input("Don't type anything; just hit enter... "):
        raise ValueError("Explosions!")
    print("All good!")
```

Then call the function:

```python
error_prone_function()
```

In the off chance that the function raises an exception, it will create an issue in the GitHub repo specified in the decorator. You can have the decorator do this with all exceptions (default behavior), or, if you specify the `exception_types` parameter, it will only create an issue when exceptions of those types are thrown.

This is mostly a joke package. It was my first library I ever wrote.
