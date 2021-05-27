from bitarray import bitarray
from itertools import product
from random import randrange
from PIL import Image

from algorithms.IAlgorithm import IAlgorithm


class ColorCode(IAlgorithm):
    def embed(self, payload: bitarray, img: Image, *args, **kwargs):
        for y, x in product(range(img.height), range(img.width)):
            r, g, b = img.getpixel((x, y))

            """set lsb of each color to target value"""
            if payload: r = self.__set_colorcode(payload.pop(0))
            if payload: g = self.__set_colorcode(payload.pop(0))
            if payload: b = self.__set_colorcode(payload.pop(0))

            img.putpixel((x, y), (r, g, b))

    def extract(self, img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
        payload = bitarray()

        for y, x in product(range(img.height), range(img.width)):
            for byte in img.getpixel((x, y)):
                if not payload_bits:
                    break

                bit = self.__get_colorcode(byte)
                payload.append(bit)
                payload_bits -= 1
        return payload

    def pixels_for(self, n):
        return n / 3

    def __set_colorcode(self, value):
        return randrange(140, 255) if value else randrange(110)

    def __get_colorcode(self, byte):
        return 1 if byte > 128 else 0
