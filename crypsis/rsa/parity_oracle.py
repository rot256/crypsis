from crypsis.rsa import encrypt
from crypsis.math import bitlen
from crypsis import logger

def decrypt(m, query, pk):
    _, N = pk
    assert m < N
    double = encrypt(2, pk)
    logger.info('Running RSA parity oracle...')
    
    # Edge case
    if m == 1:
        return 1

    # Binary search for plaintext
    s = 1
    for i in range(bitlen(N)):
        m = (m * double) % N
        s <<= 1
        if query(m) == 0:
            s -= 1
        logger.debug('Upper bound: %x' % ((s * N) >> (i+1)))
    return (s * N) >> (i+1)
