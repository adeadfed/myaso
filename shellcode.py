import os
import re
import sys

MSF_RE = re.compile(b'^msf://(.*)')


def from_args(args):
    try:
        return from_file(args.sc_file)
    except TypeError:
        pass
    try:
        msf_path = MSF_RE.findall(args.sc)[0]
        return from_msf_payload(msf_path, args.custom_args)
    except IndexError:
        if args.sc == '-':
            return sys.stdin.buffer.read()
        else:
            return args.sc


def from_file(sc_filename: str) -> bytes:
    with open(sc_filename, 'rb') as f:
        return f.read()


def from_msf_payload(msf_path: str, custom_options: list) -> bytes:
    # FIXME: could have used https://pypi.org/project/pymetasploit3/
    return os.popen(f'msfvenom -p {msf_path} {custom_options} -f raw').read().encode('utf-8')
