# -*- coding: utf8 -*-
import re
REGEXP = re.compile(
    r"(?P<nb>\d*)d(?P<sides>\d+)?(?P<modifier>[+-]\d+)?$")


class BadlyFormedExpression(Exception):
    """
    Exception thrown then the roll expression is malformed / invalid
    """


class Roll(object):
    @staticmethod
    def parse(expr):
        parsed = REGEXP.match(expr)
        if not parsed:
            raise BadlyFormedExpression(u"Impossible to parse {}".format(expr))
        groupdict = parsed.groupdict()
        nb = int(groupdict['nb']) if groupdict['nb'] else 1
        sides = int(groupdict['sides']) if groupdict['sides'] else 6  # noqa
        modifier = int(groupdict['modifier']) if groupdict['modifier'] else 0  # noqa
        return nb, sides, modifier
