import os
import random

from hypothesis import given
from hypothesis import strategies as st

"""
Test padding oracle on CBC

This test requires pycrypto
"""

from crypsis.cbc.padding_oracle import decrypt_msg
from crypsis.padding.pkcs7 import pad, padding, unpad

from Crypto.Cipher import AES

blocksize  = 16
iv         = os.urandom(blocksize)
cipher     = AES.new(os.urandom(32), AES.MODE_CBC, iv)
plaintext  = os.urandom(random.randrange(1, 1024))
plaintext  = str(pad(plaintext, blocksize))
ciphertext = cipher.encrypt(plaintext)

print ciphertext.encode('hex')

def oracle(ct):
    ct = str(ct)
    assert len(ct) % blocksize == 0
    raw = cipher.decrypt(ct)

    # PKCS7 specific
    val = ord(raw[-1])
    if val > blocksize:
        return False
    if not all(map(lambda x: ord(x) == val, raw[-val:])):
        return False
    return True

decrypt = decrypt_msg(
    ciphertext,
    oracle,
    padding,
    iv=iv,
    block_size=blocksize
)

assert str(decrypt) == str(plaintext)


