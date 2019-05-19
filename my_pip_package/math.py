from returns import returns


def add(x, y):
    return x + y


@returns(int)
def div_int(x, y):
    return x / y
