import os
import re
import sys


def from_args(args):
    try:
        msf_path = MSF_RE.findall(args.sc_file)[0]
        return from_msf_payload(msf_path, args.custom_args)
    except IndexError:
        pass
    try:
        return from_file(args.sc_file)
    except FileNotFoundError:
        pass  # todo


def from_file(sc_filename: str) -> bytes:
    with open(sc_filename, 'rb') as f:
        return f.read()


MSF_RE = re.compile('^msf://(.*)')


def from_msf_payload(msf_path: str, extra_options: list) -> bytes:
    # FIXME: could have used https://pypi.org/project/pymetasploit3/
    return os.popen(f'msfvenom -p {msf_path} {extra_options} -f raw').read().encode('utf-8')
