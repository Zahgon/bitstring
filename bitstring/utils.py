from __future__ import annotations

import functools
import re
from typing import Tuple, List, Optional, Pattern, Dict, Union, Match


# A token name followed by optional : then an integer number
NAME_INT_RE: Pattern[str] = re.compile(r'^([a-zA-Z][a-zA-Z0-9_]*?):?(\d*)$')

# A token name followed by optional : then an arbitrary keyword
NAME_KWARG_RE: Pattern[str] = re.compile(r'^([a-zA-Z][a-zA-Z0-9_]*?):?([a-zA-Z0-9_]+)$')

CACHE_SIZE = 256

DEFAULT_BITS: Pattern[str] = re.compile(r'^(?P<len>[^=]+)?(=(?P<value>.*))?$', re.IGNORECASE)

MULTIPLICATIVE_RE: Pattern[str] = re.compile(r'^(?P<factor>.*)\*(?P<token>.+)')

# Hex, oct or binary literals
LITERAL_RE: Pattern[str] = re.compile(r'^(?P<name>0([xob]))(?P<value>.+)', re.IGNORECASE)

# An endianness indicator followed by one or more struct.pack codes
STRUCT_PACK_RE: Pattern[str] = re.compile(r'^(?P<endian>[<>@=])(?P<fmt>(?:\d*[bBhHlLiIqQefd])+)$')
# The same as above, but it doesn't insist on an endianness as it's byteswapping anyway.
BYTESWAP_STRUCT_PACK_RE: Pattern[str] = re.compile(r'^(?P<endian>[<>@=])?(?P<fmt>(?:\d*[bBhHlLiIqQefd])+)$')
# An endianness indicator followed by exactly one struct.pack codes
SINGLE_STRUCT_PACK_RE: Pattern[str] = re.compile(r'^(?P<endian>[<>@=])(?P<fmt>[bBhHlLiIqQefd])$')

# A number followed by a single character struct.pack code
STRUCT_SPLIT_RE: Pattern[str] = re.compile(r'\d*[bBhHlLiIqQefd]')

# These replicate the struct.pack codes
# Big-endian
REPLACEMENTS_BE: Dict[str, str] = {'b': 'int8', 'B': 'uint8',
                                   'h': 'intbe16', 'H': 'uintbe16',
                                   'l': 'intbe32', 'L': 'uintbe32',
                                   'i': 'intbe32', 'I': 'uintbe32',
                                   'q': 'intbe64', 'Q': 'uintbe64',
                                   'e': 'floatbe16', 'f': 'floatbe32', 'd': 'floatbe64'}
# Little-endian
REPLACEMENTS_LE: Dict[str, str] = {'b': 'int8', 'B': 'uint8',
                                   'h': 'intle16', 'H': 'uintle16',
                                   'l': 'intle32', 'L': 'uintle32',
                                   'i': 'intle32', 'I': 'uintle32',
                                   'q': 'intle64', 'Q': 'uintle64',
                                   'e': 'floatle16', 'f': 'floatle32', 'd': 'floatle64'}

# Native-endian
REPLACEMENTS_NE: Dict[str, str] = {'b': 'int8', 'B': 'uint8',
                                   'h': 'intne16', 'H': 'uintne16',
                                   'l': 'intne32', 'L': 'uintne32',
                                   'i': 'intne32', 'I': 'uintne32',
                                   'q': 'intne64', 'Q': 'uintne64',
                                   'e': 'floatne16', 'f': 'floatne32', 'd': 'floatne64'}

# Size in bytes of all the pack codes.
PACK_CODE_SIZE: Dict[str, int] = {'b': 1, 'B': 1, 'h': 2, 'H': 2, 'l': 4, 'L': 4, 'i': 4, 'I': 4,
                                  'q': 8, 'Q': 8, 'e': 2, 'f': 4, 'd': 8}


def structparser(m: Match[str]) -> List[str]:
    """Parse struct-like format string token into sub-token list."""
    pass


@functools.lru_cache(CACHE_SIZE)
def parse_name_length_token(fmt: str, **kwargs) -> Tuple[str, Optional[int]]:
    # Any single token with just a name and length
    pass


@functools.lru_cache(CACHE_SIZE)
def parse_single_struct_token(fmt: str) -> Optional[Tuple[str, Optional[int]]]:
    pass


@functools.lru_cache(CACHE_SIZE)
def parse_single_token(token: str) -> Tuple[str, str, Optional[str]]:
    pass


@functools.lru_cache(CACHE_SIZE)
def preprocess_tokens(fmt: str) -> List[str]:
    # Remove whitespace and expand brackets
    pass


@functools.lru_cache(CACHE_SIZE)
def tokenparser(fmt: str, keys: Tuple[str, ...] = ()) -> \
        Tuple[bool, List[Tuple[str, Union[int, str, None], Optional[str]]]]:
    """Divide the format string into tokens and parse them.

    Return stretchy token and list of [initialiser, length, value]
    initialiser is one of: hex, oct, bin, uint, int, se, ue, 0x, 0o, 0b etc.
    length is None if not known, as is value.

    If the token is in the keyword dictionary (keys) then it counts as a
    special case and isn't messed with.

    tokens must be of the form: [factor*][initialiser][:][length][=value]

    """
    pass


BRACKET_RE = re.compile(r'(?P<factor>\d+)\*\(')


def expand_brackets(s: str) -> str:
    """Expand all brackets."""
    pass
