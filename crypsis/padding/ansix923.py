
def padding(data, block_size=16):
    data = bytearray(data)
    fill = block_size - (len(data) % block_size)
    assert 0x100 > fill > 0x0
    return bytearray([0x0] * (fill - 1) + [fill])

def pad(data, block_size=16):
    data = bytearray(data)
    return data + padding(data, block_size)

def unpad(data):
    """Strips ANSI X.923 padding from a bytearray"""
    assert isinstance(data, bytearray)
    val = data[-1]
    return data[:-val]
