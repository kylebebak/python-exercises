"""
The implementation for this problem is functional, it does not import
any classes from modules in the lib package. The functions used to solve
the problem are defined in this script, not in lib, because they are
unlikely to be used elsewhere.
"""

def fib_until(cutoff, n0=0, n1=1):
    """
    Returns the fibonacci sequence until a term
    is >= the cutoff value.

    >>> fib_until(20, 0, 1)
    [0, 1, 1, 2, 3, 5, 8, 13, 21]
    """
    seq = [n0, n1]
    while True:
        if n1 >= cutoff:
            return seq
        n0, n1 = n1, n0+n1
        seq.append(n1)

def char_at_index(D, w0, w1):
    """
    Finds char at the index specified, given that w0 and
    w1 are the starting strings in the fibonacci "string"
    sequence. Uses the length of the input strings to work
    backwards and find the index of the character in one of
    the input strings that would have to occupy the index D
    in the fibonacci string. Can handle huge values of D.
    Assumes the string has only been built up only to the
    minimum size required to contain the specified index D.

    >>> char_at_index(35, "1415926535", "8979323846")
    '9'

    >>> char_at_index(20.5, "dog", "house")
    Traceback (most recent call last):
        ...
    TypeError: The char index must be a positive integer.

    >>> char_at_index(-1, "dog", "house")
    Traceback (most recent call last):
        ...
    TypeError: The char index must be a positive integer.
    """
    if not isinstance(D, int) or D < 1:
        raise TypeError('The char index must be a positive integer.')
    if not isinstance(w0, str) or not isinstance(w1, str):
        raise TypeError('The starting terms must be strings.')

    # reverse fibonacci sequence
    indices = list(reversed(
        fib_until(D, len(w0), len(w1))
    ))
    L = len(indices)

    i = 0
    # work backwards towards string and index of original char
    while i < L-2:
        if D > indices[i+2]:
        # char came from previous word
            D -= indices[i+2]
        else:
        # char came from word before previous word
            i += 1
        i += 1
    w = w0 if L-1-i == 0 else w1
    return w[D-1]


if __name__ == '__main__':
    import doctest, sys, time
    doctest.testmod()

    start_time = time.time()
    try:
        w0, w1 = sys.argv[1], sys.argv[2]
    except IndexError:
        print("Two strings must be passed to this script.")
        sys.exit()

    # finds the value specified by the problem
    s = 0
    for i in range(18):
        s += pow(10, i) * \
        int(char_at_index(
            (127 + 19*i) * pow(7, i), w0, w1
        ))
    print(s)
    print('Duration: {0}s'.format(time.time() - start_time))
