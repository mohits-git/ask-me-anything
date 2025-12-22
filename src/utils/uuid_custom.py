import os
import time
from uuid import UUID


_CLEARFLAG_MASK = ~((0xf000c << 60))
_VERSION_7_FLAGS = (0x70008 << 60)


def _uuid_get_counter_and_tail():
    rand = int.from_bytes(os.urandom(10))
    counter = (rand >> 32) & 0x1ff_ffff_ffff
    tail = rand & 0xffff_ffff
    return counter, tail


_last_timestamp_v7 = 0
_last_counter_v7 = 0


def _uuidv7():
    global _last_timestamp_v7
    global _last_counter_v7

    timestamp = time.time_ns() // 1000000

    # if last timestamp is set to past, reseed the counter
    if _last_timestamp_v7 is None or _last_counter_v7 is None or (
            timestamp > _last_timestamp_v7):
        counter, tail = _uuid_get_counter_and_tail()
    else:
        if timestamp < _last_timestamp_v7:
            timestamp = _last_timestamp_v7 + 1
        counter = _last_counter_v7 + 1
        if counter > 0x3ff_ffff_ffff:
            timestamp += 1
            counter, tail = _uuid_get_counter_and_tail()
        else:
            tail = int.from_bytes(os.urandom(4))

    unix_timestamp = timestamp & 0xffff_ffff_ffff
    counter_hi = (counter >> 30) & 0x0fff  # clear version bits
    counter_lo = counter & 0x3fff_ffff  # clear variant bits
    tail &= 0xffff_ffff

    uuid_int = unix_timestamp << 80
    uuid_int |= counter_hi << 64
    uuid_int |= counter_lo << 32
    uuid_int |= tail

    uuid_int &= _CLEARFLAG_MASK
    uuid_int |= _VERSION_7_FLAGS
    uuid = UUID(int=uuid_int)

    _last_timestamp_v7 = timestamp
    _last_counter_v7 = counter
    return uuid


def generate_uuid() -> str:
    uuid7 = _uuidv7()
    return str(uuid7)
