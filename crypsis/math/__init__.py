"""
Contains the most commonly used mathematical functions
(and the ones not fitting into a seperate category)
"""

from gmpy2 import invert, gcd

from crypsis.exceptions import NoSolution

# Calculate the product of a list
def product(xs):
    assert len(xs) > 0
    n = 1
    for x in xs:
        n *= x
    return n


# Apply the CRT for pairwise prime elements
def crt(pairs):
    """Solves a set of simultaneous congurences using the CRT
    When running opimized this call never fails, 
    but may produce invalid results if no solution exists

    Args:
        pairs (list): An iterable of pairs (y, z) to solve for
            x = y1 mod z1
            x = y2 mod z2
            x = y3 mod z3
            ...

    Returns:
        A positive integer with x = y mod z
        for every pair (y, z)
    """
    assert len(pairs) > 0

    # Calculate solution
    x = 0
    M = product(map(lambda (y, z): z, pairs))
    for y, z in pairs:
        c = M // z
        b = invert(c, z)
        x = (x + y * b * c) % M
    
    # Check solution
    if __debug__:
        for (y, z) in pairs:
            assert y % z == x % z
    return int(x)

# Apply generalized CRT (Yih-Hing)
def hing(pairs):
    """Solves a set of simultaneous congurences using 
    a generalized CRT (Yih-Hing).
    For more detail see 
    "Elementary Number Theory", Gareth A.Jones and J. Mary Jones

    When running optimized this call never fails, 
    but may produce invalid results if no solution exists

    Args:
        pairs (list): An iterable of pairs(y, P),
            where P are the prime factors of z 
            (see crt function documentation)
            Notice that the moduli need not be 
            pairwise relativly prime!

    Returns:
        A positive integer with x = y mod product(P)
        for every pair (y, P)
    """

    # Check for existance of solution
    if __debug__:
        prods = {product(P): y for y, P in pairs}
        assert len(prods) == len(pairs)
        for z1, y1 in prods.items():
            for z2, y2 in prods.items():
                if (y1 - y2) % gcd(z1, z2) != 0:
                    raise NoSolution

    # Find the highest exponent
    part = {}
    for y, p in pairs:
        for f in set(p):
            e = p.count(f)
            try:
                if part[f][0] >= e:
                    continue
            except KeyError:
                pass
            part[f] = (e, y)

    # Produce regular CRT instance
    new = []
    for f, (e, y) in part.items():
        z = pow(f, e)
        new.append((y % z, z))
    return crt(new)


# Calculates n / d and rounds up
def div_ceil(num, div):
    return -(-num // div)

# Calculates n / d and rounds down
def div_floor(num, div):
    return num // div
