from __future__ import annotations

import numbers
import pathlib
import sys
import mmap
import struct
import array
import io
from collections import abc
import functools
from typing import Tuple, Union, List, Iterable, Any, Optional, BinaryIO, TextIO, overload, Iterator, Type, TypeVar
import bitarray
import bitstring
from bitstring import utils
from bitstring.dtypes import Dtype, dtype_register
from bitstring.fp8 import p4binary_fmt, p3binary_fmt
from bitstring.mxfp import e3m2mxfp_fmt, e2m3mxfp_fmt, e2m1mxfp_fmt, e4m3mxfp_saturate_fmt, e5m2mxfp_saturate_fmt
from bitstring.bitstring_options import Colour

ConstBitStore = bitstring.bitstore.ConstBitStore
MutableBitStore = bitstring.bitstore.MutableBitStore
helpers = bitstring.bitstore_helpers
common_helpers = bitstring.bitstore_common_helpers


# Things that can be converted to Bits when a Bits type is needed
BitsType = Union['Bits', str, Iterable[Any], bool, BinaryIO, bytearray, bytes, memoryview, bitarray.bitarray]

TBits = TypeVar("TBits", bound='Bits')

# Maximum number of digits to use in __str__ and __repr__.
MAX_CHARS: int = 250


class Bits:
    """A container holding an immutable sequence of bits.

    For a mutable container use the BitArray class instead.

    Methods:

    all() -- Check if all specified bits are set to 1 or 0.
    any() -- Check if any of specified bits are set to 1 or 0.
    copy() - Return a copy of the bitstring.
    count() -- Count the number of bits set to 1 or 0.
    cut() -- Create generator of constant sized chunks.
    endswith() -- Return whether the bitstring ends with a sub-string.
    find() -- Find a sub-bitstring in the current bitstring.
    findall() -- Find all occurrences of a sub-bitstring in the current bitstring.
    fromstring() -- Create a bitstring from a formatted string.
    join() -- Join bitstrings together using current bitstring.
    pp() -- Pretty print the bitstring.
    rfind() -- Seek backwards to find a sub-bitstring.
    split() -- Create generator of chunks split by a delimiter.
    startswith() -- Return whether the bitstring starts with a sub-bitstring.
    tobitarray() -- Return bitstring as a bitarray from the bitarray package.
    tobytes() -- Return bitstring as bytes, padding if needed.
    tofile() -- Write bitstring to file, padding if needed.
    unpack() -- Interpret bits using format string.

    Special methods:

    Also available are the operators [], ==, !=, +, *, ~, <<, >>, &, |, ^.

    Properties:

    [GENERATED_PROPERTY_DESCRIPTIONS]

    len -- Length of the bitstring in bits.

    """
    __slots__ = ('_bitstore', '_filename')

    def __init__(self, auto: Optional[Union[BitsType, int]] = None, /, length: Optional[int] = None,
                 offset: Optional[int] = None, **kwargs) -> None:
        """Either specify an 'auto' initialiser:
        A string of comma separated tokens, an integer, a file object,
        a bytearray, a boolean iterable, an array or another bitstring.

        Or initialise via **kwargs with one (and only one) of:
        bin -- binary string representation, e.g. '0b001010'.
        hex -- hexadecimal string representation, e.g. '0x2ef'
        oct -- octal string representation, e.g. '0o777'.
        bytes -- raw data as a bytes object, for example read from a binary file.
        int -- a signed integer.
        uint -- an unsigned integer.
        float / floatbe -- a big-endian floating point number.
        bool -- a boolean (True or False).
        se -- a signed exponential-Golomb code.
        ue -- an unsigned exponential-Golomb code.
        sie -- a signed interleaved exponential-Golomb code.
        uie -- an unsigned interleaved exponential-Golomb code.
        floatle -- a little-endian floating point number.
        floatne -- a native-endian floating point number.
        bfloat / bfloatbe - a big-endian bfloat format 16-bit floating point number.
        bfloatle -- a little-endian bfloat format 16-bit floating point number.
        bfloatne -- a native-endian bfloat format 16-bit floating point number.
        intbe -- a signed big-endian whole byte integer.
        intle -- a signed little-endian whole byte integer.
        intne -- a signed native-endian whole byte integer.
        uintbe -- an unsigned big-endian whole byte integer.
        uintle -- an unsigned little-endian whole byte integer.
        uintne -- an unsigned native-endian whole byte integer.
        filename -- the path of a file which will be opened in binary read-only mode.

        Other keyword arguments:
        length -- length of the bitstring in bits, if needed and appropriate.
                  It must be supplied for all integer and float initialisers.
        offset -- bit offset to the data. These offset bits are
                  ignored and this is mainly intended for use when
                  initialising using 'bytes' or 'filename'.

        """
        pass

    def __new__(cls: Type[TBits], auto: Optional[Union[BitsType, int]] = None, /, length: Optional[int] = None,
                offset: Optional[int] = None, pos: Optional[int] = None, **kwargs) -> TBits:
        x = super().__new__(cls)
        if auto is None and not kwargs:
            # No initialiser so fill with zero bits up to length
            if length is not None:
                x._bitstore = ConstBitStore.from_zeros(length)
            else:
                x._bitstore = ConstBitStore()
            return x
        x._initialise(auto, length, offset, immutable=True, **kwargs)
        return x

    @classmethod
    def _create_from_bitstype(cls: Type[TBits], auto: BitsType, /) -> TBits:
        pass

    def _initialise(self, auto: Any, /, length: Optional[int], offset: Optional[int], immutable: bool, **kwargs) -> None:
        pass

    def __getattr__(self, attribute: str) -> Any:
        # Support for arbitrary attributes like u16 or f64.
        try:
            d = Dtype(attribute)
        except ValueError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attribute}'.")
        if d.bitlength is not None and len(self) != d.bitlength:
            raise ValueError(f"bitstring length {len(self)} doesn't match length {d.bitlength} of property '{attribute}'.")
        return d.get_fn(self)

    def __iter__(self) -> Iterable[bool]:
        return iter(self._bitstore)

    def __copy__(self: TBits) -> TBits:
        """Return a new copy of the Bits for the copy module."""
        # Note that if you want a new copy (different ID), use _copy instead.
        # The copy can return self as it's immutable.
        return self

    def __lt__(self, other: Any) -> bool:
        # bitstrings can't really be ordered.
        return NotImplemented

    def __gt__(self, other: Any) -> bool:
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        return NotImplemented

    def __add__(self: TBits, bs: BitsType) -> TBits:
        """Concatenate bitstrings and return new bitstring.

        bs -- the bitstring to append.

        """
        bs = self.__class__._create_from_bitstype(bs)
        s = self._copy() if len(bs) <= len(self) else bs._copy()
        if len(bs) <= len(self):
            s._addright(bs)
        else:
            s._addleft(self)
        return s

    def __radd__(self: TBits, bs: BitsType) -> TBits:
        """Append current bitstring to bs and return new bitstring.

        bs -- An object that can be 'auto' initialised as a bitstring that will be appended to.

        """
        bs = self.__class__._create_from_bitstype(bs)
        return bs.__add__(self)

    @overload
    def __getitem__(self: TBits, key: slice, /) -> TBits:
        ...

    @overload
    def __getitem__(self, key: int, /) -> bool:
        ...

    def __getitem__(self: TBits, key: Union[slice, int], /) -> Union[TBits, bool]:
        """Return a new bitstring representing a slice of the current bitstring.

        >>> print(Bits('0b00110')[1:4])
        '0b011'

        """
        if isinstance(key, numbers.Integral):
            return bool(self._bitstore.getindex(key))
        bs = super().__new__(self.__class__)
        bs._bitstore = self._bitstore.getslice_withstep(key)
        return bs

    def __len__(self) -> int:
        """Return the length of the bitstring in bits."""
        return self._getlength()

    def __bytes__(self) -> bytes:
        return self.tobytes()

    def __str__(self) -> str:
        """Return approximate string representation of bitstring for printing.

        Short strings will be given wholly in hexadecimal or binary. Longer
        strings may be part hexadecimal and part binary. Very long strings will
        be truncated with '...'.

        """
        length = len(self)
        if not length:
            return ''
        if length > MAX_CHARS * 4:
            # Too long for hex. Truncate...
            return ''.join(('0x', self[0:MAX_CHARS*4]._gethex(), '...'))
        # If it's quite short and we can't do hex then use bin
        if length < 32 and length % 4 != 0:
            return '0b' + self.bin
        # If we can use hex then do so
        if not length % 4:
            return '0x' + self.hex
        # Otherwise first we do as much as we can in hex
        # then add on 1, 2 or 3 bits on at the end
        bits_at_end = length % 4
        return ''.join(('0x', self[0:length - bits_at_end]._gethex(),
                        ', ', '0b', self[length - bits_at_end:]._getbin()))

    def _repr(self, classname: str, length: int, pos: int):
        pass

    def __repr__(self) -> str:
        """Return representation that could be used to recreate the bitstring.

        If the returned string is too long it will be truncated. See __str__().

        """
        return self._repr(self.__class__.__name__, len(self), 0)

    def __eq__(self, bs: Any, /) -> bool:
        """Return True if two bitstrings have the same binary representation.

        >>> BitArray('0b1110') == '0xe'
        True

        """
        try:
            return self._bitstore == Bits._create_from_bitstype(bs)._bitstore
        except TypeError:
            return False

    def __ne__(self, bs: Any, /) -> bool:
        """Return False if two bitstrings have the same binary representation.

        >>> BitArray('0b111') == '0x7'
        False

        """
        return not self.__eq__(bs)

    def __invert__(self: TBits) -> TBits:
        """Return bitstring with every bit inverted.

        Raises Error if the bitstring is empty.

        """
        if len(self) == 0:
            raise bitstring.Error("Cannot invert empty bitstring.")
        s = self.__class__.__new__(self.__class__)
        s._bitstore = ~self._bitstore
        return s

    def __lshift__(self: TBits, n: int, /) -> TBits:
        """Return bitstring with bits shifted by n to the left.

        n -- the number of bits to shift. Must be >= 0.

        """
        if n < 0:
            raise ValueError("Cannot shift by a negative amount.")
        if len(self) == 0:
            raise ValueError("Cannot shift an empty bitstring.")
        n = min(n, len(self))
        s = self._absolute_slice(n, len(self))
        s._addright(Bits(n))
        return s

    def __rshift__(self: TBits, n: int, /) -> TBits:
        """Return bitstring with bits shifted by n to the right.

        n -- the number of bits to shift. Must be >= 0.

        """
        if n < 0:
            raise ValueError("Cannot shift by a negative amount.")
        if len(self) == 0:
            raise ValueError("Cannot shift an empty bitstring.")
        if not n:
            return self._copy()
        s = self.__class__(length=min(n, len(self)))
        n = min(n, len(self))
        s._addright(self._absolute_slice(0, len(self) - n))
        return s

    def __mul__(self: TBits, n: int, /) -> TBits:
        """Return bitstring consisting of n concatenations of self.

        Called for expression of the form 'a = b*3'.
        n -- The number of concatenations. Must be >= 0.

        """
        if n < 0:
            raise ValueError("Cannot multiply by a negative integer.")
        if n == 0:
            return self.__class__()
        s = self._copy()
        s._imul(n)
        return s

    def _imul(self: TBits, n: int, /) -> TBits:
        """Concatenate n copies of self in place. Return self."""
        pass

    def __rmul__(self: TBits, n: int, /) -> TBits:
        """Return bitstring consisting of n concatenations of self.

        Called for expressions of the form 'a = 3*b'.
        n -- The number of concatenations. Must be >= 0.

        """
        return self.__mul__(n)

    def __and__(self: TBits, bs: BitsType, /) -> TBits:
        """Bit-wise 'and' between two bitstrings. Returns new bitstring.

        bs -- The bitstring to '&' with.

        Raises ValueError if the two bitstrings have differing lengths.

        """
        if bs is self:
            return self.copy()
        bs = Bits._create_from_bitstype(bs)
        s = object.__new__(self.__class__)
        s._bitstore = self._bitstore & bs._bitstore
        return s

    def __rand__(self: TBits, bs: BitsType, /) -> TBits:
        """Bit-wise 'and' between two bitstrings. Returns new bitstring.

        bs -- the bitstring to '&' with.

        Raises ValueError if the two bitstrings have differing lengths.

        """
        return self.__and__(bs)

    def __or__(self: TBits, bs: BitsType, /) -> TBits:
        """Bit-wise 'or' between two bitstrings. Returns new bitstring.

        bs -- The bitstring to '|' with.

        Raises ValueError if the two bitstrings have differing lengths.

        """
        if bs is self:
            return self.copy()
        bs = Bits._create_from_bitstype(bs)
        s = object.__new__(self.__class__)
        s._bitstore = self._bitstore | bs._bitstore
        return s

    def __ror__(self: TBits, bs: BitsType, /) -> TBits:
        """Bit-wise 'or' between two bitstrings. Returns new bitstring.

        bs -- The bitstring to '|' with.

        Raises ValueError if the two bitstrings have differing lengths.

        """
        return self.__or__(bs)

    def __xor__(self: TBits, bs: BitsType, /) -> TBits:
        """Bit-wise 'xor' between two bitstrings. Returns new bitstring.

        bs -- The bitstring to '^' with.

        Raises ValueError if the two bitstrings have differing lengths.

        """
        bs = Bits._create_from_bitstype(bs)
        s = object.__new__(self.__class__)
        s._bitstore = self._bitstore ^ bs._bitstore
        return s

    def __rxor__(self: TBits, bs: BitsType, /) -> TBits:
        """Bit-wise 'xor' between two bitstrings. Returns new bitstring.

        bs -- The bitstring to '^' with.

        Raises ValueError if the two bitstrings have differing lengths.

        """
        return self.__xor__(bs)

    def __contains__(self, bs: BitsType, /) -> bool:
        """Return whether bs is contained in the current bitstring.

        bs -- The bitstring to search for.

        """
        found = Bits.find(self, bs, bytealigned=False)
        return bool(found)

    def __hash__(self) -> int:
        """Return an integer hash of the object."""
        # Only requirement is that equal bitstring should return the same hash.
        # For equal bitstrings the bytes at the start/end will be the same and they will have the same length
        # (need to check the length as there could be zero padding when getting the bytes). We do not check any
        # bit position inside the bitstring as that does not feature in the __eq__ operation.
        if len(self) <= 2000:
            # Use the whole bitstring.
            return hash((self.tobytes(), len(self)))
        else:
            # We can't in general hash the whole bitstring (it could take hours!)
            # So instead take some bits from the start and end.
            return hash(((self[:800] + self[-800:]).tobytes(), len(self)))

    def __bool__(self) -> bool:
        """Return False if bitstring is empty, otherwise return True."""
        return len(self) != 0

    def _clear(self) -> None:
        """Reset the bitstring to an empty state."""
        pass

    def _setauto_no_length_or_offset(self, s: BitsType, /) -> None:
        """Set bitstring from a bitstring, file, bool, array, iterable or string."""
        pass

    def _setauto(self, s: BitsType, length: Optional[int], offset: Optional[int], /) -> None:
        """Set bitstring from a bitstring, file, bool, array, iterable or string."""
        pass

    def _setfile(self, filename: str, length: Optional[int] = None, offset: Optional[int] = None) -> None:
        """Use file as source of bits."""
        pass

    def _setbitarray(self, ba: bitarray.bitarray, length: Optional[int], offset: Optional[int]) -> None:
        pass

    def _setbits(self, bs: BitsType, length: None = None) -> None:
        pass

    def _setp3binary(self, f: float) -> None:
        pass

    def _setp4binary(self, f: float) -> None:
        pass

    def _sete4m3mxfp(self, f: float) -> None:
        pass

    def _sete5m2mxfp(self, f: float) -> None:
        pass

    def _sete3m2mxfp(self, f: float) -> None:
        pass

    def _sete2m3mxfp(self, f: float) -> None:
        pass

    def _sete2m1mxfp(self, f: float) -> None:
        pass

    def _sete8m0mxfp(self, f: float) -> None:
        pass

    def _setmxint(self, f: float) -> None:
        pass

    def _setbytes(self, data: Union[bytearray, bytes, List], length:None = None) -> None:
        """Set the data from a bytes or bytearray object."""
        pass

    def _setbytes_with_truncation(self, data: Union[bytearray, bytes], length: Optional[int] = None, offset: Optional[int] = None) -> None:
        """Set the data from a bytes or bytearray object, with optional offset and length truncations."""
        pass

    def _getbytes(self) -> bytes:
        """Return the data as an ordinary bytes object."""
        pass

    _unprintable = list(range(0x00, 0x20))  # ASCII control characters
    _unprintable.extend(range(0x7f, 0xff))  # DEL char + non-ASCII

    def _getbytes_printable(self) -> str:
        """Return an approximation of the data as a string of printable characters."""
        pass

    def _setuint(self, uint: int, length: Optional[int] = None) -> None:
        """Reset the bitstring to have given unsigned int interpretation."""
        pass

    def _getuint(self) -> int:
        """Return data as an unsigned int."""
        pass

    def _setint(self, int_: int, length: Optional[int] = None) -> None:
        """Reset the bitstring to have given signed int interpretation."""
        pass

    def _getint(self) -> int:
        """Return data as a two's complement signed int."""
        pass

    def _setuintbe(self, uintbe: int, length: Optional[int] = None) -> None:
        """Set the bitstring to a big-endian unsigned int interpretation."""
        pass

    def _getuintbe(self) -> int:
        """Return data as a big-endian two's complement unsigned int."""
        pass

    def _setintbe(self, intbe: int, length: Optional[int] = None) -> None:
        """Set bitstring to a big-endian signed int interpretation."""
        pass

    def _getintbe(self) -> int:
        """Return data as a big-endian two's complement signed int."""
        pass

    def _setuintle(self, uintle: int, length: Optional[int] = None) -> None:
        pass

    def _getuintle(self) -> int:
        """Interpret as a little-endian unsigned int."""
        pass

    def _setintle(self, intle: int, length: Optional[int] = None) -> None:
        pass

    def _getintle(self) -> int:
        """Interpret as a little-endian signed int."""
        pass

    def _getp4binary(self) -> float:
        pass

    def _getp3binary(self) -> float:
        pass

    def _gete4m3mxfp(self) -> float:
        pass

    def _gete5m2mxfp(self) -> float:
        pass

    def _gete3m2mxfp(self) -> float:
        pass

    def _gete2m3mxfp(self) -> float:
        pass

    def _gete2m1mxfp(self) -> float:
        pass

    def _gete8m0mxfp(self) -> float:
        pass

    def _getmxint(self) -> float:
        pass

    def _setfloat(self, f: float, length: Optional[int], big_endian: bool) -> None:
        pass

    def _setfloatbe(self, f: float, length: Optional[int] = None) -> None:
        pass

    def _getfloatbe(self) -> float:
        """Interpret the whole bitstring as a big-endian float."""
        pass

    def _setfloatle(self, f: float, length: Optional[int] = None) -> None:
        pass

    def _getfloatle(self) -> float:
        """Interpret the whole bitstring as a little-endian float."""
        pass

    def _getbfloatbe(self) -> float:
        pass

    def _setbfloatbe(self, f: Union[float, str], length: Optional[int] = None) -> None:
        pass

    def _getbfloatle(self) -> float:
        pass

    def _setbfloatle(self, f: Union[float, str], length: Optional[int] = None) -> None:
        pass

    def _setue(self, i: int) -> None:
        """Initialise bitstring with unsigned exponential-Golomb code for integer i.

        Raises CreationError if i < 0.

        """
        pass

    def _readue(self, pos: int) -> Tuple[int, int]:
        """Return interpretation of next bits as unsigned exponential-Golomb code.

        Raises ReadError if the end of the bitstring is encountered while
        reading the code.

        """
        pass

    def _getue(self) -> Tuple[int, int]:
        pass

    def _getse(self) -> Tuple[int, int]:
        pass

    def _getuie(self) -> Tuple[int, int]:
        pass

    def _getsie(self) -> Tuple[int, int]:
        pass

    def _setse(self, i: int) -> None:
        """Initialise bitstring with signed exponential-Golomb code for integer i."""
        pass

    def _readse(self, pos: int) -> Tuple[int, int]:
        """Return interpretation of next bits as a signed exponential-Golomb code.

        Advances position to after the read code.

        Raises ReadError if the end of the bitstring is encountered while
        reading the code.

        """
        pass

    def _setuie(self, i: int) -> None:
        """Initialise bitstring with unsigned interleaved exponential-Golomb code for integer i.

        Raises CreationError if i < 0.

        """
        pass

    def _readuie(self, pos: int) -> Tuple[int, int]:
        """Return interpretation of next bits as unsigned interleaved exponential-Golomb code.

        Raises ReadError if the end of the bitstring is encountered while
        reading the code.

        """
        pass

    def _setsie(self, i: int, ) -> None:
        """Initialise bitstring with signed interleaved exponential-Golomb code for integer i."""
        pass

    def _readsie(self, pos: int) -> Tuple[int, int]:
        """Return interpretation of next bits as a signed interleaved exponential-Golomb code.

        Advances position to after the read code.

        Raises ReadError if the end of the bitstring is encountered while
        reading the code.

        """
        pass

    def _setbool(self, value: Union[bool, str]) -> None:
        # We deliberately don't want to have implicit conversions to bool here.
        # If we did then it would be difficult to deal with the 'False' string.
        pass

    def _getbool(self) -> bool:
        pass

    def _getpad(self) -> None:
        pass

    def _setpad(self, value: None, length: int) -> None:
        pass

    def _setbin(self, binstring: str, length: None = None) -> None:
        """Reset the bitstring to the value given in binstring."""
        pass

    def _getbin(self) -> str:
        """Return interpretation as a binary string."""
        pass

    def _setoct(self, octstring: str, length: None = None) -> None:
        """Reset the bitstring to have the value given in octstring."""
        pass

    def _getoct(self) -> str:
        """Return interpretation as an octal string."""
        pass

    def _sethex(self, hexstring: str, length: None = None) -> None:
        """Reset the bitstring to have the value given in hexstring."""
        pass

    def _gethex(self) -> str:
        """Return the hexadecimal representation as a string.

        Raises an InterpretError if the bitstring's length is not a multiple of 4.

        """
        pass

    def _getlength(self) -> int:
        """Return the length of the bitstring in bits."""
        pass

    def _copy(self: TBits) -> TBits:
        """Create and return a new copy of the Bits (always in memory)."""
        pass

    def _slice(self: TBits, start: int, end: int) -> TBits:
        """Used internally to get a slice, without error checking."""
        pass

    def _absolute_slice(self: TBits, start: int, end: int) -> TBits:
        """Used internally to get a slice, without error checking.
        Uses MSB0 bit numbering even if LSB0 is set."""
        pass

    def _readtoken(self, name: str, pos: int, length: Optional[int]) -> Tuple[Union[float, int, str, None, Bits], int]:
        """Reads a token from the bitstring and returns the result."""
        pass

    def _addright(self, bs: Bits, /) -> None:
        """Add a bitstring to the RHS of the current bitstring."""
        pass

    def _addleft(self, bs: Bits, /) -> None:
        """Prepend a bitstring to the current bitstring."""
        pass

    def _insert(self, bs: Bits, pos: int, /) -> None:
        """Insert bs at pos."""
        pass

    def _overwrite(self, bs: Bits, pos: int, /) -> None:
        """Overwrite with bs at pos."""
        pass

    def _delete(self, bits: int, pos: int, /) -> None:
        """Delete bits at pos."""
        pass

    def _reversebytes(self, start: int, end: int) -> None:
        """Reverse bytes in-place."""
        pass

    def _invert(self, pos: int, /) -> None:
        """Flip bit at pos 1<->0."""
        pass

    def _ilshift(self: TBits, n: int, /) -> TBits:
        """Shift bits by n to the left in place. Return self."""
        pass

    def _irshift(self: TBits, n: int, /) -> TBits:
        """Shift bits by n to the right in place. Return self."""
        pass

    def _getbits(self: TBits):
        pass

    def _validate_slice(self, start: Optional[int], end: Optional[int]) -> Tuple[int, int]:
        """Validate start and end and return them as positive bit positions."""
        pass

    def unpack(self, fmt: Union[str, List[Union[str, int]]], **kwargs) -> List[Union[int, float, str, Bits, bool, bytes, None]]:
        """Interpret the whole bitstring using fmt and return list.

        fmt -- A single string or a list of strings with comma separated tokens
               describing how to interpret the bits in the bitstring. Items
               can also be integers, for reading new bitstring of the given length.
        kwargs -- A dictionary or keyword-value pairs - the keywords used in the
                  format string will be replaced with their given value.

        Raises ValueError if the format is not understood. If not enough bits
        are available then all bits to the end of the bitstring will be used.

        See the docstring for 'read' for token examples.

        """
        pass

    def _readlist(self, fmt: Union[str, List[Union[str, int, Dtype]]], pos: int, **kwargs) \
            -> Tuple[List[Union[int, float, str, Bits, bool, bytes, None]], int]:
        pass

    def _read_dtype_list(self, dtypes: List[Dtype], pos: int) -> Tuple[List[Union[int, float, str, Bits, bool, bytes, None]], int]:
        pass

    def find(self, bs: BitsType, /, start: Optional[int] = None, end: Optional[int] = None,
             bytealigned: Optional[bool] = None) -> Union[Tuple[int], Tuple[()]]:
        """Find first occurrence of substring bs.

        Returns a single item tuple with the bit position if found, or an
        empty tuple if not found. The bit position (pos property) will
        also be set to the start of the substring if it is found.

        bs -- The bitstring to find.
        start -- The bit position to start the search. Defaults to 0.
        end -- The bit position one past the last bit to search.
               Defaults to len(self).
        bytealigned -- If True the bitstring will only be
                       found on byte boundaries.

        Raises ValueError if bs is empty, if start < 0, if end > len(self) or
        if end < start.

        >>> BitArray('0xc3e').find('0b1111')
        (6,)

        """
        pass

    def _find_lsb0(self, bs: Bits, start: int, end: int, bytealigned: bool) -> Union[Tuple[int], Tuple[()]]:
        # A forward find in lsb0 is very like a reverse find in msb0.
        pass

    def _find_msb0(self, bs: Bits, start: int, end: int, bytealigned: bool) -> Union[Tuple[int], Tuple[()]]:
        """Find first occurrence of a binary string."""
        pass

    def findall(self, bs: BitsType, start: Optional[int] = None, end: Optional[int] = None, count: Optional[int] = None,
                bytealigned: Optional[bool] = None) -> Iterable[int]:
        """Find all occurrences of bs. Return generator of bit positions.

        bs -- The bitstring to find.
        start -- The bit position to start the search. Defaults to 0.
        end -- The bit position one past the last bit to search.
               Defaults to len(self).
        count -- The maximum number of occurrences to find.
        bytealigned -- If True the bitstring will only be found on
                       byte boundaries.

        Raises ValueError if bs is empty, if start < 0, if end > len(self) or
        if end < start.

        Note that all occurrences of bs are found, even if they overlap.

        """
        pass

    def _findall_msb0(self, bs: Bits, start: int, end: int, count: Optional[int],
                      bytealigned: bool) -> Iterable[int]:
        pass

    def _findall_lsb0(self, bs: Bits, start: int, end: int, count: Optional[int],
                      bytealigned: bool) -> Iterable[int]:
        pass

    def rfind(self, bs: BitsType, /, start: Optional[int] = None, end: Optional[int] = None,
              bytealigned: Optional[bool] = None) -> Union[Tuple[int], Tuple[()]]:
        """Find final occurrence of substring bs.

        Returns a single item tuple with the bit position if found, or an
        empty tuple if not found. The bit position (pos property) will
        also be set to the start of the substring if it is found.

        bs -- The bitstring to find.
        start -- The bit position to end the reverse search. Defaults to 0.
        end -- The bit position one past the first bit to reverse search.
               Defaults to len(self).
        bytealigned -- If True the bitstring will only be found on byte
                       boundaries.

        Raises ValueError if bs is empty, if start < 0, if end > len(self) or
        if end < start.

        """
        pass

    def _rfind_msb0(self, bs: Bits, start: int, end: int, bytealigned: bool) -> Union[Tuple[int], Tuple[()]]:
        """Find final occurrence of a binary string."""
        pass

    def _rfind_lsb0(self, bs: Bits, start: int, end: int, bytealigned: bool) -> Union[Tuple[int], Tuple[()]]:
        # A reverse find in lsb0 is very like a forward find in msb0.
        pass

    def cut(self, bits: int, start: Optional[int] = None, end: Optional[int] = None,
            count: Optional[int] = None) -> Iterator[Bits]:
        """Return bitstring generator by cutting into bits sized chunks.

        bits -- The size in bits of the bitstring chunks to generate.
        start -- The bit position to start the first cut. Defaults to 0.
        end -- The bit position one past the last bit to use in the cut.
               Defaults to len(self).
        count -- If specified then at most count items are generated.
                 Default is to cut as many times as possible.

        """
        pass

    def split(self, delimiter: BitsType, start: Optional[int] = None, end: Optional[int] = None,
              count: Optional[int] = None, bytealigned: Optional[bool] = None) -> Iterable[Bits]:
        """Return bitstring generator by splitting using a delimiter.

        The first item returned is the initial bitstring before the delimiter,
        which may be an empty bitstring.

        delimiter -- The bitstring used as the divider.
        start -- The bit position to start the split. Defaults to 0.
        end -- The bit position one past the last bit to use in the split.
               Defaults to len(self).
        count -- If specified then at most count items are generated.
                 Default is to split as many times as possible.
        bytealigned -- If True splits will only occur on byte boundaries.

        Raises ValueError if the delimiter is empty.

        """
        pass

    def join(self: TBits, sequence: Iterable[Any]) -> TBits:
        """Return concatenation of bitstrings joined by self.

        sequence -- A sequence of bitstrings.

        """
        pass

    def tobytes(self) -> bytes:
        """Return the bitstring as bytes, padding with zero bits if needed.

        Up to seven zero bits will be added at the end to byte align.

        """
        pass

    def tobitarray(self) -> bitarray.bitarray:
        """Convert the bitstring to a bitarray object."""
        pass

    def tofile(self, f: BinaryIO) -> None:
        """Write the bitstring to a file object, padding with zero bits if needed.

        Up to seven zero bits will be added at the end to byte align.

        """
        pass

    def startswith(self, prefix: BitsType, start: Optional[int] = None, end: Optional[int] = None) -> bool:
        """Return whether the current bitstring starts with prefix.

        prefix -- The bitstring to search for.
        start -- The bit position to start from. Defaults to 0.
        end -- The bit position to end at. Defaults to len(self).

        """
        pass

    def endswith(self, suffix: BitsType, start: Optional[int] = None, end: Optional[int] = None) -> bool:
        """Return whether the current bitstring ends with suffix.

        suffix -- The bitstring to search for.
        start -- The bit position to start from. Defaults to 0.
        end -- The bit position to end at. Defaults to len(self).

        """
        pass

    def all(self, value: Any, pos: Optional[Iterable[int]] = None) -> bool:
        """Return True if one or many bits are all set to bool(value).

        value -- If value is True then checks for bits set to 1, otherwise
                 checks for bits set to 0.
        pos -- An iterable of bit positions. Negative numbers are treated in
               the same way as slice indices. Defaults to the whole bitstring.

        """
        pass

    def any(self, value: Any, pos: Optional[Iterable[int]] = None) -> bool:
        """Return True if any of one or many bits are set to bool(value).

        value -- If value is True then checks for bits set to 1, otherwise
                 checks for bits set to 0.
        pos -- An iterable of bit positions. Negative numbers are treated in
               the same way as slice indices. Defaults to the whole bitstring.

        """
        pass

    def count(self, value: Any) -> int:
        """Return count of total number of either zero or one bits.

        value -- If bool(value) is True then bits set to 1 are counted, otherwise bits set
                 to 0 are counted.

        >>> Bits('0xef').count(1)
        7

        """
        pass

    @staticmethod
    def _format_bits(bits: Bits, bits_per_group: int, sep: str, dtype: Dtype,
                     colour_start: str, colour_end: str, width: Optional[int]=None) -> Tuple[str, int]:
        pass

    @staticmethod
    def _chars_per_group(bits_per_group: int, fmt: Optional[str]):
        """How many characters are needed to represent a number of bits with a given format."""
        pass

    @staticmethod
    def _bits_per_char(fmt: str):
        """How many bits are represented by each character of a given format."""
        pass

    def _pp(self, dtype1: Dtype, dtype2: Optional[Dtype], bits_per_group: int, width: int, sep: str, format_sep: str,
            show_offset: bool, stream: TextIO, lsb0: bool, offset_factor: int) -> None:
        """Internal pretty print method."""
        pass

    @staticmethod
    def _process_pp_tokens(token_list, fmt):
        pass

    def pp(self, fmt: Optional[str] = None, width: int = 120, sep: str = ' ',
           show_offset: bool = True, stream: TextIO = sys.stdout) -> None:
        """Pretty print the bitstring's value.

        fmt -- Printed data format. One or two of 'bin', 'oct', 'hex' or 'bytes'.
              The number of bits represented in each printed group defaults to 8 for hex and bin,
              12 for oct and 32 for bytes. This can be overridden with an explicit length, e.g. 'hex:64'.
              Use a length of 0 to not split into groups, e.g. `bin:0`.
        width -- Max width of printed lines. Defaults to 120. A single group will always be printed
                 per line even if it exceeds the max width.
        sep -- A separator string to insert between groups. Defaults to a single space.
        show_offset -- If True (the default) shows the bit offset in the first column of each line.
        stream -- A TextIO object with a write() method. Defaults to sys.stdout.

        >>> s.pp('hex16')
        >>> s.pp('b, h', sep='_', show_offset=False)

        """
        pass

    def copy(self: TBits) -> TBits:
        """Return a copy of the bitstring."""
        pass

    @classmethod
    def fromstring(cls: TBits, s: str, /) -> TBits:
        """Create a new bitstring from a formatted string."""
        pass

    len = length = property(_getlength, doc="The length of the bitstring in bits. Read only.")


