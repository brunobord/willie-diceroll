# coding: utf8
"""
diceroll.py - Willie Direcroll Module
Copyright 2014, Bruno Bord
Licensed under the WTFPL.

"""
from __future__ import unicode_literals, absolute_import

from willie.module import commands

import re
from rdoclient import RandomOrgClient


REGEXP = re.compile(r"(?P<nb>\d*)d(?P<sides>\d+)?(?P<modifier>[+-]\d+)?$")  # noqa


class Roll(object):
    """
    >>> TESTS = (
    ...     {'expr': '2d6', 'sides': '6', 'nb': '2', 'modifier': None},
    ...     {'expr': 'd10', 'sides': '10', 'nb': '', 'modifier': None},
    ...     {'expr': '2d6+1', 'sides': '6', 'nb': '2', 'modifier': '+1'},
    ...     {'expr': '2d6-1', 'sides': '6', 'nb': "2", 'modifier': '-1'},
    ...     {'expr': 'd', 'sides': None, 'nb': "", 'modifier': None},
    ...     {'expr': '2d', 'sides': None, 'nb': "2", 'modifier': None},
    ... )

    >>> for test in TESTS:
    ...     parsed = REGEXP.match(test['expr'])
    ...     groupdict = parsed.groupdict()
    ...     for k, v in groupdict.items():
    ...         assert test[k] == v
    """

    @staticmethod
    def parse(expr):
        """
        >>> TESTS = (
        ...     {'expr': '2d6', 'sides': 6, 'nb': 2, 'modifier': 0},
        ...     {'expr': 'd10', 'sides': 10, 'nb': 1, 'modifier': 0},
        ...     {'expr': '2d6+1', 'sides': 6, 'nb': 2, 'modifier': 1},
        ...     {'expr': '2d6-1', 'sides': 6, 'nb': 2, 'modifier': -1},
        ...     {'expr': 'd', 'sides': 6, 'nb': 1, 'modifier': 0},
        ...     {'expr': '2d', 'sides': 6, 'nb': 2, 'modifier': 0},
        ... )

        >>> for test in TESTS:
        ...     nb, sides, modifier = Roll.parse(test['expr'])
        ...     assert nb == test['nb']
        ...     assert sides == test['sides']
        ...     assert modifier == test['modifier'], "#%s# #%s#" % (modifier, test['modifier'])  # noqa

        """
        parsed = REGEXP.match(expr)
        groupdict = parsed.groupdict()
        nb = int(groupdict['nb']) if groupdict['nb'] else 1
        sides = int(groupdict['sides']) if groupdict['sides'] else 6  # noqa
        modifier = int(groupdict['modifier']) if groupdict['modifier'] else 0  # noqa
        return nb, sides, modifier


def configure(config):
    """
    | [diceroll]   | example | purpose |
    | ------------ | ------- | ------- |
    | api_key      | YOURKEY | You API KEY |
    """
    config.interactive_add('diceroll', 'api_key', "Set the random.org API KEY")


@commands('roll')
def roll(bot, trigger):
    """Roll the dice"""
    expr = trigger.group(2)
    result = Roll.parse(expr)
    if not result:
        bot.reply("Can't roll dice")
        return
    nb, sides, modifier = result
    r = RandomOrgClient(bot.config.diceroll.api_key)
    rolls = r.generate_integers(nb, 1, sides)
    total = sum(rolls) + modifier
    roll_list = " + ".join(map(str, rolls))
    msg = "Your rolls: %s" % roll_list
    if modifier:
        if modifier > 0:
            msg += " (+%d)" % modifier
        else:
            msg += " (%d)" % modifier
    msg += " = %d" % total
    bot.reply(msg)
