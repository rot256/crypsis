"""
Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 80 00 00 00 |
"""

def padding(data, block_size=16):
    """Generates ISO 7816-4 padding"""
    data = bytearray(data)
    fill = block_size - (len(data) % block_size)
    assert 0x100 > fill > 0x0
    return bytearray([0x80] + [0x00] * (fill - 1))

def pad(data, block_size=16):
    """Adds ISO 7816-4 padding to the message"""
    data = bytearray(data)
    return data + padding(data, block_size)

def unpad(data):
    """Strips ISO 7816-4 padding from a bytearray"""
    assert isinstance(data, bytearray)
    while data[-1] != 0x80:
        data = data[:-1]
    return data[:-1]
