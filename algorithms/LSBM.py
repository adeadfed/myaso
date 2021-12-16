import random
from itertools import product

from bitarray import bitarray
from PIL import Image

from .LSB import LSB
from .utils import chunks


class LSBM(LSB):
    def embed(self, payload: bitarray, img: Image, *args, **kwargs) -> Image:
        assert len(payload) <= self.capacity(img), \
            f'[-] payload length ({len(payload)}) is greater than image capacity ({self.capacity(img)})!'

        for (y, x), pixel_bits in zip(product(range(img.height), range(img.width)), chunks(payload, 3)):
            r, g, b = img.getpixel((x, y))

            """set lsb of each color to target value"""
            if payload: r = self.set_lsbm(r, pixel_bits[0])
            if payload: g = self.set_lsbm(g, pixel_bits[1])
            if payload: b = self.set_lsbm(b, pixel_bits[2])

            img.putpixel((x, y), (r, g, b))

        return img

    def extract(self, img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
        payload = bitarray()

        for y, x in product(range(img.height), range(img.width)):
            for byte in img.getpixel((x, y)):
                if not payload_bits:
                    break

                bit = self.get_lsbm(byte)
                payload.append(bit)
                payload_bits -= 1
        return payload

    def set_lsbm(self, byte, value):
        if (byte % 2) == value:
            return byte

        if byte == 255:
            return byte - 1
        elif byte == 0:
            return byte + 1
        else:
            return byte + random.choice([-1, 1])

    def get_lsbm(self, byte):
        return byte % 2

    def img_mode(self):
        return "RGB"
