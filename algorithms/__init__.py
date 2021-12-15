from enum import Enum

from PIL.Image import Image
from loguru import logger

from . import LSB, LSBM, LSBX, colorcode, PVD
from .IAlgorithm import IAlgorithm


class Algorithms(Enum):
    LSB = 'LSB'
    LSBM = 'LSBM'
    LSBX = 'LSBX'
    ColorCode = 'ColorCode'
    PVD = 'PVD'

    @property
    def implementation(self):
        ALGORITHMS = {
            'LSB': LSB.LSB,
            'LSBM': LSBM.LSBM,
            'LSBX': LSBX.LSBX,
            'colorcode': colorcode.ColorCode,
            'PVD': PVD.PVD
        }
        return ALGORITHMS[self.value]


def get_algorithm(algorithm: Algorithms) -> IAlgorithm:
    algorithm, *algorithm_args = algorithm.split(',')
    return


def extract_data(input_file, algorithm):
    algorithm, algorithm_args = get_algorithm(algorithm)
    logger.debug(f'Algorithm: {algorithm} {algorithm_args}')
    return algorithm.extract(Image.open(input_file), *algorithm_args)


def embed_data(output_file, algorithm):
    algorithm, algorithm_args = get_algorithm(algorithm)
    image = algorithm.embed(*algorithm_args)
    image.save(output_file)
