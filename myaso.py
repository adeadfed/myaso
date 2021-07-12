#!/usr/bin/env python3
import os
import shlex
from inspect import Parameter, signature
from textwrap import dedent
from functools import partialmethod
from pathlib import Path
from typing import Optional, List

import colorama
import yaml
from PIL import Image
from PyInquirer import prompt
from bitarray import bitarray
from colorama import Style, Fore
from loguru import logger
import typer

import algorithms
from src import builder
from algorithms import Algorithms
from src.menu import runner_questions, algorithm_selection, algorithm_param_questions
from src.image_builder import get_image

app = typer.Typer(no_args_is_help=True)


def to_kwargs(ctx: typer.Context):
    return dict(token.split('=', 1) for token in shlex.split(''.join(ctx.args)))


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def embed(
        ctx: typer.Context,
        payload_file: typer.FileBinaryRead = typer.Option(..., '-f', '--payload-file', help='file with the payload to embed'),
        image: Optional[Path] = typer.Option(None, '-i', '--image', help='image to use as a source'),
        algorithm: Algorithms = typer.Option(..., '-a', '--algorithm', help='steganographic algorithm to use', prompt=True),
        dst: Path = typer.Option('stego.png', '--out-image', '-o', help='where to save the generated stego')
):
    """Embed your payload to a file with a given algorithm"""
    # TODO: check each argument for emptiness
    sc = payload_file.read()
    byte_length = len(sc)
    logger.debug(f'Shellcode: {sc}')

    payload = bitarray()
    payload.frombytes(sc)
    bit_length = len(payload)

    logger.info(f'Payload size: {byte_length} bytes (save this number!)')
    logger.debug(f'Algorithm: {algorithm.value}')

    algorithm = algorithm.implementation(**to_kwargs(ctx))
    img = get_image(image, algorithm, bit_length)
    algorithm.embed(payload, img)

    img.save(dst)
    logger.artifact(f'Saved the stego to {Fore.RED}{dst}{Style.RESET_ALL}')

    # TODO: ask if the user wants to generate a builder for the algo
    # if args.runner_config:
    #     build(args, PAYLOAD_SIZE=payload_bits, SC_SOURCE=os.path.split(args.dst)[1])


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def read(
        ctx: typer.Context,
        src: Path = typer.Option(..., '-i', '--image', help='stego image'),
        algorithm: Algorithms = typer.Option(..., '-a', '--algorithm', help='steganographic algorithm to use', prompt=True),
        payload_size: int = typer.Option(..., '--payload-size', help='size of the payload (in bits), usually obtained when embedding'),
):
    """Read up to max_bits of your payload with a given algorithm"""
    logger.debug(f'Source image: {src}')
    logger.debug(f'Algorithm: {algorithm}, extracting up to {payload_size} bits')

    img = Image.open(src)
    algorithm = algorithm.implementation(**to_kwargs(ctx))

    payload = algorithm.extract(img, payload_size)
    logger.success('Message: {}', payload.tobytes())


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def bake(
        ctx: typer.Context,
        runner_config: Optional[Path] = typer.Option(None, '--def')
):
    """Build a runner for your payload"""
    if runner_config:
        return builder.get_runner(str(runner_config), **to_kwargs(ctx))

    runner_config = prompt(algorithm_selection)
    algo = algorithms.Algorithms[runner_config['algorithm']].implementation

    runner_config['params'] = {'args': {
        'algorithm': ', '.join(prompt(algorithm_param_questions(algo)).values())
    }}
    runner_config |= prompt(runner_questions)

    try:
        save_config = runner_config['save_config']
        del runner_config['save_config']

        runner_config['arch'] = runner_config.get('arch') or 'x86'

        runner_config['params']['ARTIFACT_PATH'] = runner_config['ARTIFACT_PATH']
        base = os.path.basename(runner_config['ARTIFACT_PATH'])
        runner_config['name'] = os.path.splitext(base)[0]
        del runner_config['ARTIFACT_PATH']

        # TODO: test with options such as `myaso embed ... -a LSBX CHANNEL=1
        logger.debug(runner_config)

        if save_config:
            config_file_location = prompt([dict(
                name='config_file_location',
                type='input',
                message='Location:',
                default='{name}.{language}.yml'.format(**runner_config)
            )])['config_file_location']

            with open(config_file_location, 'w') as f:
                f.write(yaml.dump(runner_config))

        builder.get_runner(runner_config, **to_kwargs(ctx))
    except (KeyError, KeyboardInterrupt):
        exit(0)


@app.callback()
def init(ctx: typer.Context, verbose: bool = typer.Option(False, '-v', '--verbose'), banner: bool = True):
    colorama.init()
    ctx.help_option_names += ['-h']

    class TyperHandler:
        """A custom sink for loguru that disables coloring when it is not supported and corrects tty errors"""
        write = typer.echo

    logger.remove()
    logger.add(TyperHandler, format='<level>{level.icon}</level> {message}', level='DEBUG' if verbose else 'INFO')

    if banner:
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


if __name__ == '__main__':
    logger.level('ERROR', icon=r'[-]')
    logger.level('SUCCESS', icon=r'[+]', color='<bold><green>')
    logger.level('DEBUG', icon=r'[*]', color='')
    logger.level('INFO', icon=r'[!]', color='<bold><yellow>')
    logger.level('ARTIFACT', no=1337, icon=f'{Fore.RED}🥩{Style.RESET_ALL}')
    logger.__class__.artifact = partialmethod(logger.__class__.log, 'ARTIFACT')

    app()
