"""
Test symmetric padding
"""

from hypothesis import given
from hypothesis import strategies as st

### PKCS 7 ###

from crypsis.padding.pkcs7 import pad
from crypsis.padding.pkcs7 import unpad

@given(
    st.binary(),
    st.integers(min_value=1, max_value=255))
def test_pkcs7_1(msg, block_size):
    padded = pad(msg, block_size=block_size)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded)) == bytearray(msg)

@given(
    st.lists(st.integers(min_value=1, max_value=255)),
    st.integers(min_value=2, max_value=255))
def test_pkcs7_2(msg, block_size):
    padded = pad(msg, block_size=block_size)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded)) == bytearray(msg)

### ISO 7816 ###

from crypsis.padding.iso7816 import pad
from crypsis.padding.iso7816 import unpad

@given(
    st.binary(),
    st.integers(min_value=1, max_value=255))
def test_iso7816_1(msg, block_size):
    padded = pad(msg, block_size=block_size)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded)) == bytearray(msg)

@given(
    st.lists(st.integers(min_value=1, max_value=255)),
    st.integers(min_value=2, max_value=255))
def test_iso7816_2(msg, block_size):
    padded = pad(msg, block_size=block_size)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded)) == bytearray(msg)

### ANSI X.923 ###

from crypsis.padding.ansix923 import pad
from crypsis.padding.ansix923 import unpad

@given(
    st.binary(),
    st.integers(min_value=1, max_value=255))
def test_ansix923_1(msg, block_size):
    padded = pad(msg, block_size=block_size)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded)) == bytearray(msg)

@given(
    st.lists(st.integers(min_value=1, max_value=255)),
    st.integers(min_value=2, max_value=255))
def test_ansix923_2(msg, block_size):
    padded = pad(msg, block_size=block_size)
    assert len(padded) > len(msg)
    assert bytearray(unpad(padded)) == bytearray(msg)
