from crypsis import rsa
from crypsis.math import bitlen

from hypothesis import note
from hypothesis import given
from hypothesis import strategies as st

@given(
    st.integers(min_value=256, max_value=4096)
)
def test_encrypt(n):
    msg = 0x13313371337
    sk, pk = rsa.generate(n)
    note('Key:')
    note('N: 0x%x' % sk[1])
    note('d: 0x%x' % sk[0])
    note('e: 0x%d' % pk[0])
    _, N = pk
    assert bitlen(N) >= bitlen(msg)
    ct = rsa.encrypt(msg, pk)
    pt = rsa.decrypt(ct, sk)
    assert pt == msg

@given(
    st.integers(min_value=256, max_value=4096)
)
def test_sign(n):
    msg = 0x13313371337
    sk, pk = rsa.generate(n)
    note('Key:')
    note('N: 0x%x' % sk[1])
    note('d: 0x%x' % sk[0])
    note('e: 0x%d' % pk[0])
    _, N = pk
    assert bitlen(N) >= bitlen(msg)
    sig = rsa.sign(msg, sk)
    assert rsa.verify(msg, sig, pk)
