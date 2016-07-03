"""
Test symmetric padding
"""

from hypothesis import given
from hypothesis import strategies as st

from crypsis.misc import explode, implode

@given(st.text())
def _test_explode1(text):
    exp = explode(text)
    assert isinstance(exp, list)
    if len(exp) > 0:
        assert isinstance(exp[0], int)
    assert len(exp) == len(text)
    imp = implode(text)
    assert len(imp) == len(text)
    assert str(imp) == str(text)
