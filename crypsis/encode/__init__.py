# Returns the bit length of n
def bit_size(n):
    """Returns the length in bits of an integer.
    
    Args:
        n (int): A non-negative integer

    Returns:
        An integer equal to the minimum number 
        of bits required to store the value
        return 0 for n = 0.
    """
    l = 0
    while n:
        n >>= 1
        l += 1
    return l

# Returns the byte length of n
def byte_size(n):
    l = 0
    while n:
        n >>= 8
        l += 1
    return l
