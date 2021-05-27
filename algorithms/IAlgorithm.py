from abc import ABC

from bitarray import bitarray
from PIL.Image import Image


class IAlgorithm(ABC):
    def __init__(self, *args):
        pass

    def capacity(self, img: Image):
        """Maximum number of least significant bits in ONE channel"""
        return img.height * img.width

    def embed(self, payload: bitarray, img: Image, *args, **kwargs):
        raise NotImplementedError

    def extract(self, img: Image, payload_bits: int, *args, **kwargs) -> bitarray:
        raise NotImplementedError

    def pixels_for(self, n):
        raise NotImplementedError
