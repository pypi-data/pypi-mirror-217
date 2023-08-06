def enummi(*args):
    """
    Generator function that combines multiple iterables into a single sequence of tuples,
    assigning an index value to each tuple.

    Args:
        *args: One or more iterables to be combined.

    Yields:
        Tuples containing an index value and elements from the input iterables.

    Example:
        for i, a, b, c in enummi([1, 2, 3], [4, 5, 6], [7, 8, 9]):
            print(i, a, b, c)
        Output:
            0 1 4 7
            1 2 5 8
            2 3 6 9

        for i, a in enummi([1, 2, 3]):
            print(i, a)
        Output:
            0 1
            1 2
            2 3

        for i, a in enummi([]):
            print(i, a)
        Output:
            (no output)
    """
    if len(args) > 1:
        i = 0
        for va in zip(*args):
            yield i, *va
            i += 1
    elif len(args) == 1:
        for i, va in enumerate(args[0]):
            yield i, va



