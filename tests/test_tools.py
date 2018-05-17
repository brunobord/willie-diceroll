# -*- coding: utf8 -*-
import pytest
from diceroller.tools import (
    MAX_SIDES, MAX_DICE_NUMBER,
    RollParser, BadlyFormedExpression,
)


def test_tools():
    nb, sides, modifier = RollParser.parse('2d6')
    assert (nb, sides, modifier) == (2, 6, 0)

    nb, sides, modifier = RollParser.parse('2d')
    assert (nb, sides, modifier) == (2, 6, 0)

    nb, sides, modifier = RollParser.parse('d6')
    assert (nb, sides, modifier) == (1, 6, 0)

    nb, sides, modifier = RollParser.parse('2d6+3')
    assert (nb, sides, modifier) == (2, 6, 3)

    nb, sides, modifier = RollParser.parse('2d6-1')
    assert (nb, sides, modifier) == (2, 6, -1)

    nb, sides, modifier = RollParser.parse('2d6+0')
    assert (nb, sides, modifier) == (2, 6, 0)


def test_0d():
    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('0d6')

    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('0d0')


def test_too_many_dice():
    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('{}d6'.format(MAX_DICE_NUMBER+1))


def test_tools_hellish():
    with pytest.raises(BadlyFormedExpression):
        RollParser.parse(u'2d6°')

    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('2dA')

    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('2')


def test_fudge():
    nb, sides, modifier = RollParser.parse('df')
    assert (nb, sides, modifier) == (4, 'F', 0)

    nb, sides, modifier = RollParser.parse('2df')
    assert (nb, sides, modifier) == (2, 'F', 0)

    nb, sides, modifier = RollParser.parse('dF')
    assert (nb, sides, modifier) == (4, 'F', 0)

    nb, sides, modifier = RollParser.parse('2dF')
    assert (nb, sides, modifier) == (2, 'F', 0)


def test_d1():
    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('1d1')


def test_too_many_sides():
    with pytest.raises(BadlyFormedExpression):
        RollParser.parse('1d{}'.format(MAX_SIDES+1))
