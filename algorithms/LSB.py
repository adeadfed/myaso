from itertools import product

from bitarray import bitarray
from PIL import Image
from .LSB_utils import __get_lsb, __set_lsb


def capacity(img: Image):
    """Maximum number of least significant bits"""
    return img.height * img.width * 3


def embed(img: Image, payload: bitarray, **kwargs):
    assert len(payload) <= capacity(img), \
        f'[-] payload length ({len(payload)}) is greater than image capacity ({capacity(img)})!'

    for y, x in product(range(img.height), range(img.width)):
        r, g, b = img.getpixel((x, y))

        """set lsb of each color to target value"""
        if payload: r = __set_lsb(r, payload.pop(0))
        if payload: g = __set_lsb(g, payload.pop(0))
        if payload: b = __set_lsb(b, payload.pop(0))

        img.putpixel((x, y), (r, g, b))


def extract(img: Image, payload_bits: int, **kwargs) -> bitarray:
    payload = bitarray()

    for y, x in product(range(img.height), range(img.width)):
        for byte in img.getpixel((x, y)):
            if not payload_bits:
                break

            bit = __get_lsb(byte)
            payload.append(bit)
            payload_bits -= 1
    return payload

# TODO: Reverse LSB
#  for y in reversed(range(img.height))
#    ...
#    payload.append(b_bit)
#    payload.append(g_bit)
#    payload.append(r_bit)
