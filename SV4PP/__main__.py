#from pstats import SortKey
#from importlib.metadata import requires
# from codecs import ignore_errors
# from pydoc import describe
from platform import release
import shutil
from textwrap import indent
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

# from setuptools import Require
import urllib

from packaging.specifiers import SpecifierSet
from packaging.version import Version

# import report

## constants
STD_LIB = ["abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys", "compileall", "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email", "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext", "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr", "imp", "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder", "msilib", "msvcrt", "multiprocessing", "netrc", "nis", "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib", "posix", "pprint", "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess", "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "tty", "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo"]
DEP_DIR = os.path.join('temp', 'dependencies')
ABS_PATH = os.getcwd() #os.path.dirname(os.path.abspath(__file__))
VERBOSE_LVL = 1

@click.command()
@click.argument('input')
def runCLI(input):
    """
    SV4PP - Security Verification for Python Packages
    
    INPUT:\n
    \t-> path to your python project or file OR\n
    \t-> path to requirements.txt OR\n
    \t-> package name in the format package==1.1.1
    """

    '''
    package = click
    hash = 7a8260e7bdac219be27f0bdda48e79ce
    version = 8.1.3
    filename = click-8.1.3-py3-none-any.whl
    package_URL = https://files.pythonhosted.org/packages/[...]]/requests-2.27.1-py2.py3-none-any.whl
    package_path = ...//dependencies//7a8260e7bdac219be27f0bdda48e79ce
    package_type = wheel | tarball
    source_path = ...//temp//7a8260e7bdac219be27f0bdda48e79ce
    source = proj | req | pack | pypi
    report = []
    
    '''     


    print()
    print('##########################')
    print('##### STARTING SV4PP #####')
    print('##########################')
    print()

    createTempDir()

    # example = ['certifi', 'charset-normalizer', 'coloredlogs', 'gitdb', 'GitPython', 'humanfriendly', 'idna', 'lxml', 'pyreadline3', 'requests', 'smmap', 'typing-extensions', 'urllib3', 'brotlicffi', 'brotli', 'brotlipy', 'pyOpenSSL', 'cryptography', 'PySocks', 'unicodedata2', 'chardet', 'win-inet-pton', 'capturer', 'cssselect', 'html5lib', 'BeautifulSoup4', 'Cython', 'monotonic', 'pyreadline', 'soupsieve', 'html5lib;', 'lxml;', 'six', 'webencodings', 'genshi', 'pytest', 'coverage', 'pytest-xdist', 'pytest-randomly', 'cffi', 'sphinx', 'sphinx-rtd-theme', 'pyenchant', 'twine', 'sphinxcontrib-spelling', 'black', 'flake8', 'flake8-import-order', 'pep8-naming', 'setuptools-rust', 'bcrypt', 'pytest-benchmark', 'pytest-cov', 'pytest-subtests', 'pretend', 'iso8601', 'pytz', 'hypothesis', 'enum34', 'flaky']
    # sample_package_list = [{'package': 'certifi'}, {'package': 'charset-normalizer'}, {'package': 'coloredlogs'}, {'package': 'gitdb'}, {'package': 'GitPython'}, {'package': 'humanfriendly'}, {'package': 'idna'}, {'package': 'lxml'}, {'package': 'pyreadline3'}, {'package': 'requests'}, {'package': 'smmap'}, {'package': 'typing-extensions'}, {'package': 'urllib3'}, {'package': 'brotlicffi'}, {'package': 'brotli'}, {'package': 'brotlipy'}, {'package': 'pyOpenSSL'}, {'package': 'cryptography'}, {'package': 'PySocks'}, {'package': 'unicodedata2'}, {'package': 'chardet'}, {'package': 'win-inet-pton'}, {'package': 'capturer'}, {'package': 'cssselect'}, {'package': 'html5lib'}, {'package': 'BeautifulSoup4'}, {'package': 'Cython'}, {'package': 'monotonic'}, {'package': 'pyreadline'}, {'package': 'soupsieve'}, {'package': 'html5lib;'}, {'package': 'lxml;'}, {'package': 'six'}, {'package': 'webencodings'}, {'package': 'genshi'}, {'package': 'pytest'}, {'package': 'coverage'}, {'package': 'pytest-xdist'}, {'package': 'pytest-randomly'}, {'package': 'cffi'}, {'package': 'sphinx'}, {'package': 'sphinx-rtd-theme'}, {'package': 'pyenchant'}, {'package': 'twine'}, {'package': 'sphinxcontrib-spelling'}, {'package': 'black'}, {'package': 'flake8'}, {'package': 'flake8-import-order'}, {'package': 'pep8-naming'}, {'package': 'setuptools-rust'}, {'package': 'bcrypt'}, {'package': 'pytest-benchmark'}, {'package': 'pytest-cov'}, {'package': 'pytest-subtests'}, {'package': 'pretend'}, {'package': 'iso8601'}, {'package': 'pytz'}, {'package': 'hypothesis'}, {'package': 'enum34'}, {'package': 'flaky'}]

    #temporary check for the virtual enviroment TODO to be imporved
    try :
        os.environ['VIRTUAL_ENV'] ## if 'VIRTUAL_ENV' in os.environ may be better
    except KeyError as e :
        print('not in virtual enviroment') # TODO ask user do they want to continue.
        exit()
    

    # input type source / requirements / package
    input_type = 'requirements'

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
                dependencies.append({'package': package, 'source': 'user'})
                # print(package)

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
                    dependencies.append({'package':match.group(1),'version': match.group(2), 'source': 'req'})
                    
    elif input_type=='package':
        match = re.match(r'(^[a-zA-Z0-9\-]+)==([0-9\.]+)', input)
        if match :
            dependencies.append({'package':match.group(1),'version': match.group(2)})
        else :
            dependencies.append({'package': input})
    else : 
        raise Exception("Input type need to be specified")

    
    # print("gathered dependencies @@ ", dependencies)
    print('### Getting package info from PyPi###')
    dependencies = getInfoFromPyPi(dependencies)

    print('### Extracting Dependencies from the packages ###')
    sub_dep = []
    temp_list = []
    for dep in dependencies:
        path = dep['package_path']
        sub_dep.append(extractDependenciesfromPackage(path))
    
    for sub_list in sub_dep:
        if sub_list:
            for sub_pg in sub_list:
                temp_list.append(sub_pg)
        else:
            # print('subdep should be empty : ', sub_list)
            pass
    
    dependencies = dependencies + temp_list 
 

    # print(sub_dep)
    # print(dependencies)
    print('### Extracting Source from the packages ###')
    for d in dependencies:
        if 'package_path' in d:        
            file_path = d['package_path']
            # print(file_path)
            d['source_files'] = extractSourceFromPackage(file_path)


    # extractSourceFromPackage()

    # banditScan(os.path.join(ABS_PATH, 'temp', 'bandit'))
    
    # ### CHECK
    # for d in temp_list:
    #     print('###')
    #     for x,y in d.items():
    #         print(x,' : ', y)

    
    

    



    # getDepFromPyPi(dependencies)
    # dependencies += extractDepfromFiles()

    # dependencies = deDupList(dependencies)
    # dependencies = remStdLib(dependencies)

    # print('####')               
    # print('final list @@ ',dependencies, '###')


    ## analize the code

    #for x in safety_db : print(x)

    # databases
    print('### checking package in Safety-DB ###')
    safety_db = requests.get('https://raw.githubusercontent.com/pyupio/safety-db/master/data/insecure_full.json').json() ## TODO check was the data correct
    
    for package in dependencies :
        name = package['package']
        version = package['version']

        if name in safety_db:
            return_list = []
            safety_results = safety_db[name]
            # print(type(safety_results))
            # print('### ', name, ' == ', version)

            for x in range(len(safety_results)):
                specs = safety_results[x]['specs']
                for spec in specs:
                    is_relevent = Version(version) in SpecifierSet(spec)
                    # print('{} is {}'.format(spec, is_relevent))
                    if is_relevent:
                        return_list.append(safety_results[x])

                # print(safety_results[x]['id'])
                # print(safety_results)
                
            # print(return_list)
            package['safety_db'] = return_list

    print('### checking package in OSV ###')
    ### OSV check
    #     postdata = '{"version": "%s", "package": {"name": "%s", "ecosystem": "PyPI"}}'%(version,name)
    #     #print('\t***********\tBAZINGA!!\t***********\n')
    #     print(postdata)
    #     r = requests.post(url='https://api.osv.dev/v1/query', data=postdata)
    #     resp_json = r.json()
    #     print(r.status_code,resp_json)
    #     if r.status_code == 200 and resp_json != {} :
    #         # package['OSV'] = resp_json
    #         print('condition for package ', name)
    for package in dependencies:
        name = package['package']
        version = package['version']
        postdata = '{"version": "%s", "package": {"name": "%s", "ecosystem": "PyPI"}}'%(version,name)
        r = requests.post(url='https://api.osv.dev/v1/query', data=postdata)
        test = r.json()
        
        if 'vulns' in test :
            osv_vulns = []
            for entry in test['vulns']:
                temp = {'id' : entry['id'], 'details' : entry['details'], 'aliases': entry['aliases']}
                urls = []
                for alias in entry['aliases']:
                    if re.match(r'^CVE-',alias):
                        urls.append('https://nvd.nist.gov/vuln/detail/' + alias)
                    elif re.match(r'^GHSA-', alias):
                        urls.append('https://github.com/advisories/' + alias)
                temp['urls'] = urls
                osv_vulns.append(temp)
            package['OSV'] = osv_vulns

 
    
    
    
    # for item in dependencies:
    #     if 'file_path' in item:
    # banditScan('D:\\OneDrive - Technological University Dublin\\@Individual Project\\Program\\temp\\src\\click\\')
    print('### checking python source with bandit ###')
    for dep in dependencies:
        bandit_results = []
        src_file_list = dep['source_files']
        for src_file in src_file_list:
            # print('bandit scan @ ', src_file)
            bandit_results.append(banditScan(src_file))
        dep['bandit'] = bandit_results
    if VERBOSE_LVL == 1:
        print()
    
    print('### checking packages for typosquatting ###')
    pypi_scan_path = os.path.join(ABS_PATH, 'SV4PP\IQTLabs\pypi-scan')
    if os.path.exists(pypi_scan_path):
        for dep in dependencies:
            package_name = dep['package']
            if VERBOSE_LVL >=2 :
                print('I am checking for possible typosquatting for package :: ', package_name)
            elif VERBOSE_LVL >=1:
                print('.', end=' ', flush=True)
            pypi_scan = subprocess.Popen(['py', 'main.py', '-m', package_name], stdout=subprocess.PIPE, cwd=pypi_scan_path)
            out1, out2 = pypi_scan.communicate(timeout=30)
            output = out1.decode('utf8')
            typo_candidates = re.findall(r'[0-9]{1,2}\: ([a-zA-Z0-9\-\_\.]+)',output)
            dep['typo_candidates'] = typo_candidates
            if VERBOSE_LVL >=2 :
                print('done checking %s for typosquatting'%package_name)
        if VERBOSE_LVL == 1:
            print()
    else:
        print("pypi-scan could not be found")
    print('### Writing report to file')
    writeReportToJSON(dependencies)

    print()
    print('##########################')
    print('### ANALYSIS COMPLETED ###')
    print('##########################')
    print()

    # user_input = input('what would you like to do\n')

    # ### CHECK
    # for d in dependencies:
    #     print("###")
    #     for x,y in d.items():
    #         print(x,' : ', y)
    


### FUNCTIONS

def getPyFromSource():
    
    pass


def writeReportToJSON(output:dict):
    #output = {"example": banditScan('..\\sample\\test.py')}
    timestamp = datetime.now()
    filename = timestamp.strftime('%Y%m%d_%H%M%S') + '.json'
    output_folder = os.path.join(ABS_PATH, 'reports')

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    with open(os.path.join(output_folder, filename), 'w') as f:
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


def extractDependenciesfromPackage(file_path):
    dependencieslist = []
    # depdir = os.path.join (ABS_PATH, DEP_DIR)
    dir_path = os.path.dirname(file_path)

    if zipfile.is_zipfile(file_path) :
        with zipfile.ZipFile(file_path) as archive:
            contents = archive.namelist()
            for i in contents: 
                
                if re.search(r'\.dist-info\/METADATA$', i):
                    # print(i, ' match ')
                    meta = archive.open(i).read().decode('utf-8')
                    parent = re.search(r'\nName: ([a-zA-Z0-9\-\_\.]+)\n', meta).group(1)
                    sub_dep = re.findall(r'Requires-Dist: ([a-zA-Z0-9\-\_\.]+)', meta) ##TODO include version of the package
                    
                    for item in sub_dep:
                        dependencieslist.append({'package': item, 'source': 'meta', 'parent': parent})
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
        if VERBOSE_LVL > 1:
            print('could not extract dependencies for %s, package not in wheel format.'%file_path )
        pass
    
    
    dependencieslist = getInfoFromPyPi(dependencieslist)
    return dependencieslist
    pass


def extractSourceFromPackage(file_path):
    tempdir = os.path.join(ABS_PATH, 'temp', 'src')
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)

    source_path_list = []

    # depdir = os.path.join(ABS_PATH, DEP_DIR)

    # createTempDir('src')

    # for filename in os.listdir(depdir):
    #     location = os.path.join(depdir, filename)
    if zipfile.is_zipfile(file_path) :
        with zipfile.ZipFile(file_path, 'r') as archive:
            for file in archive.namelist():
                if re.search(r'\.py$', file):
                    extract_path = os.path.join(tempdir, '\\'.join(file.split('/')) )
                    # extract_dir = os.path.join(tempdir, extract_path)
                    archive.extract(file, tempdir)
                    source_path_list.append(extract_path)
                # else:
                #     print('not source files',file)

        # else :
            #print(depdir, ' @ ' , filename  )
    return source_path_list

