from itertools import product, chain
from math import ceil, sqrt
from random import randrange, sample
from PIL import Image
from loguru import logger

from algorithms.IAlgorithm import IAlgorithm


def get_image(src, algorithm, bits):
    if src:
        logger.debug(f'Source image: {src}')
        return Image.open(src)
    else:
        logger.debug('No image supplied. Generating new one...')
        return ImageBuilder(algorithm).build(bits)


def closest_square_of(n):
    return ceil(sqrt(n))


class ImageBuilder:
    def __init__(self, algorithm: IAlgorithm):
        self.algorithm = algorithm

    def build(self, n):
        pixel_dim = closest_square_of(self.algorithm.pixels_for(n))
        img = Image.new(
            mode=self.algorithm.img_mode(), 
            size=(
                pixel_dim,
                pixel_dim
            )
        )
        
        # TODO: alrogithms can supply their own parameters for pictures entirely
        # e.g. PVD: grayscale image, min pixel value = 50, max pixel value = 200
        
        # TODO: change the way images are generated
        if self.algorithm.img_mode() == "RGB":
            # generate list of (R,G,B) tuples with the length of pixel_dim**2
            img_data = sample(
                list(product(range(255), repeat=3)),
                k=pixel_dim ** 2
            )
        else:
            # generate list of (L) tuples with the length of pixel_dim**2
            # PVD requires even pixels nearby
            # TODO: fix PVD extreme cases
            img_data = [randrange(50, 200) for _ in range(pixel_dim ** 2)]
        
        img.putdata(img_data)
        return img

