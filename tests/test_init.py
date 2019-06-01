from my_pip_package import hello_world


def test_hello_world(capsys):
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == 'This is my first pip package!\n'
    assert captured.err == ''
