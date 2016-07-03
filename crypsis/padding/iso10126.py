from os import urandom

"""
Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 81 A6 23 04 |
"""

def padding(data, block_size=16):
    data = bytearray(data)
    fill = block_size - (len(data) % block_size)
    assert 0x100 > fill > 0x0
    return bytearray(urandom(fill - 1)) + bytearray([fill])

def pad(data, block_size=16):
    data = bytearray(data)
    return data + padding(data, block_size=16)

def unpad(data):
    """Strips ISO 10126 padding from a bytearray"""
    assert isinstance(data, bytearray)
    val = data[-1]
    return data[:-val]
