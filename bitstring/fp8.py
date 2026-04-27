"""
The 8-bit float formats used here are from a proposal supported by Graphcore, AMD and Qualcomm.
See https://arxiv.org/abs/2206.02915

"""

import struct
import zlib
import array
import bitarray
from bitstring.luts import binary8_luts_compressed
import math


class Binary8Format:
    """8-bit floating point formats based on draft IEEE binary8"""

    def __init__(self, exp_bits: int, bias: int):
        self.exp_bits = exp_bits
        self.bias = bias
        self.pos_clamp_value = 0b01111111
        self.neg_clamp_value = 0b11111111

    def __str__(self):
        return f"Binary8Format(exp_bits={self.exp_bits}, bias={self.bias})"

    def decompress_luts(self):
        pass

    def create_luts(self):
        pass

    def float_to_int8(self, f: float) -> int:
        """Given a Python float convert to the best float8 (expressed as an integer in 0-255 range)."""
        pass

    def createLUT_for_float16_to_binary8(self) -> bytes:
        # Used to create the LUT that was compressed and stored for the fp8 code
        pass

    def createLUT_for_binary8_to_float(self):
        """Create a LUT to convert an int in range 0-255 representing a float8 into a Python float"""
        pass


# We create the 1.5.2 and 1.4.3 formats.
p4binary_fmt = Binary8Format(exp_bits=4, bias=8)
p3binary_fmt = Binary8Format(exp_bits=5, bias=16)


def decompress_luts():
    pass
