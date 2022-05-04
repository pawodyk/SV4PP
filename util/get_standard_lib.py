"""
Code acquired from https://stackoverflow.com/a/8992937/5230280
"""


# import distutils.sysconfig as sysconfig
# import os
# import sys

# std_lib = sysconfig.get_python_lib(standard_lib=True)

# #print(std_lib)

# for top, dirs, files in os.walk(std_lib):
#     for nm in files:
#         prefix = top[len(std_lib)+1:]
#         if prefix[:13] == 'site-packages':
#             continue
#         if nm == '__init__.py':
#             print(top[len(std_lib)+1:].replace(os.path.sep,'.'))
#         elif nm[-3:] == '.py':
#             print(os.path.join(prefix, nm)[:-3].replace(os.path.sep,'.'))
#         elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
#             print(nm[0:-3])

# for builtin in sys.builtin_module_names:
#     print(builtin)

import json


with open('std_lib.txt', 'r') as input, open("std_lib.json", 'w') as output :
    # lines = f.readlines()
    # lines = f.read().splitlines()

    raw = input.read()
    formated = raw.replace('\n', ' ')
    lines = formated.split(' ')
    REMOVE = ["(Unix)", "(Windows)", "(Linux,",  "FreeBSD)"]
    for i in REMOVE:
        while i in lines:
            lines.remove(i)

    json_data = json.dumps(lines)
    output.write(json_data)
    