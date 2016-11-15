"""
Core Rabin functions

This implementation is used for testing
and as a building block in exploits...

THESE FUNCTIONS ARE NOT SAFE FOR CRYPTOGRAPHIC USE.
"""

from gmpy2 import invert
from crypsis.math import primes, sqrt_mod, crt
from crypsis.encode import bit_size
from crypsis import logger

def generate(n=2048, fast=False):
    """
    Generates a Rabin key pair of exactly n bits
    """
    mp = n // 2
    mq = mp + 1 if n % 2 else mp
    p = primes.random(mp)
    q = primes.random(mq)
    N = p * q
    if bit_size(N) != n:
        return generate(n, fast)
    return (p, q, N), N

def encrypt(m, pk):
    return pow(m, 2, pk)

def decrypt(c, sk):
    # Find squares
    p, q, N = sk
    mp = sqrt_mod(c, p)
    mq = sqrt_mod(c, q)
    
    # Apply CRT
    q_inv = invert(q, p)
    p_inv = invert(p, q)
    r = (p_inv * p * mq + q_inv * q * mp) % N
    s = (p_inv * p * mq - q_inv * q * mp) % N

    # Return 4 possible plaintexts
    return (r, N - r, s, N - s)
