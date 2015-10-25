# -*- coding: utf8 -*-
import pytest
from diceroller.tools import Roll, BadlyFormedExpression


def test_tools():
    nb, sides, modifier = Roll.parse('2d6')
    assert (nb, sides, modifier) == (2, 6, 0)

    nb, sides, modifier = Roll.parse('2d')
    assert (nb, sides, modifier) == (2, 6, 0)

    nb, sides, modifier = Roll.parse('2d1')
    assert (nb, sides, modifier) == (2, 1, 0)

    nb, sides, modifier = Roll.parse('d6')
    assert (nb, sides, modifier) == (1, 6, 0)

    nb, sides, modifier = Roll.parse('2d6+3')
    assert (nb, sides, modifier) == (2, 6, 3)

    nb, sides, modifier = Roll.parse('2d6-1')
    assert (nb, sides, modifier) == (2, 6, -1)

    nb, sides, modifier = Roll.parse('2d6+0')
    assert (nb, sides, modifier) == (2, 6, 0)


def test_tools_tricks():
    nb, sides, modifier = Roll.parse('0d6')
    assert (nb, sides, modifier) == (0, 6, 0)

    nb, sides, modifier = Roll.parse('0d0')
    assert (nb, sides, modifier) == (0, 0, 0)


def test_tools_hellish():
    with pytest.raises(BadlyFormedExpression):
        Roll.parse(u'2d6°')

    with pytest.raises(BadlyFormedExpression):
        Roll.parse('2dA')

    with pytest.raises(BadlyFormedExpression):
        Roll.parse('2')
