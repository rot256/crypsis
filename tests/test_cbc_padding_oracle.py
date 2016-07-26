"""
Test padding oracle on CBC

This test requires PyCrypto and patience
"""

from logging import DEBUG, INFO, WARNING

from hypothesis import note
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from Crypto.Cipher import AES
from Crypto.Cipher import DES

from crypsis.exceptions import InvalidPadding
from crypsis.cbc.padding_oracle import decrypt_msg
from crypsis import logger

logger.level = DEBUG

@given(
    st.binary(min_size=16, max_size=16),
    st.binary(min_size=32, max_size=32),
    st.binary(max_size=1024),
    st.integers(min_value=1, max_value=16),
)
def test_cbc_padding_oracle_aes_pkcs7(iv, key, plaintext,threads):
    # Produce target ciphertext
    from crypsis.padding.pkcs7 import pad, unpad, padding
    note('Padding oracle AES/PKCS7')
    note('Plaintext: ' + plaintext.encode('hex'))

    blocksize  = 16
    cipher     = AES.new(key, AES.MODE_CBC, iv)
    plaintext  = str(pad(plaintext, blocksize))
    ciphertext = cipher.encrypt(plaintext)
    note('Padded plaintext: ' + plaintext.encode('hex'))

    # Target oracle
    def oracle(ct):
        ct = bytearray(ct)
        ci = AES.new(key, AES.MODE_CBC, iv)
        pt = ci.decrypt(str(ct))
        try:
            unpad(pt, blocksize)
            return True
        except InvalidPadding:
            return False

    # Attack
    decrypt = decrypt_msg(
        ciphertext,
        oracle,
        padding,
        iv=iv,
        blocksize=blocksize,
        threads=1,
    )
    assert str(decrypt) == str(plaintext)

@given(
    st.binary(min_size=8, max_size=8),
    st.binary(min_size=8, max_size=8),
    st.binary(),
    st.integers(min_value=1, max_value=16),
)
def test_cbc_padding_oracle_des_iso7816(iv, key, plaintext, threads):
    # Produce target ciphertext
    from crypsis.padding.iso7816 import pad, unpad, padding
    note('Padding oracle DES/ISO-7816')
    note('Plaintext: ' + plaintext.encode('hex'))

    blocksize  = 8
    cipher     = DES.new(key, DES.MODE_CBC, iv)
    plaintext  = str(pad(plaintext, blocksize))
    ciphertext = cipher.encrypt(plaintext)
    note('Padded plaintext: ' + plaintext.encode('hex'))

    # Target oracle
    def oracle(ct):
        ct = bytearray(ct)
        ci = DES.new(key, DES.MODE_CBC, iv)
        pt = ci.decrypt(str(ct))
        try:
            unpad(pt, blocksize)
            return True
        except InvalidPadding:
            return False

    # Attack
    decrypt = decrypt_msg(
        ciphertext,
        oracle,
        padding,
        iv=iv,
        blocksize=blocksize,
        threads=1,
    )
    note('Decrypted: ' + decrypt)
    assert str(decrypt) == str(plaintext)

if __name__ == '__main__':
    logger.level = INFO
    test_cbc_padding_oracle_aes_pkcs7()
    test_cbc_padding_oracle_des_iso7816()
