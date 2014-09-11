import re
REGEXP = re.compile(r"(?P<nb>\d*)d(?P<sides>\d+)?(?P<modifier>[+-]\d+)?$")  # noqa


class Roll(object):
    @staticmethod
    def parse(expr):
        parsed = REGEXP.match(expr)
        groupdict = parsed.groupdict()
        nb = int(groupdict['nb']) if groupdict['nb'] else 1
        sides = int(groupdict['sides']) if groupdict['sides'] else 6  # noqa
        modifier = int(groupdict['modifier']) if groupdict['modifier'] else 0  # noqa
        return nb, sides, modifier
