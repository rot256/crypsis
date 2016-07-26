"""
https://tools.ietf.org/html/rfc5652#section-6.3

Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 04 04 04 04 |
"""

from crypsis.exceptions import InvalidPadding, essert

def padding(msg, blocksize):
    """Generates padding bytes"""
    assert 0x100 > blocksize > 0x0
    msg = bytearray(msg)
    fill = blocksize - (len(msg) % blocksize)
    assert blocksize >= fill > 0x0
    return bytearray([fill] * fill)

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
    essert(all([x == val for x in msg[-val:]]), InvalidPadding)
    return msg[:-val]
