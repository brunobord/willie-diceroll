# -*- coding: utf8 -*-
import re
from rdoclient import RandomOrgClient


REGEXP = re.compile(
    r"(?P<nb>\d*)d(?P<sides>\d+|[fF])?(?P<modifier>[+-]\d+)?$")


class BadlyFormedExpression(Exception):
    """
    Exception thrown then the roll expression is malformed / invalid
    """


class RollParser(object):

    @staticmethod
    def nb(groupnb, sides):
        if sides == 'F':
            if not groupnb:
                return 4
        return int(groupnb) if groupnb else 1

    @staticmethod
    def parse(expr):
        parsed = REGEXP.match(expr)
        if not parsed:
            raise BadlyFormedExpression(
                u"Invalid dice expression: `{}`".format(expr))
        groupdict = parsed.groupdict()
        if groupdict['sides'] not in ('f', 'F'):
            sides = int(groupdict['sides']) if groupdict['sides'] else 6  # noqa
        else:
            sides = 'F'
        nb = RollParser.nb(groupdict['nb'], sides)
        modifier = int(groupdict['modifier']) if groupdict['modifier'] else 0  # noqa
        return nb, sides, modifier


class DiceResult(object):
    def __init__(self, dicelist, modifier=0):
        self.dicelist = dicelist
        self.modifier = modifier

    @property
    def sum(self):
        return sum(self.dicelist) + self.modifier


class Roller(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def roll(self, nb=0, sides=6, modifier=0):
        r = RandomOrgClient(self.api_key)
        dicelist = r.generate_integers(nb, 1, sides)
        return DiceResult(dicelist, modifier)
