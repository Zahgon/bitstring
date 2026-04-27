from __future__ import annotations

import struct
import math
from typing import Union, Dict, Callable, Optional
import functools
import bitstring
from bitstring.fp8 import p4binary_fmt, p3binary_fmt
from bitstring.mxfp import (e3m2mxfp_fmt, e2m3mxfp_fmt, e2m1mxfp_fmt, e4m3mxfp_saturate_fmt,
                            e5m2mxfp_saturate_fmt, e4m3mxfp_overflow_fmt, e5m2mxfp_overflow_fmt)

helpers = bitstring.bitstore_helpers
ConstBitStore = bitstring.bitstore.ConstBitStore
MutableBitStore = bitstring.bitstore.MutableBitStore


CACHE_SIZE = 256

@functools.lru_cache(CACHE_SIZE)
def str_to_bitstore(s: str) -> ConstBitStore:
    pass


literal_bit_funcs: Dict[str, Callable[..., ConstBitStore]] = {
    '0x': helpers.hex2bitstore,
    '0X': helpers.hex2bitstore,
    '0b': helpers.bin2bitstore,
    '0B': helpers.bin2bitstore,
    '0o': helpers.oct2bitstore,
    '0O': helpers.oct2bitstore,
}


def bitstore_from_token(name: str, token_length: Optional[int], value: Optional[str]) -> ConstBitStore:
    pass



def ue2bitstore(i: Union[str, int]) -> ConstBitStore:
    pass


def se2bitstore(i: Union[str, int]) -> ConstBitStore:
    pass


def uie2bitstore(i: Union[str, int]) -> ConstBitStore:
    pass


def sie2bitstore(i: Union[str, int]) -> ConstBitStore:
    pass


def bfloat2bitstore(f: Union[str, float], big_endian: bool) -> ConstBitStore:
    pass


def p4binary2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def p3binary2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def e4m3mxfp2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def e5m2mxfp2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def e3m2mxfp2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def e2m3mxfp2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def e2m1mxfp2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


e8m0mxfp_allowed_values = [float(2 ** x) for x in range(-127, 128)]


def e8m0mxfp2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass


def mxint2bitstore(f: Union[str, float]) -> ConstBitStore:
    pass
