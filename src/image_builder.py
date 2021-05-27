from itertools import product
from math import ceil, sqrt
from random import sample
from PIL import Image
from loguru import logger


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
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def build(self, n):
        pixel_dim = closest_square_of(self.algorithm.pixels_for(n))
        img = Image.new(
            mode="RGB", 
            size=(
                pixel_dim,
                pixel_dim
            )
        )
        
        # generate list of (R,G,B) tuples with the length of pixel_dim**2
        img_data = sample(
            list(product(range(255), repeat=3)),
            k=pixel_dim ** 2
        )
        
        img.putdata(img_data)
        return img

