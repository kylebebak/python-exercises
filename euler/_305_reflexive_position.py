"""
S is the Champernowne constant:

'1234567891011121314151617181920...'

let f(n) be the starting position of the nth occurrence of n in S
e.g. f(1) = 1, f(5) = 81, f(12) = 271, f(7780) = 111111365

find a fast way to compute f(n) for any n. specifically, find:
sum(map(f, [pow(3, k) for k in range(1,14)]))
"""


def p(target):
    """
    Returns starting position of where target is first
    explicity appended to string.

    >>> p(83)
    156
    """
    p, l = 0, len(str(target))
    for i in range(1, l):
        p += 9 * pow(10, i-1) * i
    p += (int(target) - pow(10, l-1)) * l
    return p



def f(x):
    nums = set()
    sx = str(x)
    digits = len(sx)
    offset = 0

    # x in y1y2 with y1 smaller than x (e.g. 243 in 42, 43)
    for i in range(1, digits//2+1):
        y = int(sx[:i])
        sy = str(y+1)
        if sy == sx[digits - len(sy):]:
            offset += 1

    # rotations of x
    for i in range(digits):
        s = sx[i:] + sx[:i]
        if s[0] != '0':
            nums.add(int(s))

    # ___x___ and all  x2___x1 ('x1x2' = 'x')
    k, p10 = 1, 10
    while True:
        if len(nums) + offset >= x:
            break
        offset += len(nums)
        nums = set()

        for y in range(p10):
            sy = str(y).rjust(k, '0')
            for i in range(1, k+1):
                s = sy[:i] + sx + sy[i:]
                if s[0] != '0':
                    nums.add(int(s))
            for i in range(digits):
                s = sx[i:] + sy + sx[:i]
                if s[0] != '0':
                    nums.add(int(s))
        k += 1
        p10 *= 10

    # sort nums and get n
    nums = list(sorted(nums))
    n = nums[x-1 - offset]

    # count digits before n
    pos = p(n)

    # adjust for position in n, n+1
    s = str(n)+str(n+1)
    pos += s.index(sx) + 1

    return pos



if __name__ == '__main__':
    import doctest, sys
    doctest.testmod()

    N = int(sys.argv[1])
    s = 0
    for k in range(1, N+1):
        y = f(pow(3, k))
        print(k, y)
        s += y

    print('sum: {0}'.format(s))
