import re
from sre_constants import error
import string
import random

rand_namespace = string.ascii_letters + string.digits

with open('../../test.ps1', 'rb') as f:
    contents = f.read().decode('utf-8')

multi_tab_regex = r'(\s){2,}'                                # replaces multiple whitespace characters with ';'
wspace_operator_regex = r'\s(([\[\]=|+\-*\/])+)\s'           # replaces whitespaces on the sides of operator e.g. a = b -> a=b
wspace_declaration_regex = r'([\[\]()$,{}])\s([\[\]()$,{}])' # replaces whitespaces inbetween declarations e.g. function a() {...} -> function a(){...}

func_regex = r'function ((\w)+)'                             # matches format of function names 
var_regex = r'\$\w+'                                         # matches format of PowerShell variable

contents = re.sub(multi_tab_regex, ';', contents)
contents = re.sub(wspace_operator_regex, '\g<1>', contents)
contents = re.sub(wspace_declaration_regex, '\g<1>\g<2>', contents)


script_vars = set(re.findall(var_regex, contents))
script_vars = sorted(script_vars, key=len, reverse=True)

script_funcs = set(x[0] for x in re.findall(func_regex, contents))
script_funcs = sorted(script_funcs, key=len, reverse=True)

# specify here a list of variables to be ignored upon replacing
const_vars = ['$true', '$false']

for var in const_vars:
    try:
        script_vars.remove(var)
    except ValueError:
        pass


for var in script_vars:
    rand_var = '$' + ''.join(random.choice(rand_namespace) for _ in range(random.randrange(3,10)))

    print('[+] Replacing: {} -> {}'.format(var, rand_var))
    contents = contents.replace(var, rand_var)

for func in script_funcs:
    rand_func = ''.join(random.choice(rand_namespace) for _ in range(random.randrange(3,10)))
    print('[+] Replacing: {} -> {}'.format(func, rand_func))
    contents = contents.replace(func, rand_func)

print(contents)