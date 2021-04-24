from bitarray import bitarray
from PIL import Image


def __set_lsb(byte, value):
    """
    set last bit to 1 by doing bitwise OR with 0b00000001
    set last bit to 0 by doing bitwise AND with 0b11111110
    """
    return byte | 0b1 if value else byte & ~0b1


def __get_lsb(byte):
    """get last bit by doing bitwise AND with 0b00000001"""
    return byte & 0b1


def capacity(img: Image):
    """Maximum number of least significant bits"""
    return img.height * img.width * 3


def embed(img: Image, payload: bitarray, **kwargs):
    assert len(payload) < capacity(img), '[-] Too much to handle!'

    for y, x in zip(range(img.height), range(img.width)):
        r, g, b = img.getpixel((x, y))

        """set lsb of each color to target value"""
        if payload: r = __set_lsb(r, payload.pop(0))
        if payload: g = __set_lsb(g, payload.pop(0))
        if payload: b = __set_lsb(b, payload.pop(0))

        img.putpixel((x, y), (r, g, b))


def extract_data(img: Image, payload_bits: int, **kwargs) -> bitarray:
    payload = bitarray()

    for y, x in zip(range(img.height), range(img.width)):
        for byte in img.getpixel((x, y)):
            if not payload_bits:
                return payload

            bit = __get_lsb(byte)
            payload.append(bit)
            payload_bits -= 1


# TODO: Reverse LSB
#  for y in reversed(range(img.height))
#    ...
#    payload.append(b_bit)
#    payload.append(g_bit)
#    payload.append(r_bit)
