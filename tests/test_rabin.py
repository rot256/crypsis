from crypsis import rabin

from hypothesis import note
from hypothesis import given
from hypothesis import strategies as st

@given(
    st.integers(min_value=256, max_value=2**512),
    st.integers(min_value=32, max_value=2**11)
)
def test_rabin(m, b):
    sk, pk = rabin.generate(b)
    m = m % pk
    ct = rabin.encrypt(m, pk)
    pt = rabin.decrypt(ct, sk)
    assert m in pt
