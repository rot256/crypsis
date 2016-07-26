"""
Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 80 00 00 00 |
"""

from crypsis.exceptions import InvalidPadding, essert

def padding(msg, blocksize):
    """Generates padding bytes"""
    assert 0x100 > blocksize > 0x0
    msg = bytearray(msg)
    fill = blocksize - (len(msg) % blocksize)
    assert blocksize >= fill > 0x0
    return bytearray([0x80] + [0x00] * (fill - 1))

def pad(msg, blocksize):
    """Adds padding to a messsage"""
    assert 0x100 > blocksize > 0x0
    msg = bytearray(msg)
    msg = msg + padding(msg, blocksize)
    assert len(msg) % blocksize == 0
    return msg

def unpad(msg, blocksize):
    """Verifies and strips padding from a message"""
    assert 0x100 > blocksize > 0x0
    msg = bytearray(msg)
    essert(len(msg) >= blocksize, InvalidPadding)
    essert(len(msg) % blocksize == 0, InvalidPadding)
    msg = bytearray(msg)
    for _ in range(blocksize):
        if msg[-1] != 0x00:
            essert(msg[-1] == 0x80, InvalidPadding)
            return msg[:-1]
        msg = msg[:-1]
    raise InvalidPadding
