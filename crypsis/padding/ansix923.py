"""
Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 00 00 00 04 |
"""

def padding(data, block_size=16):
    """Generates ANSI X.923 padding"""
    data = bytearray(data)
    fill = block_size - (len(data) % block_size)
    assert 0x100 > fill > 0x0
    return bytearray([0x0] * (fill - 1) + [fill])

def pad(data, block_size=16):
    """Adds ANSI X.923 padding"""
    data = bytearray(data)
    return data + padding(data, block_size)

def unpad(data):
    """Strips ANSI X.923 padding from a bytearray"""
    assert isinstance(data, bytearray)
    val = data[-1]
    return data[:-val]

def check(data, block_size=16):
    """Returns true if data is validly ANSI X.923 padded"""
    if len(data) < block_size:
        return False
    if len(data) % block_size != 0:
        return False
    data, val = data[:-1], data[-1]
    if val > block_size:
        return False
    return all([x == 0 for x in data[:-(val - 1)]])
