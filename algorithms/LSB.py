from itertools import product

from bitarray import bitarray
from PIL import Image

from .IAlgorithm import IAlgorithm
from .utils import chunks


class LSB(IAlgorithm):
    def capacity(self, img: Image):
        """Maximum number of least significant bits"""
        return img.height * img.width * 3

    def embed(self, payload: bitarray, img: Image, *args, **kwargs):
        assert len(payload) <= self.capacity(img), \
            f'[-] payload length ({len(payload)}) is greater than image capacity ({self.capacity(img)})!'

        for (y, x), pixel_bits in zip(product(range(img.height), range(img.width)), chunks(payload, 3)):
            r, g, b = img.getpixel((x, y))

            """set lsb of each color to target value"""
            if payload: r = self.set_lsb(r, pixel_bits[0])
            if payload: g = self.set_lsb(g, pixel_bits[1])
            if payload: b = self.set_lsb(b, pixel_bits[2])

            img.putpixel((x, y), (r, g, b))

        return img

    def extract(self, img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
        payload = bitarray()

        for y, x in product(range(img.height), range(img.width)):
            for byte in img.getpixel((x, y)):
                if not payload_bits:
                    break

                bit = self.get_lsb(byte)
                payload.append(bit)
                payload_bits -= 1
        return payload

    def pixels_for(self, n):
        return n / 3

    def set_lsb(self, byte, value):
        """
        set last bit to 1 by doing bitwise OR with 0b00000001
        set last bit to 0 by doing bitwise AND with 0b11111110
        """
        return byte | 0b1 if value else byte & ~0b1

    def get_lsb(self, byte):
        """get last bit by doing bitwise AND with 0b00000001"""
        return byte & 0b1

    def img_mode(self):
        return "RGB"