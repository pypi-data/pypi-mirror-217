#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Human Friendly Numbers.

Numbers created by :any:`bin_`, :any:`hex` and :any:`bytes_`
simply stay in their representation even through calculations if they are the left operand.
Any string conversion results in a pretty formatted number.

Binary:

>>> bin_(42)
Bin('0b101010')
>>> str(bin_(42))
'0b101010'
>>> str(bin_(42) + 24)
'0b1000010'
>>> str(bin_(42, width=16))
'0b0000000000101010'

Hexadecimal

>>> hex_(42)
Hex('0x2A')
>>> str(hex_(42))
'0x2A'
>>> str(hex_(42) + 24)
'0x42'
>>> str(hex_(42, width=16))
'0x002A'

Bytes:

>>> bytes_(42)
Bytes('42 bytes')
>>> str(bytes_(42))
'42 bytes'
>>> str(bytes_(42) + 24)
'66 bytes'
>>> str(bytes_(42*1000))
'41.02 KB'
>>> str(bytes_(42*1024))
'42 KB'
"""

from typing import Any, Optional

from . import baseint, converter
from .binary import Bin
from .bytes import Bytes
from .hex import Hex


def bin_(value: Any, width: Optional[int] = None) -> Bin:
    """
    Integer with binary representation.

    The binary format is kept through calculations!!!

    Keyword Args:
        width (int): Width in bits.

    >>> bin_(32)
    Bin('0b100000')
    >>> str(bin_(32) + 3)
    '0b100011'
    >>> str(bin_(-32))
    '-0b100000'
    >>> str(bin_("0x50"))
    '0b01010000'
    >>> str(bin_("-0b1010000"))
    '-0b1010000'
    >>> str(bin_("0o50"))
    '0b101000'
    >>> bin_("5Z")
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: '5Z'

    A width in bits is optional:

    >>> bin_(32, width=16)
    Bin('0b0000000000100000')

    If given, the default width is taken from the value:

    >>> bin_("16'd50")
    Bin('0b0000000000110010')

    Smaller widths are not truncated:

    >>> bin_("16'd50", width=4)
    Bin('0b110010')
    """
    return Bin(value, width=width)


def hex_(value: Any, width: Optional[int] = None) -> Hex:
    """
    Integer with hexadecial representation.

    The hexadecial format is kept through calculations!!!

    Keyword Args:
        width (int): Width in bits.

    >>> hex_(32)
    Hex('0x20')
    >>> str(hex_(32) + 3)
    '0x23'
    >>> str(hex_(-32))
    '-0x20'
    >>> str(hex_("0x50"))
    '0x50'
    >>> str(hex_("-0b1010000"))
    '-0x50'
    >>> str(hex_("0o50"))
    '0x28'
    >>> hex_("5Z")
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: '5Z'

    A width in bits is optional:

    >>> hex_(32, width=16)
    Hex('0x0020')

    If given, the default width is taken from the value:

    >>> hex_("16'd50")
    Hex('0x0032')

    Smaller widths are not truncated:

    >>> hex_("16'd50", width=4)
    Hex('0x32')
    """
    return Hex(value, width=width)


def bytes_(value: Any) -> Bytes:
    """
    Integer with byte representation, return :any:`Bytes` object.

    >>> bytes_(32*1024*1024)
    Bytes('32 MB')
    >>> str(bytes_(32*1024*1024))
    '32 MB'
    >>> str(bytes_("45000.2 KB"))
    '43.95 MB'
    >>> str(bytes_(Bytes(40*1024)))
    '40 KB'
    >>> str(bytes_("0x1000"))
    '4 KB'
    >>> str(int(bytes_("0x1000")))
    '4096'
    >>> str(bytes_("-0x1000"))
    '-4096 bytes'
    >>> bytes_("5FOO")
    Traceback (most recent call last):
        ...
    ValueError: Invalid number of bytes: '5FOO'
    """
    return Bytes(value)
