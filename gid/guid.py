import random
import threading
import time
from typing import List

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE62_LENGTH = 62
HASH_LENGTH = 9
TIME_BYTES = 7
UNIQUENESS_LEVEL = 2


def _time_ms() -> int:
    return int(time.time() * 1000)


def base62_encode(value: int) -> str:
    result = ""
    while value >= BASE62_LENGTH:
        letter_position = int(value % BASE62_LENGTH)
        value = int(value / BASE62_LENGTH)
        result += BASE62[letter_position]

    if value > 0:
        result += BASE62[value]

    return result[::-1]


def base62_decode(value: str) -> int:
    base = len(value)
    result = 0
    for char in value:
        result += BASE62.index(char) * pow(BASE62_LENGTH, base - 1)
        base -= 1

    return result


class Guid:
    """
    Guid is 16 characters long globally unique, sortable uri safe identifier.

    Sbt5LrD9iSAwb300
    |      |      |
    +- first 7 characters for millisecond timestamp
           |      |
           +- next 7 characters is randomly generated hash
                  |
                  + last two characters to ensure uniqueness of guid in a single millisecond

    In 1 ms with uniqueness of 2 there can be 62^2 unique generated ids on a single machine
    """

    _latest_timestamp: int = 0
    _latest_random_sequence: List[int] = [0 for i in range(0, HASH_LENGTH)]
    _inc_lock = threading.Lock()
    _id: str
    _ts: int
    __slots__ = ["_id", "_ts"]

    def __init__(self, value: str = None):

        if not value:
            with Guid._inc_lock:
                ts = _time_ms()
                ha = Guid._generate_hash(ts)

            self._ts = ts
            self._id = base62_encode(ts) + ha
        else:
            if not self.validate(value):
                raise ValueError(f"Passed value {value} is not valid guid.")
            self._id = value
            self._ts = 0

    @classmethod
    def _generate_hash(cls, ts: int) -> str:
        if cls._latest_timestamp == ts:
            for i in range(0, UNIQUENESS_LEVEL):
                i = HASH_LENGTH - i - 1
                cls._latest_random_sequence[i] += 1

                if cls._latest_random_sequence[i] >= BASE62_LENGTH:
                    cls._latest_random_sequence[i] = 0
                    continue

                break
        else:
            for i in range(0, HASH_LENGTH - UNIQUENESS_LEVEL):
                cls._latest_random_sequence[i] = random.randint(0, BASE62_LENGTH - 1)

            # gently randomise last characters of hash so ids look a bit better
            for i in range(0, UNIQUENESS_LEVEL):
                cls._latest_random_sequence[HASH_LENGTH - i - 1] = random.randint(0, 9)

        result: str = ""
        for i in cls._latest_random_sequence:
            result += BASE62[i]

        cls._latest_timestamp = ts

        return result

    def __str__(self) -> str:
        return self._id

    def __repr__(self) -> str:
        return self._id

    @property
    def timestamp(self) -> int:
        if self._ts:
            return self._ts

        # time is stored in the first 7 bytes
        time_fraction = self._id[0:TIME_BYTES]
        self._ts = base62_decode(time_fraction)

        return self._ts

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Guid):
            return NotImplemented
        return self._id > other._id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Guid):
            return NotImplemented
        return self._id < other._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Guid):
            return NotImplemented
        return self._id == other._id

    @classmethod
    def validate(cls, guid: str) -> bool:
        if len(guid) != HASH_LENGTH + TIME_BYTES:
            return False

        return True
