#!/usr/bin/env python3
import re
import os
import sys
from shutil import rmtree
from git import Repo

BLUE = '\033[94m'
GREEN = '\033[92m'
work_dir = '/tmp/digit_dir/'


def banner():
    print(GREEN + '''
________    .___    ________  .______________
\______ \   |   |  /  _____/  |   \__    ___/
 |    |  \  |   | /   \  ___  |   | |    |   
 |    `   \ |   | \    \_\  \ |   | |    |   
/_______  / |___|  \______  / |___| |____|   
        \/                \/                 
    Made with ♥ by Abdelrhman(@aufzayed)
''')



def digit(name, url, output):
    endpoints = set()
    out = os.path.abspath(output)
    print(f'{BLUE}[+] {GREEN}Cloning {url}')
    # clone the repo into temp dir
    Repo.clone_from(url, f'{work_dir}{name}')
    print(f'{BLUE}[+] {GREEN}repo Clonned')
    # regex by LinkFinder team https://github.com/GerbenJavado/LinkFinder
    endpoints_regex = r"""
    (?:"|')                               # Start newline delimiter
    (
        ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
        [^"'/]{1,}\.                        # Match a domain name (any character + dot)
        [a-zA-Z]{2,}[^"']{0,})              # The domain extension and/or path
        |
        ((?:/|\.\./|\./)                    # Start with /,../,./
        [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
        [^"'><,;|()]{1,})                   # Rest of the characters can't be
        |
        ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
        [a-zA-Z0-9_\-/]{1,}                 # Resource name
        \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
        (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
        |
        ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
        [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
        (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
        |
        ([a-zA-Z0-9_\-]{1,}                 # filename
        \.(?:php|asp|aspx|jsp|json|
             action|html|js|txt|xml)        # . + extension
        (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    )
    (?:"|')                               # End newline delimiter
    """

    files_list = []
    for dirs_paths, dirs_list, files_names in os.walk(work_dir):
        for file_name in files_names:
            files_list.append(os.path.join(dirs_paths, file_name))

    print(f'{BLUE}[+] {GREEN}Extract Endpoints')
    for file in files_list:
        with open(file, 'r') as f:
            try:
                lines = f.readlines()
                for line in lines:
                    regex = re.compile(endpoints_regex, re.VERBOSE)
                    f_endpoints = regex.findall(line)
                    for e in f_endpoints:
                        for i in e:
                            if i != '':
                                if not i[0:7] == 'http://' and not i[0:8] == 'https://':
                                    endpoints.add(i)
                                else:
                                    pass
            except UnicodeDecodeError:
                pass

    for end in sorted(endpoints):
        with open(out, 'a') as file:
            file.write(f'{end}\n')
    print(f'{BLUE}[+] {GREEN}saving results')
    print(f'{BLUE}[+] {GREEN}deleting temp files')
    rmtree(work_dir)
    print(f'{BLUE}[+] {GREEN}{len(endpoints)} Endpoints Found!')


if len(sys.argv) != 3:
    banner()
    print(BLUE + 'Usage: python3 digit <repo url> <output file>')
    print(BLUE + 'Example: python3 digit.py https://github.com/test/testrepo output.txt')
    sys.exit()
else:
    banner()
    repo_name = sys.argv[1].split('/')[-1]
    repo_url = sys.argv[1]
    output_file = sys.argv[2]
    try:
        os.mkdir(work_dir)
    except FileExistsError:
        pass
    digit(repo_name, repo_url, output_file)
