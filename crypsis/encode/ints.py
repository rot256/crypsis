"""
Encode an decode raw integer values
"""

def to_bytes(val):
    """
    Convert val to a bigendian byte array

    Note:
        Also accepts longs and mpz objects

    Args:
        val (int): Value to encode

    Returns:
        A bytearray representing val
    """
    try:
        return bytearray(('%x' % val).decode('hex'))
    except TypeError:
        return bytearray(('0%x' % val).decode('hex'))

def from_bytes(val):
    """
    Decode bytearray into integer

    Args:
        val: Value to decode (str, list, bytearray)
    
    Returns:
        An integer representing val in bigendian format
    """
    val = bytearray(val)
    return int(str(val).encode('hex'), 16)
