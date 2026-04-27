from __future__ import annotations

from typing import Union
from tibs import Tibs, Mutibs
import bitstring

MutableBitStore = bitstring.bitstore.MutableBitStore
ConstBitStore = bitstring.bitstore.ConstBitStore

from bitstring.helpers import tidy_input_string


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
