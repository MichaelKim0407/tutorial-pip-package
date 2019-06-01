import random

from my_pip_package.math import add, div_int, cmd_add


def test_add():
    assert add(1, 2) == 3
    assert add(0.1, 3) == 3.1
    a, b = random.random(), random.random()
    assert add(a, b) == a + b


def test_div_int():
    assert div_int(3, 2) == 1
    assert div_int(3, 1.6) == 1
    a, b = random.random(), random.random()
    assert div_int(a, b) == a // b


def test_cmd_add(capsys):
    cmd_add(['1', '3'])
    cmd_add(['1', '2.2'])
    captured = capsys.readouterr()
    assert captured.out == '4\n3.2\n'
    assert captured.err == ''
