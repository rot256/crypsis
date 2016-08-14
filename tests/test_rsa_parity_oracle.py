from crypsis import *
from crypsis import rsa
from crypsis.rsa import parity_oracle
from crypsis.math import *

from hypothesis import note
from hypothesis import given
from hypothesis import strategies as st

@given(
    st.integers(min_value=2**256, max_value=2**511),
    st.integers(min_value=512, max_value=2048)
)
def test_oracle(msg, keysize):
    # Generate key
    sk, pk = rsa.generate(n=keysize)
    assert bitlen(sk[1]) == keysize
    ct = rsa.encrypt(msg, pk)
    note('Key:')
    note('N:' + hex(sk[1]))
    note('d:' + hex(sk[0]))
    note('e:' + hex(pk[0]))
    note('Cipher text:' + hex(ct))
    
    # Begin attack
    def oracle(m):
        n = rsa.decrypt(m, sk)
        return n % 2
    pt = parity_oracle.decrypt(ct, oracle, pk)
    assert pt == msg
