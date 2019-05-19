from setuptools import setup, find_packages

from my_pip_package import __version__

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/MichaelKim0407/tutorial-pip-package',
    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    packages=find_packages(),

    install_requires=[
        'returns-decorator',
    ],
)
