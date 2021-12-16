from itertools import chain

from math import ceil, floor, log
from bitarray import bitarray, util
from PIL import Image

from .IAlgorithm import IAlgorithm
from .utils import chunks

# PVD requires even pixels nearby
# TODO: fix PVD extreme cases
class PVD(IAlgorithm):
    def capacity(self, img: Image):
        """Number of bits to be embedded in worst case scenario"""
        return img.height * img.width // 2

    def embed(self, payload: bitarray, img: Image, *args, **kwargs) -> Image:
        # just to be sure that we are dealing with greyscale image
        img = img.convert('L')

        # last byte is sometimes chewed up, add padding
        payload += bitarray('00000000')
        assert len(payload) <= self.capacity(img), \
                f'[-] payload length ({len(payload)}) is greater than image capacity ({self.capacity(img)})!'
        
        # take grayscale pixels
        pixels = list(img.getdata())

        # group pixels by two
        pixel_pairs = list(chunks(pixels, 2))

        i = 0
        while len(payload):
            # step 1
            d = abs(pixel_pairs[i][1] - pixel_pairs[i][0])
            # step 2
            n = self.get_closest_pf_square(d)
            # step 3
            if d >= 240:
                d_stego = 240 + util.ba2int(payload[:4])
                pixel_pairs[i], payload = self._embed(pixel_pairs[i], d, d_stego, 4, payload)
            else:
                m = floor(log(2 * n, 2)) # log2(2 * n)

                range_min = (n ** 2) - n
                range_mid = (n ** 2) + n - (2 ** m)
                range_max = (n ** 2) + n

                # first subrange
                d_stego = self.search_p_in_range(range_min, range_mid, m + 1, payload)
                if d_stego > 0:
                    pixel_pairs[i], payload = self._embed(pixel_pairs[i], d, d_stego, m + 1, payload)
                else:
                    # second subrange
                    d_stego = self.search_p_in_range(range_mid, range_max, m, payload) 
                    pixel_pairs[i], payload = self._embed(pixel_pairs[i], d, d_stego, m, payload)
            i += 1
        img.putdata(list(chain(*pixel_pairs)))
        return img

    def extract(self, img: Image, payload_bits: int, *args, **kwargs) -> bitarray:

        img = img.convert('L')
        # take greyscale pixels
        pixels = list(img.getdata())

        # group pixels by two
        pixel_pairs = list(chunks(pixels, 2))

        i = 0
        payload = bitarray()

        while payload_bits > 0:
            d_stego = abs(pixel_pairs[i][1] - pixel_pairs[i][0])
            n = self.get_closest_pf_square(d_stego)
            if d_stego >= 240:
                payload += self.get_n_lsb(d_stego, 4)
                payload_bits -= 4
            else:
                m = floor(log(2 * n, 2)) # log2(2*n)
                range_mid = (n ** 2) + n - (2 ** m)

                if d_stego < range_mid:
                    payload += self.get_n_lsb(d_stego, m + 1)
                    payload_bits -= m + 1
                else:
                    payload += self.get_n_lsb(d_stego, m)
                    payload_bits -= m
            i+=1
        return payload

    def pixels_for(self, n):
        return n * 2

    def img_mode(self):
        return "L"

    # predefined perfect square ranges
    PF_SQUARE_RANGES = {
        range(0, 2)    : 1,
        range(2, 6)    : 2,
        range(6, 12)   : 3,
        range(12, 20)  : 4,
        range(20, 30)  : 5,
        range(30, 42)  : 6,
        range(42, 56)  : 7,
        range(56, 72)  : 8,
        range(72, 90)  : 9,
        range(90, 110) : 10,
        range(110, 132): 11,
        range(132, 156): 12,
        range(156, 182): 13,
        range(182, 210): 14,
        range(210, 240): 15,
        range(240, 256): 16
    }

    def get_closest_pf_square(self, n):
        for rng, sqr in self.PF_SQUARE_RANGES.items():
            if n in rng:
                return sqr

    # helpers
    def get_n_lsb(self, n, m):
        return util.int2ba(n)[-m:]
    
    def search_p_in_range(self, min, max, m, secret):
        for p in range(min, max):
            if self.get_n_lsb(p, m) == secret[:m]:
                return p
        return -1
    
    def set_average(self, pixels: list, d: int, d_stego: int) -> tuple:
        avg = abs(d_stego - d) / 2
        if pixels[0] >= pixels[1]:
            if d_stego > d:
                return pixels[0] + ceil(avg), pixels[1] - floor(avg)
            else:
                return pixels[0] - ceil(avg), pixels[1] + floor(avg)
        else:
            if d_stego > d:
                return pixels[0] - ceil(avg), pixels[1] + floor(avg)
            else:
                return pixels[0] + ceil(avg), pixels[1] - floor(avg)
        
    def _embed(self, pixels: list, d: int, d_stego: int, m_range: int, payload: list) -> tuple:
        pixels = self.set_average(pixels, d, d_stego)
        return pixels, payload[m_range:]