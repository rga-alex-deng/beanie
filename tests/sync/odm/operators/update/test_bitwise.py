from beanie.odm.operators.update.bitwise import Bit
from tests.sync.models import Sample


def test_bit():
    q = Bit({Sample.integer: 2})
    assert q == {"$bit": {"integer": 2}}