def createTempDir():
    temp_dir = os.path.join(ABS_PATH, 'temp')
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
       

def removeTempDir():
    temp_dir = os.path.join(ABS_PATH, 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=False)


def getPackageFromPyPi(file_path, pypi_URL):
    if not os.path.exists(DEP_DIR): os.makedirs(DEP_DIR)
    pypi_URL = urllib.parse.quote(pypi_URL, safe=':/')
    if re.match(r'^(https:\/\/files.pythonhosted.org\/packages).+(\.tar\.gz|\.whl)$', pypi_URL):
        if not os.path.exists(file_path):
            with open(file_path, "wb") as package:
                package.write(requests.get(pypi_URL).content)
        return file_path #if file exists or was downloaded return file path.
    else:
        return None # if the file could not be written or something
        # raise Exception('not a pypi repository')

    
def getInfoFromPyPi(dependencies):
    
    output = []
    for dep in dependencies:
        # try:
        address_latest = 'https://pypi.org/pypi/{}/json'.format(dep['package'])
        if 'version' in dep:
            version_address = 'https://pypi.org/pypi/{}/{}/json'.format(dep['package'],dep['version'])
            req = requests.get(version_address)
            if req.status_code != 200:
                req = requests.get(address_latest)
        else:
            req = requests.get(address_latest)

        if req.status_code == 200 :
            resp = req.json()
            pypi_info = resp['info']
            pypi_pg = None
            if len(resp['urls']) > 0:
                pypi_pg = resp['urls'][0]
                
            else :
                releases = resp['releases']
                lastkey = list(releases.keys())[-1]
                pypi_pg = releases[lastkey][0]
                dep['version'] = pypi_info['version']


                #print('Error: there is no version {} for package {}; using latest version: {}'.format(dep['version'], dep['package'], pypi_info['version']))
            
            if not 'version' in dep:
                dep['version'] = pypi_info['version']        

            #print(resp_info['name'], " -> ", resp_info['summary'], "@", address) # gets the info from pypi

            dep['package_URL'] = pypi_pg['url']
            dep['hash'] = pypi_pg['md5_digest']
            # print(dep)
           
            dep['package_path'] = getPackageFromPyPi(os.path.join(ABS_PATH, DEP_DIR,dep['hash']), dep['package_URL'])
            if 'package_path' in dep:
                pg_type = ''
                if pypi_pg['packagetype'] == 'bdist_wheel':
                    pg_type = 'wheel'
                elif pypi_pg['packagetype'] == 'sdist':
                    pg_type = 'tarball'
                dep['package_type'] = pg_type
            
            # if 'requires_dist' in resp_info and resp_info['requires_dist'] is not None:
            #     for subdep in resp_info['requires_dist']:
            #         match = re.match(r'(^[a-zA-Z0-9\-\_\.]+)\s(\([0-9\>\<\]+|\)\,\=\.\~\!]*)', subdep)
            
            
            # pypi_vuln = resp['vulnerabilities']
            # print(pypi_vuln)
            #dep['PyPi_vulns'] = pypi_vuln ### not needed, same results as OSV

        output.append(dep)
        # except Exception as ex:
        #     #print('dependency ', dep['package'], 'could not be found, not on PyPi' )
        #     print(ex.with_traceback)
        
    
    # print(output)
    return output


def deDupList(inputlist:list):
    deduplist = []
    [deduplist.append(i) for i in inputlist if i not in deduplist]

    return deduplist


# def deDupPackages(input:dict):
#     pass


def banditScan(path):
    ## Bandit analysis
    if VERBOSE_LVL >= 2:
        print('Bandit checking ', path)
    elif VERBOSE_LVL ==1 :
        print('.', end=' ', flush=True)
    report = []
    bandit = subprocess.Popen(["bandit", path, '-f', 'json', '-r', '-q'], stdout=subprocess.PIPE)
    # bandit.wait(timeout=30)
    out1, out2 = bandit.communicate(timeout=30)
    output_json = json.loads(out1.decode('utf8'))
    # print(type(output_json))

    # for x, y in output_json.items() : print(x, y)
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
