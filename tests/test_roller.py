import random
import mock
from diceroller.tools import Roller


def fake_generate_integers(self, nb, minimum, maximum, *args, **kwargs):
    dicelist = [random.randint(minimum, maximum) for x in range(nb)]
    return dicelist


@mock.patch(
    'rdoclient.RandomOrgClient.generate_integers', fake_generate_integers
)
def test_d6():
    roller = Roller("fake api key")
    for x in range(25000):
        result = roller.roll(nb=2, sides=6, modifier=0)
        assert 2 <= result.sum <= 12
