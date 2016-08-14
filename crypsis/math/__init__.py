"""
Contains

"""


# Calculate the product of a list
# Like sum -- why is this not a buildin?
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
def bitlen(n):
    l = 0
    while n:
        n >>= 1
        l += 1
    return l
