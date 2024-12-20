"""
Client of Circuit. At first I cheated and looked up the solution on OEIS:

http://oeis.org/A153588

It's the 18th entry in the sequence. Then I implemented a solution suggested here:
https://www.quora.com/How-to-solve-Problem-155-Counting-capacitor-circuits-on-Project-Euler
"""

from itertools import product
from lib import circuit


def build_circuits_naive(max_level):
    cap_values = set()

    def bc(cr, level, max_level):
        if level < max_level:
            bc(cr.copy().add_parallel(), level+1, max_level)
            bc(cr.copy().add_series(), level+1, max_level)
        cap_values.add(cr.get_cap())

    bc(circuit.Circuit(), 1, max_level)
    return cap_values


def add_parallel(a, b):
    return a+b

def add_series(a, b):
    return 1 / (1/a + 1/b)

def build_circuits(max_level, epsilon=.000000001):
    """
    Epsilon parameter deals with floating point
    precision problems.

    >>> len(build_circuits(10, .000000001))
    2525
    """
    max_level = max(2, max_level)
    caps = [set() for i in range(max_level)]
    caps[0], caps[1] = set([1]), set([1/2, 2])

    for i in range(2, max_level):
        for j in range(i):
            if j > i-1-j:
                break
            for pair in product(caps[i-1-j], caps[j]):
                caps[i].add(add_parallel(*pair))
                caps[i].add(add_series(*pair))

    result = set()
    for cap_values in caps:
        result = result.union(cap_values)

    result = sorted(result)
    deduplicated = [result[0]]
    for i in range(1, len(result)):
        if abs(result[i-1] - result[i]) > epsilon:
            deduplicated.append(result[i])
    return deduplicated


if __name__ == '__main__':
    import doctest, sys
    doctest.testmod()

    max_level = int(sys.argv[1])
    cap_values = build_circuits(max_level)
    print(len(cap_values))
