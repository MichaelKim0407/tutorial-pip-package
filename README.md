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

### Recommendations for this tutorial

It is recommended to create a virtual environment and do everything in it
for the purpose of this tutorial,
so that you won't mess up your python installation.

For Python 3.6+, you may use the `venv` module in the standard library.
[HOWTO](https://docs.python.org/3/library/venv.html#creating-virtual-environments)

For previous versions of Python, you may use [`virtualenv`](https://virtualenv.pypa.io/en/latest/).

After creating the virtual environment,
it might be a good idea to update the base packages we are going to use:

```bash
$ pip install -U pip setuptools
```

## Step 1: Create an importable module!

Since `pip` is going to install modules that we can `import`,
we need to have one ready first.
Let's create `my_pip_package.py`:

```python
def hello_world():
    print("This is my first pip package!")
```

Confirm that it can be imported properly:

```bash
$ python -c "import my_pip_package; my_pip_package.hello_world()"
This is my first pip package!
```

Checkout the repo at this stage using the [`01-create-module`](https://github.com/MichaelKim0407/tutorial-pip-package/tree/01-create-module) tag.

## Step 2: Create `setup.py`

`setup.py` is used to tell `pip` how to install the package.
You can find the full documentation [here](https://setuptools.readthedocs.io/en/latest/setuptools.html).

For this tutorial we will have the most basic setup ready,
and expand upon it.

```python
from setuptools import setup

from my_pip_package import __version__

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/MichaelKim0407/tutorial-pip-package',
    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    py_modules=['my_pip_package'],
)
```

Change url and author info for yourself.

Add this to `my_pip_package.py`:

```python
__version__ = 'dev'
```

To confirm that `setup.py` works properly:

```bash
$ pip install -e .
```

It should install the package
and create a folder called `my_pip_package.egg-info`.

If you are using version control systems like `git`,
make sure to ignore that folder.

Now, you should be able to import the package outside of the folder:

```bash
$ cd ..
$ python -c "import my_pip_package; my_pip_package.hello_world()"
This is my first pip package!
```

If you have pushed your code to a git hosting service,
you should be able to install it anywhere right now:

```bash
$ pip install git+git://github.com/MichaelKim0407/tutorial-pip-package.git#egg=my_pip_package
```

(replace with your own repo url)

Note for `pipenv`:
you should use `-e` flag so that `pipenv` will pick up dependencies in the lock file.

Checkout the repo at this stage using the [`02-setup-py`](https://github.com/MichaelKim0407/tutorial-pip-package/tree/02-setup-py) tag.

## Step 3: Convert to multi-file package

This step is optional, if you want to keep everything in one file.
However, the setup is slightly different so we'll keep this as a separate step.

First, turn the Python module into a package:

```bash
$ mkdir my_pip_package
$ mv my_pip_package.py my_pip_package/__init__.py
```

Add another Python file in the package, e.g. `math.py`:

```python
def add(x, y):
    return x + y
```

Change the following lines in `setup.py`:

`from setuptools import setup` ->
`from setuptools import setup, find_packages`

`py_modules=['my_pip_package']` ->
`packages=find_packages()`

Test that everything works:

```bash
$ python -c "import my_pip_package; my_pip_package.hello_world()"
This is my first pip package!
$ python -c "from my_pip_package.math import add; print(add(1, 3))"
4
```

Checkout the repo at this stage using the [`03-convert-package`](https://github.com/MichaelKim0407/tutorial-pip-package/tree/03-convert-package) tag.

## Step 4: Adding dependencies

If you want to use another `pip` library as dependency,
you can specify it in `setup.py`.

First, let's add the following code to `math.py`:

```python
from returns import returns


@returns(int)
def div_int(x, y):
    return x / y
```

The `returns` decorator comes from the `returns-decorator` package
(DISCLAIMER: created by the author of this tutorial),
which is available on `pypi`.
When writing production code you should totally use `//`,
but for the sake of demonstration let's use the decorator for now.

To specify `returns-decorator` as a dependency,
add the following entry to `setup(...)` in `setup.py`:

```python
install_requires=[
    'returns-decorator',
],
```

Run `pip install -e .` again to pick up the new dependency.

Now verify that it works:

```bash
$ python -c "from my_pip_package.math import div_int; print(div_int(3, 2))"
1
```

You may also specify versions of your dependency,
e.g. `returns-decorator>=1.1`.
For the full spec, see [PEP 508](https://www.python.org/dev/peps/pep-0508/).

Checkout the repo at this stage using the [`04-dependency`](https://github.com/MichaelKim0407/tutorial-pip-package/tree/04-dependency) tag.

## Step 5: Adding optional (extra) dependencies

Sometimes certain parts of your code require a specific dependency,
but it's not necessarily useful for all use cases.

One example would be the `sqlalchemy` library,
which supports a variety of SQL dialects,
but in most cases anyone using it would only be interested in one dialect.

Installing all dependencies is both inefficient and messy,
so it's better to let the user decide what exactly is needed.
However, it would be cumbersome for the user to install the specific dependencies.
This is where extra dependencies some in.

For this tutorial, after the last step,
let's pretend that we don't want to always install `returns-decorator` unless `math` is used.
We can replace the `install_requires` with the following:

```python
extras_require={
    'math': [
        'returns-decorator',
    ],
},
```

Note the `s`: `install_requires` is singular but `extras_require` is plural.

Now, we can install the extra dependency by appending `[math]` in the installation:

```bash
$ pip install -e .[math]
```

or

```bash
$ pip install git+git://github.com/MichaelKim0407/tutorial-pip-package.git#egg=my_pip_package[math]
```

However, we are not finished just yet -
since we want to add more extra dependencies in the future,
it's better to keep them organized.

One good habit is to make a `[dev]` extra dependency,
which includes all dependencies needed for local development.
In `setup.py`:

```python
extra_math = [
    'returns-decorator',
]

extra_dev = [
    *extra_math,
]
```

and in `setup(...)`:

```python
extras_require={
    'math': extra_math,

    'dev': extra_dev,
},
```

Now we can just run `pip install -e .[dev]` whenever we want to setup a dev environment.

Checkout the repo at this stage using the [`05-extra-dependency`](https://github.com/MichaelKim0407/tutorial-pip-package/tree/05-extra-dependency) tag.

## Step 6: Command line entries

`pip` allows packages to create command line entries in the `bin/` folder.

First, let's make a function that accepts command line arguments in `math.py`,
and make the module callable:

```python
def cmd_add(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)
    parsed_args = parser.parse_args(args)

    print(add(parsed_args.x, parsed_args.y))


if __name__ == '__main__':
    cmd_add()
```

Test it out:

```bash
$ python my_pip_package/math.py 1.5 3
4.5
```

Now, add the following entry to `setup(...)`:

```python
entry_points={
    'console_scripts': [
        'add=my_pip_package.math:cmd_add',
    ],
},
```

The syntax is `{cmd entry name}={module path}:{function name}`.

Run `pip install -e .[dev]` again to create the command line entry.

```bash
$ add 1.6 4
5.6
```

The `__name__ == '__main__'` part is not really needed,
so let's remove it.

Also, since the `add` command requires the `[math]` dependency,
let's make it explicit for anyone wishing to use the command:

```python
extra_bin = [
    *extra_math,
]
```

and

```python
extra_requires = {
    ...,
    'bin': extra_bin,
}
```

Checkout the repo at this stage using the [`06-command`](https://github.com/MichaelKim0407/tutorial-pip-package/tree/06-command) tag.
