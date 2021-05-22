from itertools import product

from bitarray import bitarray
from PIL import Image
from .LSB_utils import __from_colorcode, __to_colorcode


def embed(img: Image, payload: bitarray, *args, **kwargs):
    for y, x in product(range(img.height), range(img.width)):
        r, g, b = img.getpixel((x, y))

        """set lsb of each color to target value"""
        if payload: r = __to_colorcode(payload.pop(0))
        if payload: g = __to_colorcode(payload.pop(0))
        if payload: b = __to_colorcode(payload.pop(0))

        img.putpixel((x, y), (r, g, b))


def extract(img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
    payload = bitarray()

    for y, x in product(range(img.height), range(img.width)):
        for byte in img.getpixel((x, y)):
            if not payload_bits:
                break

            bit = __from_colorcode(byte)
            payload.append(bit)
            payload_bits -= 1
    return payload
