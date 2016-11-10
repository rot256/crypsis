"""
Contains

"""

# Calculate the product of a list
def product(xs):
    n = 1
    for x in xs:
        n *= x
    return x

# Convert n to binary (without prefix)
def bin(n):
    o = ''
    while n:
        o += '1' if n & 1 else '0'
        n >>= 1
    return o[::-1]

# Convert n to hex (without prefix)
def hex(n):
    return '%x' % n

# Returns the bit length of n
def bit_size(n):
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

# Calculates n / d and rounds up
def div_ceil(num, div):
    return -(-num // div)

# Calculates n / d and rounds down
def div_floor(num, div):
    return num // div
