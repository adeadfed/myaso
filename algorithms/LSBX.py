from enum import IntEnum

from bitarray import bitarray
from PIL import Image
from .LSB_utils import __get_lsb, __set_lsb


def capacity(img: Image):
    """Maximum number of least significant bits in ONE channel"""
    return img.height * img.width


def embed(img: Image, payload: bitarray, **kwargs):
    assert len(payload) < capacity(img), '[-] Too much to handle!'

    idx = Channel[kwargs.get('channel') or 'R'].value

    for y, x in zip(range(img.height), range(img.width)):
        channels = list(img.getpixel((x, y)))

        if payload: channels[idx] = __set_lsb(channels[idx], payload.pop(0))

        img.putpixel((x, y), channels)


def extract(img: Image, payload_bits: int, **kwargs) -> bitarray:
    idx = Channel[kwargs.get('channel') or 'R'].value
    payload = bitarray()

    for y, x in zip(range(img.height), range(img.width)):
        channels = list(img.getpixel((x, y)))
        if not payload_bits:
            return payload

        bit = __get_lsb(channels[idx])
        payload.append(bit)
        payload_bits -= 1


class Channel(IntEnum):
    R = 0
    G = 1
    B = 2
