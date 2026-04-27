from __future__ import annotations

import bitarray
import bitarray.util
from bitstring.exceptions import CreationError
from typing import Union, Iterable, Optional, overload, Iterator, Any
from bitstring.helpers import offset_slice_indices_lsb0

if bitarray.__version__.startswith("2."):
    raise ImportError(f"bitstring version 4.3 requires bitarray version 3 or higher. Found version {bitarray.__version__}.")


class _BitStore:
    """A light wrapper around bitarray that does the LSB0 stuff"""

    __slots__ = ('_bitarray', 'modified_length', 'immutable')

    def __init__(self, initializer: Union[bitarray.bitarray, None] = None,
                 immutable: bool = False) -> None:
        if isinstance(initializer, str):
            assert False
        self._bitarray = bitarray.bitarray(initializer)
        self.immutable = immutable
        self.modified_length = None

    @classmethod
    def from_zeros(cls, i: int) -> _BitStore:
        pass


    @classmethod
    def from_bin(cls, s: str) -> _BitStore:
        pass

    @classmethod
    def from_bytes(cls, b: Union[bytes, bytearray, memoryview], /) -> _BitStore:
        pass

    @classmethod
    def frombuffer(cls, buffer, /, length: Optional[int] = None) -> _BitStore:
        pass

    @classmethod
    def join(cls, bitstores: Iterable[_BitStore], /) -> _BitStore:
        pass

    @staticmethod
    def using_rust_core() -> bool:
        pass

    def tobitarray(self) -> bitarray.bitarray:
        pass

    def to_bytes(self) -> bytes:
        pass

    def to_u(self) -> int:
        pass

    def to_i(self) -> int:
        pass

    def to_hex(self) -> str:
        pass

    def to_bin(self) -> str:
        pass

    def to_oct(self) -> str:
        pass

    def __imul__(self, n: int, /) -> _BitStore:
        self._bitarray *= n
        return self

    def __ilshift__(self, n: int, /) -> None:
        self._bitarray <<= n

    def __irshift__(self, n: int, /) -> None:
        self._bitarray >>= n

    def __iadd__(self, other: _BitStore, /) -> _BitStore:
        self._bitarray += other._bitarray
        return self

    def __add__(self, other: _BitStore, /) -> _BitStore:
        bs = self._mutable_copy()
        bs += other
        return bs

    def __eq__(self, other: Any, /) -> bool:
        return self._bitarray == other._bitarray

    def __and__(self, other: _BitStore, /) -> _BitStore:
        return _BitStore(self._bitarray & other._bitarray)

    def __or__(self, other: _BitStore, /) -> _BitStore:
        return _BitStore(self._bitarray | other._bitarray)

    def __xor__(self, other: _BitStore, /) -> _BitStore:
        return _BitStore(self._bitarray ^ other._bitarray)

    def __iand__(self, other: _BitStore, /) -> _BitStore:
        self._bitarray &= other._bitarray
        return self

    def __ior__(self, other: _BitStore, /) -> _BitStore:
        self._bitarray |= other._bitarray
        return self

    def __ixor__(self, other: _BitStore, /) -> _BitStore:
        self._bitarray ^= other._bitarray
        return self

    def __invert__(self) -> _BitStore:
        return _BitStore(~self._bitarray)

    def find(self, bs: _BitStore, start: int, end: int, bytealigned: bool = False) -> int | None:
        pass

    def rfind(self, bs: _BitStore, start: int, end: int, bytealigned: bool = False) -> int | None:
        pass

    def findall_msb0(self, bs: _BitStore, start: int, end: int, bytealigned: bool = False) -> Iterator[int]:
        pass

    def rfindall_msb0(self, bs: _BitStore, start: int, end: int, bytealigned: bool = False) -> Iterator[int]:
        pass

    def count(self, value, /) -> int:
        pass

    def clear(self) -> None:
        pass

    def reverse(self) -> None:
        pass

    def __iter__(self) -> Iterable[bool]:
        for i in range(len(self)):
            yield self.getindex(i)

    def _mutable_copy(self) -> _BitStore:
        """Always creates a copy, even if instance is immutable."""
        pass

    def as_immutable(self) -> _BitStore:
        pass

    def copy(self) -> _BitStore:
        pass

    def __getitem__(self, item: Union[int, slice], /) -> Union[int, _BitStore]:
        # Use getindex or getslice instead
        raise NotImplementedError

    def getindex_msb0(self, index: int, /) -> bool:
        pass

    def getslice_withstep_msb0(self, key: slice, /) -> _BitStore:
        pass

    def getslice_withstep_lsb0(self, key: slice, /) -> _BitStore:
        pass

    def getslice_msb0(self, start: Optional[int], stop: Optional[int], /) -> _BitStore:
        pass

    def getslice_lsb0(self, start: Optional[int], stop: Optional[int], /) -> _BitStore:
        pass

    def getindex_lsb0(self, index: int, /) -> bool:
        pass

    @overload
    def setitem_lsb0(self, key: int, value: int, /) -> None:
        ...

    @overload
    def setitem_lsb0(self, key: slice, value: _BitStore, /) -> None:
        ...

    def setitem_lsb0(self, key: Union[int, slice], value: Union[int, _BitStore], /) -> None:
        pass

    def delitem_lsb0(self, key: Union[int, slice], /) -> None:
        pass

    def invert_msb0(self, index: Optional[int] = None, /) -> None:
        pass

    def invert_lsb0(self, index: Optional[int] = None, /) -> None:
        pass

    def extend_left(self, other: _BitStore, /) -> None:
        pass

    def any(self) -> bool:
        pass

    def all(self) -> bool:
        pass

    def __len__(self) -> int:
        return self.modified_length if self.modified_length is not None else len(self._bitarray)

    def setitem_msb0(self, key, value, /):
        pass

    def delitem_msb0(self, key, /):
        pass


ConstBitStore = _BitStore
MutableBitStore = _BitStore