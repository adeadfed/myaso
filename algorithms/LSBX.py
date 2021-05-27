from enum import IntEnum
from itertools import product

from bitarray import bitarray
from PIL import Image
from loguru import logger

from .LSB import LSB


class Channel(IntEnum):
    R = 0
    G = 1
    B = 2


class LSBX(LSB):
    def capacity(self, img: Image):
        """Maximum number of least significant bits in ONE channel"""
        return img.height * img.width

    def embed(self, payload: bitarray, img: Image, *args, **kwargs):
        assert len(payload) <= self.capacity(img), \
            f'[-] payload length ({len(payload)}) is greater than image capacity ({self.capacity(img)})!'

        idx = Channel[args[0]].value
        logger.debug('LSB-X args: {} {}', args, idx)

        for y, x in product(range(img.height), range(img.width)):
            channels = list(img.getpixel((x, y)))

            if payload: channels[idx] = self.set_lsb(channels[idx], payload.pop(0))

            img.putpixel((x, y), tuple(channels))

    def extract(self, img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
        idx = Channel[args[0]].value
        logger.debug('LSB-X args: {} {}', args, idx)
        payload = bitarray()

        for y, x in product(range(img.height), range(img.width)):
            channels = list(img.getpixel((x, y)))
            if not payload_bits:
                break

            bit = self.get_lsb(channels[idx])
            payload.append(bit)
            payload_bits -= 1
        return payload

    def pixels_for(self, n):
        return n
