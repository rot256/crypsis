import os

def random(size, exclude=[]):
    out = bytearray([])
    exclude = set(exclude)
    assert isinstance(size, int)
    while len(out) < size:
        byte = os.urandom(1)
        if byte not in exclude:
            out.append(byte)
    return out

def explode(bstr):
    assert type(bstr) in (bytearray, str, bytes, unicode)
    return map(ord, bstr)

def implode(ilst):
    """ Implodes a list of integers into a single binary string """
    return bytearray(ilst)

def chop(ilst, size):
    """ Chops an integer list into fixed size blocks
    If the list length is not a multiple of "size",
    the additional data is ignored.

    Args:
        ilst ([int]) : A list of integers
        size (int)   : Size of each chunk
    """
    return [ilst[i:i+size] for i in range(0, len(ilst), size)]

