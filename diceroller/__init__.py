# -*- coding: utf8 -*-
"""
diceroller.py - Sopel Direroll Module
Copyright 2014, Bruno Bord
Licensed under the WTFPL.

"""
from __future__ import unicode_literals, absolute_import

from sopel.module import commands
from rdoclient import RandomOrgClient

from .tools import Roll, BadlyFormedExpression


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
    try:
        result = Roll.parse(expr)
    except BadlyFormedExpression, exc:
        bot.reply(exc)
        bot.reply("Can't roll dice")
        return
    nb, sides, modifier = result
    if sides == 'F':
        bot.reply("Not implemented yet")
        return
    r = RandomOrgClient(bot.config.diceroll.api_key)
    rolls = r.generate_integers(nb, 1, sides)
    total = sum(rolls) + modifier
    roll_list = " + ".join(map(str, rolls))
    if nb == 1:
        msg = "Your roll: %s" % roll_list
    else:
        msg = "Your rolls: %s" % roll_list
    if modifier:
        if modifier > 0:
            msg += " (+%d)" % modifier
        else:
            msg += " (%d)" % modifier
    if nb > 1:
        msg += " = %d" % total
    bot.reply(msg)
