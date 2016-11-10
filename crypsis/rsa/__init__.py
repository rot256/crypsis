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
from crypsis.math import primes
from crypsis.encode import bit_size
from crypsis import logger

def generate(n=2048, e=65537):
    """
    Generates an RSA key pair of exactly n bits
    """
    mp = n // 2
    mq = mp + 1 if n % 2 else mp
    p = primes.random(mp)
    q = primes.random(mq)
    if bit_size(p * q) != n:
        return generate(n, e)
    try:
        d = invert(e, (p-1) * (q-1))
    except:
        return generate(n, e)
    N = p * q
    return (p, q, d, N), (e, N)

def decrypt_crt(m, sk):
    p, q, d, N = sk
    mp = pow(m, d, p)
    mq = pow(m, d, q)
    rp = invert(p, q)
    rq = invert(q, p)
    return (mp * q * rq + mq * p * rp) % N

def encrypt(m, pk):
    e, N = pk
    return pow(m, e, N)

def decrypt(m, sk):
    _, _, d, N = sk
    return pow(m, d, N)

def sign(m, sk):
    return decrypt(m, sk)

def verify(m, sig, pk):
    return m == encrypt(sig, pk)
