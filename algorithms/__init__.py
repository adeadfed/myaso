from PIL.Image import Image
from loguru import logger

from . import LSB, LSBX, colorcode

ALGORITHMS = {
    'LSB': LSB.LSB,
    'LSB-X': LSBX.LSBX,
    'colorcode': colorcode.ColorCode
}


def get_algorithm(algorithm):
    algorithm, *algorithm_args = algorithm.split(',')
    return ALGORITHMS[algorithm](), algorithm_args


def extract_data(input_file, algorithm):
    algorithm, algorithm_args = get_algorithm(algorithm)
    logger.debug(f'Algorithm: {algorithm} {algorithm_args}')
    return algorithm.extract(Image.open(input_file), *algorithm_args)


def embed_data(output_file, algorithm):
    algorithm, algorithm_args = get_algorithm(algorithm)
    image = algorithm.embed(*algorithm_args)
    image.save(output_file)
