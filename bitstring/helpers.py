from typing import Union, Tuple


def _indices(s: slice, length: int) -> Tuple[int, Union[int, None], int]:
    """A better implementation of slice.indices such that a
    slice made from [start:stop:step] will actually equal the original slice."""
    pass

def offset_slice_indices_lsb0(key: slice, length: int) -> slice:
    pass

def tidy_input_string(s: str) -> str:
    """Return string made lowercase and with all whitespace and underscores removed."""
    pass
