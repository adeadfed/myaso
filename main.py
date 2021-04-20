"""
C implementation reads pixels left to right, top to bottom
Python implementation reads pixels left to right, bottom to top!
"""
import argparse

from PIL import Image
from bitarray import bitarray

from algorithms import LSB


ALGORITHMS = ['LSB']


def read_sc_file(sc_filename):
    with open(sc_filename, 'rb') as f:
        sc_bits = bitarray()
        sc_bits.fromfile(f)
    return sc_bits.tolist()


def save_encoded_image(source_file, dest_file, payload_bytes: bytes):
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
        description='A steganographic shellcode obfuscator. ' + \
                    'The executor reads data from a BMP image and executes it ' + \
                    'using VirtualAlloc/HeapAlloc. '
    )

    shellcode_source = parser.add_mutually_exclusive_group(required=True)
    shellcode_source.add_argument('-f', type=str, help='File with shellcode', dest='sc_file')
    shellcode_source.add_argument('--sc', type=bytes, help='Shellcode encoded as Python bytes', dest='sc')

    parser.add_argument('-i', type=str, help='Source image', required=True, dest='src')
    parser.add_argument('-o', type=str, help='Destination image', required=True, dest='dst')

    parser.add_argument('-a', type=str, help=f'Algorithm to use. Available options: {", ".join(ALGORITHMS)}')
    
    args = parser.parse_args()

    if args.sc_file:
        with open(args.sc_file, 'rb') as f:
            args.sc = f.read()

    save_encoded_image(args.src, args.dst, args.sc)
    payload = read_encoded_image(args.dst, 5737*8)
    print(payload)