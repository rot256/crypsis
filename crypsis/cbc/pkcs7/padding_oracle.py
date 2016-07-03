import os
from crypsis import logger
from crypsis.scaling import search
from crypsis.misc import xor, rand, implode, explode, chop

def genpad(size, block_size):
    return ([0] * (block_size - size)) + ([size] * size)

def decrypt(iv, block, query, block_size, threads):
    null = []
    plain = []
    assert isinstance(iv, list)
    def gen_queries(tmp, index):
        for byte in range(0x100):
            test = list(tmp)
            test[block_size - index] = byte
            logger.debug('Attempt byte: 0x%02x', byte)
            yield (byte, implode(test + block))
    work = lambda (b, msg): query(msg)
    for p in range(1, block_size + 1):
        tmp = rand(block_size - len(null)) + null
        tmp = xor(tmp, genpad(p, block_size))
        logger.debug('Plaintext: %s', str(map(chr, plain)))
        logger.info('Decrypting index %d', block_size - p)
        found = search(work, gen_queries(tmp, p), threads)
        if found is None:
            logger.error('Failed to decrypt byte')
            raise ValueError
        byte, _ = found
        char = byte ^ iv[block_size - p] ^ p
        plain = [char] + plain
        null = [byte ^ p] + null
    return plain

def decrypt_block(iv, block, query, block_size = 16, threads = 1):
    iv, block = explode(iv), explode(block)
    assert len(iv) == len(block)
    return implode(decrypt(iv, block, query, block_size, threads))

def decrypt_msg(msg, query, iv = None, block_size = 16, threads = 1):
    assert len(msg) % block_size == 0
    assert len(msg) > block_size
    blocks = chop(explode(msg), block_size)
    pairs = zip(blocks, blocks[1:])
    logger.info('Decrypting %d block of data using a padding oracle' % len(pairs))
    out = ''
    n = 1
    for (iv, block) in pairs:
        logger.info('Decrypting block %d' % n)
        out += implode(decrypt(iv, block, query, block_size, threads))
        logger.info('Decrypted block: %s' % out[-block_size:])
        n += 1
    return out
