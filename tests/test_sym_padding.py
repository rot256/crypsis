"""
Test symmetric padding
"""

from os import urandom
from hypothesis import given
from hypothesis import strategies as st

### PKCS 7 ###

from crypsis.padding.pkcs7 import pad
from crypsis.padding.pkcs7 import unpad

@given(
    st.binary(),
    st.integers(min_value=1, max_value=255))
def test_pkcs7_1(msg, blocksize):
    padded = pad(msg, blocksize=blocksize)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded, blocksize)) == bytearray(msg)

@given(
    st.lists(st.integers(min_value=1, max_value=255)),
    st.integers(min_value=1, max_value=255))
def test_pkcs7_2(msg, blocksize):
    padded = pad(msg, blocksize=blocksize)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded, blocksize)) == bytearray(msg)

def test_pkcs7_3():
    # Valid padding
    good = [
        '5cab3f4fcee129181c7f8f79ccccca2b10101010101010101010101010101010'
    ]
    good = map(lambda x: x.decode('hex'), good)
    tester = lambda x: unpad(x, 16)
    map(tester, good)

    # Invalid padding
    bad = [
        '0a896c9467db4d78f211ef88928f783513101010101010101010101010101010'
    ]
    bad = map(lambda x: x.decode('hex'), bad)
    tester = lambda x: unpad(x, 16)
    for b in bad:
        try:
            tester(b)
            assert False
        except:
            pass

### ISO 7816 ###


### ANSI X.923 ###

if __name__ == '__main__':
    test_pkcs7_1()
    test_pkcs7_2()
    test_pkcs7_3()

