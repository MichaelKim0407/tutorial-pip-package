from returns import returns


def add(x, y):
    return x + y


@returns(int)
def div_int(x, y):
    return x / y


def cmd_add(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)
    parsed_args = parser.parse_args(args)

    print(add(parsed_args.x, parsed_args.y))
