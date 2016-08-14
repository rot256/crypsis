"""
Core RSA functions

This implementation is used for testing
and as a building block in exploits...

THESE FUNCTIONS ARE NOT SAFE 
FOR CRYPTOGRAPHIC USE, 
FOR A NUMBER OF REASONS.
"""

from gmpy2 import invert
from random import randrange, getrandbits
from crypsis.math import primes, bitlen
from crypsis import logger

def generate(n=2048, e=65537):
    """
    Generates an RSA key pair of exactly n bits
    """
    mp = n // 2
    mq = mp + 1 if n % 2 else mp
    p = primes.random(mp)
    q = primes.random(mq)
    if bitlen(p * q) != n:
        return generate(n, e)
    print 'RSA p: 0x%x' % p
    print 'RSA q: 0x%x' % q
    d = invert(e, (p-1) * (q-1))
    N = p * q
    return (d, N), (e, N)

def encrypt(m, pk):
    e, N = pk
    return pow(m, e, N)

def decrypt(m, sk):
    d, N = sk
    return pow(m, d, N)

def sign(m, sk):
    return decrypt(m, sk)

def verify(m, sig, pk):
    return m == encrypt(sig, pk)
