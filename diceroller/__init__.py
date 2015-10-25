# -*- coding: utf8 -*-
"""
diceroller.py - Sopel Direroll Module
Copyright 2014-2015, Bruno Bord
Licensed under the WTFPL.

"""
from __future__ import unicode_literals, absolute_import

from sopel.module import commands

from .tools import RollParser, Roller, BadlyFormedExpression


def configure(config):
    """
    | [diceroll]   | example | purpose |
    | ------------ | ------- | ------- |
    | api_key      | YOURKEY | You API KEY |
    """
    config.interactive_add('diceroll', 'api_key', "Set the random.org API KEY")


@commands('roll')
def roll(bot, trigger):
    """
Roll the dice.
By default, it rolls 6-side-dice.

e.g:
.roll 3d
.roll 2d6-1
.roll 3d10+5

It can also roll Fudge dice:
.roll df
"""
    expr = trigger.group(2)
    try:
        result = RollParser.parse(expr)
    except BadlyFormedExpression, exc:
        bot.reply(exc)
        bot.reply("Can't roll dice")
        return
    nb, sides, modifier = result

    roller = Roller(bot.config.diceroll.api_key)
    rolls = roller.roll(nb, sides, modifier)
    if nb == 1:
        msg = "Your roll: %s" % rolls
    else:
        msg = "Your rolls: %s" % rolls
    bot.reply(msg)
