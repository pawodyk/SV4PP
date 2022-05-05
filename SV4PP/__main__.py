#from pstats import SortKey
#from importlib.metadata import requires
import click
# import bandit
import subprocess
import json
import os
import sys
import re
import requests
import zipfile
from datetime import datetime

from setuptools import Require

import report

## constants
STD_LIB = ["abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys", "compileall", "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email", "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext", "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr", "imp", "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder", "msilib", "msvcrt", "multiprocessing", "netrc", "nis", "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib", "posix", "pprint", "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess", "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "tty", "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo"]
DEP_DIR = 'dependencies'
ABS_PATH = os.getcwd() #os.path.dirname(os.path.abspath(__file__))

@click.command()
def runCLI():
    """
    SV4PP - Security Verification for Python Packages
 
    """
    # example = ['certifi', 'charset-normalizer', 'coloredlogs', 'gitdb', 'GitPython', 'humanfriendly', 'idna', 'lxml', 'pyreadline3', 'requests', 'smmap', 'typing-extensions', 'urllib3', 'brotlicffi', 'brotli', 'brotlipy', 'pyOpenSSL', 'cryptography', 'PySocks', 'unicodedata2', 'chardet', 'win-inet-pton', 'capturer', 'cssselect', 'html5lib', 'BeautifulSoup4', 'Cython', 'monotonic', 'pyreadline', 'soupsieve', 'html5lib;', 'lxml;', 'six', 'webencodings', 'genshi', 'pytest', 'coverage', 'pytest-xdist', 'pytest-randomly', 'cffi', 'sphinx', 'sphinx-rtd-theme', 'pyenchant', 'twine', 'sphinxcontrib-spelling', 'black', 'flake8', 'flake8-import-order', 'pep8-naming', 'setuptools-rust', 'bcrypt', 'pytest-benchmark', 'pytest-cov', 'pytest-subtests', 'pretend', 'iso8601', 'pytz', 'hypothesis', 'enum34', 'flaky']
    # sample_package_list = [{'package': 'certifi'}, {'package': 'charset-normalizer'}, {'package': 'coloredlogs'}, {'package': 'gitdb'}, {'package': 'GitPython'}, {'package': 'humanfriendly'}, {'package': 'idna'}, {'package': 'lxml'}, {'package': 'pyreadline3'}, {'package': 'requests'}, {'package': 'smmap'}, {'package': 'typing-extensions'}, {'package': 'urllib3'}, {'package': 'brotlicffi'}, {'package': 'brotli'}, {'package': 'brotlipy'}, {'package': 'pyOpenSSL'}, {'package': 'cryptography'}, {'package': 'PySocks'}, {'package': 'unicodedata2'}, {'package': 'chardet'}, {'package': 'win-inet-pton'}, {'package': 'capturer'}, {'package': 'cssselect'}, {'package': 'html5lib'}, {'package': 'BeautifulSoup4'}, {'package': 'Cython'}, {'package': 'monotonic'}, {'package': 'pyreadline'}, {'package': 'soupsieve'}, {'package': 'html5lib;'}, {'package': 'lxml;'}, {'package': 'six'}, {'package': 'webencodings'}, {'package': 'genshi'}, {'package': 'pytest'}, {'package': 'coverage'}, {'package': 'pytest-xdist'}, {'package': 'pytest-randomly'}, {'package': 'cffi'}, {'package': 'sphinx'}, {'package': 'sphinx-rtd-theme'}, {'package': 'pyenchant'}, {'package': 'twine'}, {'package': 'sphinxcontrib-spelling'}, {'package': 'black'}, {'package': 'flake8'}, {'package': 'flake8-import-order'}, {'package': 'pep8-naming'}, {'package': 'setuptools-rust'}, {'package': 'bcrypt'}, {'package': 'pytest-benchmark'}, {'package': 'pytest-cov'}, {'package': 'pytest-subtests'}, {'package': 'pretend'}, {'package': 'iso8601'}, {'package': 'pytz'}, {'package': 'hypothesis'}, {'package': 'enum34'}, {'package': 'flaky'}]

    #temporary check for the virtual enviroment TODO to be imporved
    try :
        os.environ['VIRTUAL_ENV'] ## if 'VIRTUAL_ENV' in os.environ may be better
    except KeyError as e :
        print('not in virtual enviroment') # TODO ask user do they want to continue.
        exit()

    # input type source / requirements / package
    input_type = 'source'
    input = 'sample\\test2.py'

    ### SECTION: Gather dependencies.... ###

    dependencies = []

    if input_type == 'source':
        if os.path.exists(input) : 
            files = getAllPyFiles(input)
            deplist = []
            filedep = []
            for file in files:
                filedep = getDepFromProject(file)
                for pg in filedep : deplist.append(pg)

            deplist = deDupList(deplist)
            deplist = remStdLib(deplist)
            for package in deplist:
                dependencies.append({'package': package})
                print(package)

    elif input_type=='requirements':
        if os.path.isdir(input):
            input = input + "\\requirements.txt"

        if not os.path.exists(input):
            raise Exception("your requirements files do not exist")
        
        with open(input, 'r') as f:
            req_file = f.read().splitlines()
            for line in req_file:
                # print('@', line)
                match = re.match(r'(^[a-zA-Z0-9\-]+)==([0-9\.]+)', line)
                if match :
                    dependencies.append({'package':match.group(1),'version': match.group(2)})
                    
    elif input_type=='package':
        match = re.match(r'(^[a-zA-Z0-9\-]+)==([0-9\.]+)', input)
        if match :
            dependencies.append({'package':match.group(1),'version': match.group(2)})
        else :
            dependencies.append({'package': input})
    else : 
        raise Exception("Input type need to be specified")

    
    print("gathered dependencies @@ ", dependencies)
    
    dependencies = getDepFromPyPi(dependencies)

    # getDepFromPyPi(dependencies)
    # dependencies += extractDepfromFiles()


    # dependencies = deDupList(dependencies)
    # dependencies = remStdLib(dependencies)

    # print('####')               
    # print('final list @@ ',dependencies, '###')

    

    ## analize the code

    # os.mkdir('temp')
    # os.chdir('temp')

    output = {}

    # r = requests.get('https://raw.githubusercontent.com/pyupio/safety-db/master/data/insecure_full.json')
    # safety_db = r.json() ## TODO check was the data correct

    # for x in safety_db : print(x)

    # database 


    # for package in example :
    #     if package in safety_db:
    #         print(package)
    
    # writeToJSON(output)
    
    # for item in dependencies:
    #     if 'file_path' in item:
    #         print(banditScan(item['file_path']))



    


### FUNCTIONS

def getPyFromSource():
    
    pass


def getPyFromPackage() :
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
    pass


def writeToJSON(output:dict):
    #output = {"example": banditScan('..\\sample\\test.py')}
    timestamp = datetime.now()
    filename = timestamp.strftime('%Y%m%d_%H%M%S') + '.json'
    with open(os.path.join('temp', filename), 'w') as f:
        f.write(json.dumps(output, indent=4))


def getAllPyFiles(input):
    files = []
    output = []
    if os.path.isdir(input):
        for root, dir, file in os.walk(input):
            for f in file:
                files.append(os.path.abspath(os.path.join(root, f)))
    elif os.path.isfile(input):
        files.append(os.path.abspath(input))
    else:
        return []

    for path in files:
        if re.search(r'\.py$', path):
            output.append(path)

    return output


def getDepFromProject(path):
    dependencies = []
    with open(path, 'r') as f :
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
            # print('removed standard library : ', std_lib_item )
    return dependencies


def extractDepfromFiles():
   
    dependencieslist = []

    for filename in os.listdir(DEP_DIR) :
        dep = os.path.join (ABS_PATH, DEP_DIR, filename)
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

## TODO split into gathering informationan and downloading package
def getDepFromPyPi(dependencies):
    if not os.path.exists(DEP_DIR): os.makedirs(DEP_DIR)
    output = []
    for dep in dependencies:
        # try:
        address = 'https://pypi.org/pypi/{}/json'.format(dep['package'])
        req = requests.get(address)
        if req.status_code == 200 :
            resp = req.json()
            print(resp['info']['name'], " -> ", resp['info']['summary'], "@", address) # gets the info from pypi
            if not 'version' in dep:
                dep['version'] = resp['info']['version']
            else:
                try:
                    resp['releases'][dep['version']]
                except KeyError:
                    print('no key')
                    dep['URL'] = resp['urls'][0]['url']
                    dep['hash'] = resp['urls'][0]['md5_digest']

            dep['URL'] = resp['releases'][dep['version']][0]['url']
            dep['hash'] = resp['releases'][dep['version']][0]['md5_digest']


            
            package_url = dep['URL']
            filename = dep['hash']
            path_to_file = os.path.join(ABS_PATH, DEP_DIR,filename)
            dep['file_path'] = path_to_file

            if not os.path.exists(path_to_file):
                with open(path_to_file, "wb") as package:
                    package.write(requests.get(package_url).content)
        output.append(dep)
        # except Exception as ex:
        #     #print('dependency ', dep['package'], 'could not be found, not on PyPi' )
        #     print(ex.with_traceback)
        
    
    print(output)
    return output


def deDupList(inputlist:list):
    deduplist = []
    [deduplist.append(i) for i in inputlist if i not in deduplist]

    return deduplist


def deDupPackages(input:dict):
    pass


def banditScan(path):
    ## Bandit analysis
    report = []
    bandit = subprocess.Popen(["bandit", "-f", "json", path, "-q"], stdout=subprocess.PIPE)
    output = bandit.communicate()
    output_json = json.loads(output[0].decode('utf8'))
    #print(type(output_json))

    #for x, y in output_json.items() : print(x, y)
    # print(output_json['results'])

    for x in output_json['results'] :
        #for y, z in x.items() : print(y, z)
        report.append(x)

    return report

if __name__ == '__main__':
    runCLI()

# class Package:
#     ## define package entity
#     '''
#     package = click
#     hash = 7a8260e7bdac219be27f0bdda48e79ce
#     version = 8.1.3
#     filename = click-8.1.3-py3-none-any.whl
#     packagetype = bdist_wheel | sdist
#     location = 
#     source = dep | subdep | user | req 
#     report = []
#     '''     
#     def __init__(self, name):
#         self.package = name
