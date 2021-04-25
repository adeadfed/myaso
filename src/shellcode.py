import os
import re
import tempfile

from loguru import logger


def from_args(args):
    try:
        msf_path = MSF_RE.findall(args.sc_file)[0]
        logger.debug('Taking shellcode from MSF payload...')
        return from_msf_payload(msf_path, args.custom_args)
    except IndexError:
        pass
    try:
        logger.debug('Reading shellcode from file...')
        return from_file(args.sc_file)
    except FileNotFoundError:
        logger.error(f'File {args.sc_file} not found. Maybe check the path?')


def from_file(sc_filename: str) -> bytes:
    with open(sc_filename, 'rb') as f:
        return f.read()


MSF_RE = re.compile('^msf://(.*)')


def from_msf_payload(msf_path: str, extra_options: list) -> bytes:
    # FIXME: could have used https://pypi.org/project/pymetasploit3/
    with tempfile.TemporaryFile(suffix='bin') as fp:
        os.popen(f'msfvenom -p {msf_path} {extra_options} -f raw -o {fp.name}').read().encode('utf-8')
        fp.seek(0)
        return fp.read()
