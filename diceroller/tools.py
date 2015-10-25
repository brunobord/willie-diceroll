# -*- coding: utf8 -*-
import re
REGEXP = re.compile(
    r"(?P<nb>\d*)d(?P<sides>\d+|[fF])?(?P<modifier>[+-]\d+)?$")


class BadlyFormedExpression(Exception):
    """
    Exception thrown then the roll expression is malformed / invalid
    """



class Roll(object):

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
        nb = Roll.nb(groupdict['nb'], sides)
        modifier = int(groupdict['modifier']) if groupdict['modifier'] else 0  # noqa
        return nb, sides, modifier
