# Practices

The Style, Linting, Documentation, and Code practices to be used while writing code for this repository.

## Documentation

All functions are to have docstrings.

```py
    """Short Description of the function

    (Optional) Long Description of the function

    Args:
        argument name (argument type): Description of the argument
    Returns:
        Type of the return value: Description of the return value
    """
```

For Example,

```py
    """Finds all URLs in a string and returns them as a list.
    Args:
        string (str): The string to search for URLs in.
    Returns:
        List[str]: A list of URLs found in the string.
    """
```

This allows other developers to easily understand, and build off of this code. Please use comments to document any confusing parts of your code.

Remember to use the `typing` extension, and typehint all arguments and functions. Make sure to lint your code using `mypy` and `pylint` before pushing.

## Style

Long lines are fine, so are multiple imports on one line. Please format all code with `black` before pushing. Please follow `camelCase` while naming variables, functions, and classes.

## Code Practices

Please test your code before pushing and make sure it's error free. Object Oriented, Asynchronous and Pythonic code are expected. This project uses `python 3.9.10`. Whenever something notable happens (command error, bot ready, etc), please log it to console using rich.

---

Dank Memer Grinder
