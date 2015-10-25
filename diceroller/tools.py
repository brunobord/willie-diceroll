# -*- coding: utf8 -*-
import re
from rdoclient import RandomOrgClient


REGEXP = re.compile(
    r"(?P<nb>\d*)d(?P<sides>\d+|[fF])?(?P<modifier>[+-]\d+)?$")

FUDGE_FACES = (' ', '+', '-')
FUDGE_SCORES = {' ': 0, '+': 1, '-': -1}


class BadlyFormedExpression(Exception):
    """
    Exception thrown then the roll expression is malformed / invalid
    """


class RollParser(object):
    """
    Parses a dice roll string
    """
    @staticmethod
    def nb(groupnb, sides):
        if sides == 'F':
            if not groupnb:
                return 4
        return int(groupnb) if groupnb else 1

    @staticmethod
    def parse(expr):
        """
        Parse a dice roll expression, return a tuple with (nb, sides, modifier)
        """
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
    """
    Common dice result
    """
    def __init__(self, dicelist, modifier=0):
        self.dicelist = dicelist
        self.modifier = modifier

    @property
    def sum(self):
        """
        Return the sum of all dice + modifier
        """
        return sum(self.dicelist) + self.modifier

    def __repr__(self):
        result = ' + '.join(map(str, self.dicelist))
        if self.modifier:
            if self.modifier > 0:
                result = result + ' (+{})'.format(self.modifier)
            else:
                result = result + ' ({})'.format(self.modifier)
        result = result + ' = {}'.format(self.sum)
        return result


class FudgeDiceResult(DiceResult):
    """
    Dice result class for FudgeDice
    """
    @property
    def fudgesum(self):
        """
        Return the sum of the fudgedice
        """
        dicelist = [FUDGE_SCORES[d] for d in self.dicelist]
        return sum(dicelist)

    @property
    def sum(self):
        """
        Return the sum of all dice + modifier
        """
        return self.fudgesum + self.modifier

    def __repr__(self):
        result = ' '.join('[{}]'.format(d) for d in self.dicelist)
        if self.modifier:
            if self.modifier > 0:
                result = result + ' = {} (+{})'.format(
                    self.fudgesum, self.modifier)
            else:
                result = result + ' = {} ({})'.format(
                    self.fudgesum, self.modifier)
        result = result + ' = {}'.format(self.sum)
        return result


class Roller(object):
    """
    RandomOrg dice Roller
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def roll(self, nb=0, sides=6, modifier=0):
        r = RandomOrgClient(self.api_key)
        if sides == 'F':
            dicelist = r.generate_strings(nb, 1, ' -+')
            return FudgeDiceResult(dicelist, modifier)
        else:
            dicelist = r.generate_integers(nb, 1, sides)
            return DiceResult(dicelist, modifier)
