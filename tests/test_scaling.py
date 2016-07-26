"""
Test scaling features
"""

import random

from hypothesis import given
from hypothesis import note
from hypothesis import strategies as st

import crypsis.scaling as scaling

@given(
    st.integers(min_value=1, max_value=64),
    st.lists(st.tuples(
        st.integers(),
        st.integers(min_value=0),
        st.integers(min_value=1))))
def test_scaling_map(threads, vals):
    note('Mapping with %d threads' % threads)
    def funcer(t):
        m, p, n = t
        return pow(m, p, n)
    res = scaling.map(funcer, vals, threads=threads)
    assert set(res) == set(map(funcer, vals))

@given(
    st.lists(st.integers(), min_size=1),
    st.integers(min_value=1, max_value=64))
def test_scaling_search(vals, threads):
    note('Searching with %d threads' % threads)
    good = random.choice(vals)
    def funcer(t):
        return t == good
    res = scaling.search(funcer, vals, threads=threads)
    assert res == good

if __name__ == '__main__':
    test_scaling_map()
    test_scaling_search()
