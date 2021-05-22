from enum import IntEnum
from itertools import product

from bitarray import bitarray
from PIL import Image
from loguru import logger

from .LSB_utils import __get_lsb, __set_lsb


def capacity(img: Image):
    """Maximum number of least significant bits in ONE channel"""
    return img.height * img.width


def embed(img: Image, payload: bitarray, *args, **kwargs):
    assert len(payload) <= capacity(img), \
        f'[-] payload length ({len(payload)}) is greater than image capacity ({capacity(img)})!'

    idx = Channel[args[0]].value
    logger.debug('LSB-X args: {} {}', args, idx)

    for y, x in product(range(img.height), range(img.width)):
        channels = list(img.getpixel((x, y)))

        if payload: channels[idx] = __set_lsb(channels[idx], payload.pop(0))

        img.putpixel((x, y), tuple(channels))


def extract(img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
    idx = Channel[args[0]].value
    logger.debug('LSB-X args: {} {}', args, idx)
    payload = bitarray()

    for y, x in product(range(img.height), range(img.width)):
        channels = list(img.getpixel((x, y)))
        if not payload_bits:
            break

        bit = __get_lsb(channels[idx])
        payload.append(bit)
        payload_bits -= 1
    return payload


class Channel(IntEnum):
    R = 0
    G = 1
    B = 2
