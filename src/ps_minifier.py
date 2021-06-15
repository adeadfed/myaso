import re
import string
import random

from loguru import logger


TAB_RE = re.compile(r'[\t\r\n]+|\s{2,}')  # replaces multiple whitespace characters with ';'
WSPACE_OP_RE = re.compile(r'\s(([\[\]=|+\-*\/,])+)\s')  # replaces whitespaces on the sides of operator e.g. a = b -> a=b
WSPACE_DECLARATION_RE = re.compile(r'([\[\]()$,{}])\s([\[\]()$,{}])')  # replaces whitespaces inbetween declarations e.g. function a() {...} -> function a(){...}

FUNC_RE = re.compile(r'function ((\w)+)')  # matches format of function names
VAR_RE = re.compile(r'\$\w+')  # matches format of PowerShell variable

SPECIAL_VARIABLES = {'$true', '$false'}


def minify_PS(contents: str) -> str:
    contents = remove_white_space(contents)

    script_vars = set(VAR_RE.findall(contents))
    script_vars -= SPECIAL_VARIABLES

    contents = replace_with_random_names(contents, script_vars, fake_variable)

    script_funcs = set(x[0] for x in FUNC_RE.findall(contents))
    contents = replace_with_random_names(contents, script_funcs, fake_name)

    return contents


def replace_with_random_names(text, names_to_replace, name_generator):
    for func in sorted(names_to_replace, key=len, reverse=True):
        rand_func = name_generator()
        logger.debug('[+] Replacing: {} -> {}'.format(func, rand_func))
        text = text.replace(func, rand_func)
    return text


def remove_white_space(contents):
    contents = TAB_RE.sub(';', contents)
    contents = WSPACE_OP_RE.sub('\g<1>', contents)
    contents = WSPACE_DECLARATION_RE.sub('\g<1>\g<2>', contents)
    return contents


def fake_name():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randrange(3, 10)))


def fake_variable():
    return '$' + fake_name()

