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
"""Bytes."""

from typing import Any

from humanfriendly import format_size, parse_size

from . import converter
from .baseint import BaseInt


class Bytes(BaseInt, int):  # type: ignore
    """
    Integer with byte representation.

    >>> Bytes(1)
    Bytes('1 byte')
    >>> Bytes('1 byte')
    Bytes('1 byte')
    >>> str(Bytes(1))
    '1 byte'
    >>> str(Bytes(50))
    '50 bytes'
    >>> str(Bytes(50 * 1024))
    '50 KB'
    >>> str(Bytes(1023))
    '1023 bytes'

    This value behaves like a normal integer.

    >>> str(Bytes(50) + 50)
    '100 bytes'
    >>> 50 + Bytes(50)
    100
    >>> str(Bytes(8) - 2)
    '6 bytes'
    >>> str(Bytes(8) * 3)
    '24 bytes'
    >>> str(Bytes(8) / 3)
    '2 bytes'
    >>> str(Bytes(8) // 3)
    '2 bytes'
    >>> str(Bytes(8) % 5)
    '3 bytes'
    >>> str(Bytes(8) << 1)
    '16 bytes'
    >>> str(Bytes(8) >> 1)
    '4 bytes'
    >>> str(Bytes(8) ** 2)
    '64 bytes'
    >>> str(Bytes(9) & 3)
    '1 byte'
    >>> str(Bytes(8) | 3)
    '11 bytes'
    >>> str(Bytes(9) ^ 3)
    '10 bytes'
    >>> str(divmod(Bytes(9), 3))
    "(Bytes('3 bytes'), Bytes('0 bytes'))"
    >>> str(~Bytes(9))
    '-10 bytes'
    >>> str(-Bytes(9))
    '-9 bytes'
    >>> str(abs(Bytes(-9)))
    '9 bytes'
    >>> str(+Bytes(9))
    '9 bytes'

    >>> Bytes(8) | 'A'
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for |: 'Bytes' and 'str'
    >>> divmod(Bytes(9), 'A')
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for divmod(): 'Bytes' and 'str'

    An integer can retrieved by

    >>> Bytes(50) + 50
    Bytes('100 bytes')
    >>> int(Bytes(50) + 50)
    100

    Corner Cases:

    >>> Bytes(0)
    Bytes('0 bytes')
    >>> Bytes(-5)
    Bytes('-5 bytes')
    """

    def __new__(cls, value: Any):
        try:
            value = converter.int_(value, strcast=_parse_bytes)[0]
        except Exception:
            raise ValueError(f"Invalid number of bytes: '{value}'") from None
        return super().__new__(cls, value)

    def __str__(self):
        ret = format_size(int(self), binary=True)
        return ret.replace("iB", "B")


def _parse_bytes(value):
    return parse_size(value, binary=True)
