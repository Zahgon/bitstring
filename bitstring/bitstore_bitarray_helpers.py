from __future__ import annotations

import struct
import math
import functools
from typing import Union, Optional, Dict, Callable
import bitarray
import bitstring
from bitstring.fp8 import p4binary_fmt, p3binary_fmt
from bitstring.mxfp import (e3m2mxfp_fmt, e2m3mxfp_fmt, e2m1mxfp_fmt, e4m3mxfp_saturate_fmt,
                            e5m2mxfp_saturate_fmt, e4m3mxfp_overflow_fmt, e5m2mxfp_overflow_fmt)
from bitstring.helpers import tidy_input_string

ConstBitStore = bitstring.bitstore.ConstBitStore
MutableBitStore = bitstring.bitstore.MutableBitStore


def bin2bitstore(binstring: str) -> ConstBitStore:
    pass


def hex2bitstore(hexstring: str) -> ConstBitStore:
    pass


def oct2bitstore(octstring: str) -> ConstBitStore:
    pass


def int2bitstore(i: int, length: int, signed: bool) -> ConstBitStore:
    pass


def intle2bitstore(i: int, length: int, signed: bool) -> ConstBitStore:
    pass


def float2bitstore(f: Union[str, float], length: int, big_endian: bool) -> ConstBitStore:
    pass

