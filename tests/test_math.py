from hypothesis import note
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from crypsis.math import div_ceil, div_floor, sqrt_mod

@given(
    st.integers(),
    st.integers(),
)
def test_div_up(top, bot):
    note('%d / %d' % (top, bot))
    if bot == 0:
        return
    ratio = div_ceil(top, bot)
    assert ratio >= top // bot
    assert ratio - 1 <= top // bot
    if top % bot == 0 and abs(bot) > 1:
        assert ratio == top // bot

@given(
    st.integers(),
    st.integers(),
)
def test_div_down(top, bot):
    note('%d / %d' % (top, bot))
    if bot == 0:
        return
    ratio = div_floor(top, bot)
    assert ratio <= top // bot
    assert ratio + 1 >= top // bot
    if top % bot == 0 and abs(bot) > 1:
        assert ratio == top // bot

def test_sqrt_mod():
    tests = [
        (32, 
         3642480029),
        (544444444, 
         3642480029),
        (2, 
         3642480029),
        (1337, 
         4980273906768962942352214838261),
        (6374637653745735643643, 
         1191579233142480640273208371995915017508695872855742116459009),
        (1, 
         1029172077848948395257994416535575711810761280388709917322399),
        (5474687548758674557699999999999999999999999999999999999999999999, 
         1202859343338774738557564134627043556833829768867657339410123313809671454239754227181947386631749913019565818024080912602422663027),
        (2367426723643273637264724637, 
         6406561088971089257876527943560721189101201656606258981122019180377211033444397291111441235565154588078904841478685634105470914772696497620586575521724839),
        (547458654768548764587648776586748654605468849684568948496859, 
         56061774205101364188571349778394416555371955560855463284810121732428337964648441957579006225570025417715029162397190405038667882361317494152059089409561416498282192631155828358867036908790261166037389536739107445626558866811560210668793422510192327413230145442520350919647058534472627999303492191567666359819),
    ]
    for s, p  in tests:
        s = s % p
        c = pow(s, 2, p)
        r = sqrt_mod(c, p)
        assert pow(r, 2, p) == c