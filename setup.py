from setuptools import setup, find_packages

from my_pip_package import __version__

extra_math = [
    'returns-decorator',
]

extra_bin = [
    *extra_math,
]

extra_test = [
    *extra_math,
    'pytest>=4',
    'pytest-cov>=2',
]
extra_dev = [
    *extra_test,
]

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/MichaelKim0407/tutorial-pip-package',
    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    packages=find_packages(),

    extras_require={
        'math': extra_math,

        'bin': extra_bin,

        'test': extra_test,
        'dev': extra_dev,
    },

    entry_points={
        'console_scripts': [
            'add=my_pip_package.math:cmd_add',
        ],
    },
)
