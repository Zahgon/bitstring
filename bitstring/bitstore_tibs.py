from __future__ import annotations

from tibs import Tibs, Mutibs

from bitstring.exceptions import CreationError
from typing import Union, Iterable, Optional, overload, Iterator, Any
from bitstring.helpers import offset_slice_indices_lsb0



class ConstBitStore:
    """A light wrapper around tibs.Tibs that does the LSB0 stuff"""

    __slots__ = ('_bits',)

    def __init__(self, initializer: Union[Tibs, None] = None) -> None:
        if initializer is not None:
            self._bits = initializer
        else:
            self._bits = Tibs()

    @classmethod
    def join(cls, bitstores: Iterable[ConstBitStore], /) -> ConstBitStore:
        pass

    @classmethod
    def from_zeros(cls, i: int):
        pass

    @classmethod
    def from_tibs(cls, tb: Tibs):
        pass

    @classmethod
    def from_bytes(cls, b: Union[bytes, bytearray, memoryview], /) -> ConstBitStore:
        pass

    @classmethod
    def frombuffer(cls, buffer, /, length: Optional[int] = None) -> ConstBitStore:
        pass

    @classmethod
    def from_bin(cls, s: str) -> ConstBitStore:
        pass

    def set(self, value, pos) -> None:
        pass

    @staticmethod
    def using_rust_core() -> bool:
        pass

    def tobitarray(self):
        raise TypeError("tobitarray() is not available when using the Rust core option.")

    def to_bytes(self, pad_at_end: bool = True) -> bytes:
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

    def __add__(self, other: ConstBitStore, /) -> ConstBitStore:
        newbits = self._bits + other._bits
        return ConstBitStore.from_tibs(newbits)

    def __eq__(self, other: Any, /) -> bool:
        return self._bits == other._bits

    def __and__(self, other: ConstBitStore, /) -> ConstBitStore:
        return ConstBitStore.from_tibs(self._bits & other._bits)

    def __or__(self, other: ConstBitStore, /) -> ConstBitStore:
        return ConstBitStore.from_tibs(self._bits | other._bits)

    def __xor__(self, other: ConstBitStore, /) -> ConstBitStore:
        return ConstBitStore.from_tibs(self._bits ^ other._bits)

    def __invert__(self) -> ConstBitStore:
        return ConstBitStore.from_tibs(~self._bits)

    def find(self, bs: ConstBitStore, start: int, end: int, bytealigned: bool = False) -> int | None:
        pass

    def rfind(self, bs: ConstBitStore, start: int, end: int, bytealigned: bool = False) -> int | None:
        pass

    def findall_msb0(self, bs: ConstBitStore, start: int, end: int, bytealigned: bool = False) -> Iterator[int]:
        pass

    def rfindall_msb0(self, bs: ConstBitStore, start: int, end: int, bytealigned: bool = False) -> Iterator[int]:
        pass

    def count(self, value, /) -> int:
        pass

    def __iter__(self) -> Iterable[bool]:
        length = len(self)
        for i in range(length):
            yield self.getindex(i)

    def _mutable_copy(self) -> MutableBitStore:
        """Always creates a copy, even if instance is immutable."""
        pass

    def copy(self) -> ConstBitStore:
        pass

    def __getitem__(self, item: Union[int, slice], /) -> Union[int, ConstBitStore]:
        # Use getindex or getslice instead
        raise NotImplementedError

    def getindex_msb0(self, index: int, /) -> bool:
        pass

    def getslice_withstep_msb0(self, key: slice, /) -> ConstBitStore:
        pass

    def getslice_withstep_lsb0(self, key: slice, /) -> ConstBitStore:
        pass

    def getslice_msb0(self, start: Optional[int], stop: Optional[int], /) -> ConstBitStore:
        pass

    def getslice_lsb0(self, start: Optional[int], stop: Optional[int], /) -> ConstBitStore:
        pass

    def getindex_lsb0(self, index: int, /) -> bool:
        pass

    def any(self) -> bool:
        pass

    def all(self) -> bool:
        pass

    def __len__(self) -> int:
        return len(self._bits)


