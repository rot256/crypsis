import os

def xor(a, b):
    return map(lambda (x, y): x^y, zip(a, b))

def rand(n):
    assert type(n) == int
    return map(ord, os.urandom(n))

def explode(bstr):
    assert type(bstr) == str
    return map(ord, bstr)

def implode(ilst):
    """ Implodes a list of integers into a single binary string """
    return ''.join(map(chr, ilst))

def chop(ilst, size):
    """ Chops an integer list into fixed size blocks
    If the list length is not a multiple of "size",
    the additional data is ignored.

    Args:
        ilst ([int]) : A list of integers
        size (int)   : Size of each chunk
    """
    return [ilst[i:i+size] for i in range(0, len(ilst), size)]

