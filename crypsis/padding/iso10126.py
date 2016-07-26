"""
Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 81 A6 23 04 |
"""

from os import urandom
from crypsis.exceptions import InvalidPadding, essert

def padding(msg, blocksize):
    """Generates padding bytes"""
    assert 0x100 > blocksize > 0x0
    msg = bytearray(msg)
    fill = blocksize - (len(msg) % blocksize)
    assert blocksize >= fill > 0x0
    return bytearray(urandom(fill - 1)) + bytearray([fill])

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
    val = msg[-1]
    essert(len(msg) >= blocksize, InvalidPadding)
    essert(len(msg) % blocksize == 0, InvalidPadding)
    essert(val <= blocksize, InvalidPadding)
    return msg[:-val]