class MutableBitStore:
    """A light wrapper around tibs.Mutibs that does the LSB0 stuff"""

    __slots__ = ('_bits',)

    def __init__(self, initializer: Union[Mutibs, Tibs, None] = None) -> None:
        if initializer is not None:
            self._bits = initializer
        else:
            self._bits = Mutibs()

    @classmethod
    def from_zeros(cls, i: int):
        pass

    @classmethod
    def from_mutibs(cls, mb: Mutibs):
        pass

    @classmethod
    def from_bytes(cls, b: Union[bytes, bytearray, memoryview], /) -> MutableBitStore:
        pass

    @classmethod
    def frombuffer(cls, buffer, /, length: Optional[int] = None) -> MutableBitStore:
        pass

    @classmethod
    def from_bin(cls, s: str) -> MutableBitStore:
        pass

    def set(self, value, pos) -> None:
        pass

    @staticmethod
    def using_rust_core() -> bool:
        pass

    def tobitarray(self):
        raise TypeError("tobitarray() is not available when using the Rust core option.")

    def to_bytes(self, pad_at_end: bool = True) -> bytes:
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

    def __imul__(self, n: int, /) -> None:
        self._bits *= n

    def __ilshift__(self, n: int, /) -> None:
        self._bits <<= n

    def __irshift__(self, n: int, /) -> None:
        self._bits >>= n

    def __iadd__(self, other: MutableBitStore, /) -> MutableBitStore:
        self._bits += other._bits
        return self

    def __add__(self, other: MutableBitStore, /) -> MutableBitStore:
        bs = self._mutable_copy()
        bs += other
        return bs

    def __eq__(self, other: Any, /) -> bool:
        return self._bits == other._bits

    def __and__(self, other: MutableBitStore, /) -> MutableBitStore:
        return MutableBitStore.from_mutibs(self._bits & other._bits)

    def __or__(self, other: MutableBitStore, /) -> MutableBitStore:
        return MutableBitStore.from_mutibs(self._bits | other._bits)

    def __xor__(self, other: MutableBitStore, /) -> MutableBitStore:
        return MutableBitStore.from_mutibs(self._bits ^ other._bits)

    def __iand__(self, other: MutableBitStore, /) -> MutableBitStore:
        self._bits &= other._bits
        return self

    def __ior__(self, other: MutableBitStore, /) -> MutableBitStore:
        self._bits |= other._bits
        return self

    def __ixor__(self, other: MutableBitStore, /) -> MutableBitStore:
        self._bits ^= other._bits
        return self

    def __invert__(self) -> MutableBitStore:
        return MutableBitStore.from_mutibs(~self._bits)

    def find(self, bs: MutableBitStore, start: int, end: int, bytealigned: bool = False) -> int:
        pass

    def rfind(self, bs: MutableBitStore, start: int, end: int, bytealigned: bool = False):
        pass

    def findall_msb0(self, bs: MutableBitStore, start: int, end: int, bytealigned: bool = False) -> Iterator[int]:
        pass

    def rfindall_msb0(self, bs: MutableBitStore, start: int, end: int, bytealigned: bool = False) -> Iterator[int]:
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

    def extend_left(self, other: MutableBitStore, /) -> None:
        pass

    def _mutable_copy(self) -> MutableBitStore:
        """Always creates a copy, even if instance is immutable."""
        pass

    def copy(self) -> MutableBitStore:
        pass

    def __getitem__(self, item: Union[int, slice], /) -> Union[int, MutableBitStore]:
        # Use getindex or getslice instead
        raise NotImplementedError

    def getindex_msb0(self, index: int, /) -> bool:
        pass

    def getslice_withstep_msb0(self, key: slice, /) -> MutableBitStore:
        pass

    def getslice_withstep_lsb0(self, key: slice, /) -> MutableBitStore:
        pass

    def getslice_msb0(self, start: Optional[int], stop: Optional[int], /) -> MutableBitStore:
        pass

    def getslice_lsb0(self, start: Optional[int], stop: Optional[int], /) -> MutableBitStore:
        pass

    def getindex_lsb0(self, index: int, /) -> bool:
        pass

    @overload
    def setitem_lsb0(self, key: int, value: int, /) -> None:
        ...

    @overload
    def setitem_lsb0(self, key: slice, value: MutableBitStore, /) -> None:
        ...

    def setitem_lsb0(self, key: Union[int, slice], value: Union[int, MutableBitStore], /) -> None:
        pass

    def delitem_lsb0(self, key: Union[int, slice], /) -> None:
        pass

    def invert_msb0(self, index: Optional[int] = None, /) -> None:
        pass

    def invert_lsb0(self, index: Optional[int] = None, /) -> None:
        pass

    def any(self) -> bool:
        pass

    def all(self) -> bool:
        pass

    def __len__(self) -> int:
        return len(self._bits)

    def setitem_msb0(self, key, value, /):
        pass

    def delitem_msb0(self, key, /):
        pass
