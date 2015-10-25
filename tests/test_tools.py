from tools import Roll


def test_tools():
    nb, sides, modifier = Roll.parse('2d6')
    assert (nb, sides, modifier) == (2, 6, 0)

    nb, sides, modifier = Roll.parse('2d')
    assert (nb, sides, modifier) == (2, 6, 0)

    nb, sides, modifier = Roll.parse('2d1')
    assert (nb, sides, modifier) == (2, 1, 0)

    nb, sides, modifier = Roll.parse('2d6+3')
    assert (nb, sides, modifier) == (2, 6, 3)

    nb, sides, modifier = Roll.parse('2d6-1')
    assert (nb, sides, modifier) == (2, 6, -1)

    nb, sides, modifier = Roll.parse('2d6+0')
    assert (nb, sides, modifier) == (2, 6, 0)
