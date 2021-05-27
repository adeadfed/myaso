from itertools import product
from math import ceil, sqrt
from random import sample
from PIL import Image


class ImageBuilder:
    def __init__(self, n):
        # 1 pixel has 3 bits
        self.pixel_dim = self._get_closest_square(n / 3)
    
    def _get_closest_square(self, n):
        return ceil(sqrt(n))
    
    def build(self):
        img = Image.new(
            mode="RGB", 
            size=(
                self.pixel_dim, 
                self.pixel_dim
            )
        )
        
        # generate list of (R,G,B) tuples with the length of pixel_dim**2
        img_data = sample(
            list(product(range(255),repeat=3)),
            k=self.pixel_dim**2
        )
        
        img.putdata(img_data)
        return img

