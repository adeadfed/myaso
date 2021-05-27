from itertools import product
from bitarray import bitarray
from PIL import Image
from random import randrange

def embed(img: Image, payload: bitarray, **kwargs):
    
    for y, x in product(range(img.height), range(img.width)):
        r, g, b = img.getpixel((x, y))

        """set lsb of each color to target value"""
        if payload: r = __set_colorcode(payload.pop(0))
        if payload: g = __set_colorcode(payload.pop(0))
        if payload: b = __set_colorcode(payload.pop(0))

        img.putpixel((x, y), (r, g, b))


def extract(img: Image, payload_bits: int, **kwargs) -> bitarray:
    payload = bitarray()

    for y, x in product(range(img.height), range(img.width)):
        for byte in img.getpixel((x, y)):
            if not payload_bits:
                break

            bit = __get_colorcode(byte)
            payload.append(bit)
            payload_bits -= 1
    return payload


def __set_colorcode(value):
    # return 255 if value else 0
    return randrange(140, 255) if value else randrange(110) 

def __get_colorcode(byte):
    return 1 if byte > 128 else 0