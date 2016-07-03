"""
https://tools.ietf.org/html/rfc5652#section-6.3

Example:
| DD DD DD DD DD DD DD DD | DD DD DD DD 04 04 04 04 |
"""

def padding(data, block_size=16):
    """Generates PKCS#7 padding"""
    data = bytearray(data)
    fill = block_size - (len(data) % block_size)
    assert 0x100 > fill > 0x0
    return bytearray([fill] * fill)

def pad(data, block_size=16):
    """Adds PKCS7 padding to the messsage"""
    data = bytearray(data)
    return data + padding(data, block_size)

def unpad(data):
    """Strips PKCS7 padding from a bytearray"""
    assert isinstance(data, bytearray)
    val = data[-1]
    return data[:-val]
