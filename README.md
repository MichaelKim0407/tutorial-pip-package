# TUTORIAL: How to create your own pip library

Author: Michael Kim <mkim0407@gmail.com>

## Overview

The idea of `pip` roots back to the `import` keyword in Python,
and that the keyword works for both standard library and user-defined modules.

While user-defined modules are often single-use and not very complicated,
it can be helpful that they can be reused across different projects without copy-pasting,
or even shared with other developers.

Before moving on to `pip`, there are several other possible approaches.

1. Add modules to the standard Python library.

    This is not a good approach because every developer needs different libraries,
    so increasing the size of the Python distribution is not beneficial.
    Also, code in the standard library should have a higher standard
    and have less flexibility when changes are needed.

2. Modify `PYTHONPATH` environment variable.

    While this can work locally on one machine,
    modifying the system setup can be problematic when it comes to distribution/deployment,
    and it has a high chance of messing things up on other parts of the system.

### So what is `pip`?

From the [homepage](https://pip.pypa.io/en/stable/):

> pip is the package installer for Python.
> You can use pip to install packages from the Python Package Index and other indexes.

### `pip` vs `pypi`

`pip` is the package installer,
while [Python Package Index](https://pypi.org/), or `pypi`,
is the package distribution platform that `pip` references *by default*.

Because running `pip install {package}` will find the package on `pypi`,
download, and then install it,
it is easy to confuse them as one integral service.

However, a package for `pip` does not have to live on `pypi`,
as we'll demonstrate in this tutorial,
and apparently you can download packages from `pypi` without using `pip`.
