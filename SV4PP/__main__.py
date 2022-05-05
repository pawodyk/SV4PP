#from pstats import SortKey
import click
# import bandit
import subprocess
import json
import os
import sys
import re
import requests
import zipfile

## cosntants
STD_LIB = ["abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys", "compileall", "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email", "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext", "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr", "imp", "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder", "msilib", "msvcrt", "multiprocessing", "netrc", "nis", "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib", "posix", "pprint", "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess", "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "tty", "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo"]
DEP_DIR = 'dependencies'


@click.command()
@click.argument('file')
def runCLI(file):
    """
    SV4PP - Security Verification for Python Packages
 
    """
    
    #temporary check for the virtual enviroment TODO to be imporved
    try :
        print(os.environ['VIRTUAL_ENV'])
    except KeyError as e :
        print('not in virtual enviroment') # TODO ask user do they want to continue.
        exit()

    # gather dependencies 
 
    dependencies = getDepFromProject(file)
    dependencies = remStdLib(dependencies)
    
    print("dependencies list @@ ", dependencies)
    
    

    getDepFromPyPi(dependencies)
    dependencies += extractDepfromFiles()

    getDepFromPyPi(dependencies)
    dependencies += extractDepfromFiles()


    dependencies = deDupList(dependencies)
    dependencies = remStdLib(dependencies)

    print('####')               
    print('final list @@ ',dependencies, '###')

    ## analize the code
      
    

### FUNCTIONS

def getDepFromProject(file):
    dependencies = []
    with open(file, 'r') as f :
        lines = f.readlines()
        
        for line in lines:
            if re.match(r'^(from).\w*.(import)|^(import).*', line) :
                match = re.sub(r'\n|,|^(import).|(from)|\s(import).*|\s(as).*', '', line).strip()
                dependencies+= match.split()
                # for i in dependencies : dependencies.remove(",")

    return dependencies


def remStdLib(dependencies) :
    ## remove any standard library packages
    for std_lib_item in STD_LIB :
        while (std_lib_item in dependencies):
            dependencies.remove(std_lib_item)
            print('removed standard library : ', std_lib_item )
    return dependencies

def extractDepfromFiles():
   
    dependencieslist = []

    for filename in os.listdir(DEP_DIR) :
        dep = os.path.join (DEP_DIR, filename)
        if zipfile.is_zipfile(dep) :
            with zipfile.ZipFile(dep) as archive:
                contents = archive.namelist()
                for i in contents: 
                    
                    if re.search(r'\.dist-info\/METADATA$', i):
                        # print(i, ' match ')
                        meta = archive.open(i).read().decode('utf-8')
                        sub_dep = re.findall(r'Requires-Dist: (.*?)\s', meta) ##TODO include version of the package
                        dependencieslist += sub_dep
                        # print('sd @@ ', sub_dep)
                        # print('d @@ ', dependencieslist)

                        # for line in archive.open(i):
                        #     ln = line.decode('utf-8')
                        #     if re.search(r'(Requires-Dist:)', ln):
                        #         print(ln)
                        #     # if not i in dependencies:
                        #     #     dependencies.append(i)
                        
                    # print(i)
        else :
            print('#### not a wheel : ', filename )
    return dependencieslist


def getDepFromPyPi(dependencies):
    if not os.path.exists(DEP_DIR): os.makedirs(DEP_DIR)

    for dep in dependencies:
        try:
            address = 'https://pypi.org/pypi/{}/json'.format(dep)
            req = requests.get(address)
            resp = req.json()
            # print(resp['info']['name'], " -> ", resp['info']['summary'], "@", address) # gets the info from pypi
            package_url = resp['urls'][0]['url']
            filename = resp['urls'][0]['md5_digest']
            path_to_file = os.path.join(DEP_DIR,filename)
            if not os.path.exists(path_to_file):
                with open(path_to_file, "wb") as package:
                    package.write(requests.get(package_url).content)
        except Exception:
            print('dependency ', dep, 'could not be found, not on PyPi' )
    

def deDupList(inputlist:list):
    deduplist = []
    [deduplist.append(i) for i in inputlist if i not in deduplist]

    return deduplist
    

def banditScan(file):
    ## Bandit analysis
    bandit = subprocess.Popen(["bandit", "-f", "json", file, "-q"], stdout=subprocess.PIPE)
    output = bandit.communicate()
    output_json = json.loads(output[0].decode('utf8'))
    print(type(output_json))

    for x, y in output_json.items() : print(x, y)
    print(output_json['results'])

    for x in output_json['results'] :
        for y, z in x.items() : print(y, z) 

if __name__ == '__main__':
    runCLI()