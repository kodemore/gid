from copy import copy
from random import shuffle
import time

import pytest

from gid.guid import Guid, base62_decode, base62_encode


def test_base62_value() -> None:
    assert "1" == base62_encode(1)
    assert "z" == base62_encode(61)
    assert "10" == base62_encode(62)
    assert "11" == base62_encode(63)


def test_base62_encode_decode() -> None:
    timestamp = int(time.time() * 1000)
    decoded = base62_encode(timestamp)
    assert base62_decode(decoded) == timestamp


def test_generate_guid() -> None:
    values = []
    for i in range(0, 1000):
        values.append(Guid())

    assert len(values) == len(tuple(values))
    print(values)

    previous = None
    for current in values:
        if not previous:
            previous = current
            continue
        assert current > previous


def test_recreate_guid() -> None:
    generated_id = Guid()
    recreated_id = Guid(str(generated_id))

    assert generated_id.timestamp == recreated_id.timestamp
    assert generated_id == recreated_id


def test_fail_on_invalid_guid() -> None:
    with pytest.raises(ValueError):
        guid = Guid("invalidGuid")


def test_guid_is_sortable() -> None:
    original_guid = [
        'ShjZz5Dvr0JyJL00',
        'Shja07nr23XgJk00',
        'Shja1AOUhKufOh00',
        'Shja2CxdQ0AgNa00',
        'Shja3FWSn2wuWu00',
        'Shja4I6kVG860e00'
    ]
    guid_shuffled = copy(original_guid)
    shuffle(guid_shuffled)

    sorted(guid_shuffled)

    assert sorted(guid_shuffled) == original_guid


def test_fail_comparison_on_non_compatible_types() -> None:
    with pytest.raises(TypeError):
        assert not Guid() > "3"

    with pytest.raises(TypeError):
        assert not Guid() < "3"
