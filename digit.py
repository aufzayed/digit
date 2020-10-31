#!/usr/bin/env python3
import re
import os
import sys
import argparse
from shutil import rmtree
from git import Repo
from colorama import Fore, init


work_dir = '/tmp/digit_dir/'
init()

def banner():
    print(f'''{Fore.GREEN}
________    .___    ________  .______________
\______ \   |   |  /  _____/  |   \__    ___/
 |    |  \  |   | /   \  ___  |   | |    |   
 |    `   \ |   | \    \_\  \ |   | |    |   
/_______  / |___|  \______  / |___| |____|   
        \/                \/                 
    {Fore.BLUE}Made with {Fore.RED}♥ {Fore.BLUE}by Abdelrhman(@aufzayed){Fore.RESET}
''')
banner()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--repo-list', metavar='', help='a file containing a list of repos to extract data from them')
arg_parser.add_argument('--output', metavar='', help='output directory')
args = arg_parser.parse_args()


if args.repo_list is not None:
    repo_list_abs_path = os.path.abspath(args.repo_list)
    with open(repo_list_abs_path) as repo_list:
        urls_list = [url.split('\n')[0] for url in repo_list.readlines()]
elif args.repo_list is None:
    urls_list = [url.split('\n')[0] for url in sys.stdin]
else:
    sys.exit()

if args.output is not None:
    output_path = os.path.abspath(args.output)
else:
    output_path = os.path.abspath('.')

def digit(name, url, output):
    endpoints = set()
    print(f'{Fore.BLUE}[+] {Fore.GREEN}Cloning {url}')
    # clone the repo into temp dir
    try:
        Repo.clone_from(url, f'{work_dir}{name}')
    except Exception as e:
        print(f'{Fore.RED}[!] Error occurred while cloning {url}')
        print(e)
        pass
    print(f'{Fore.BLUE}[+] {Fore.GREEN}repo Cloned')
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

    print(f'{Fore.BLUE}[+] {Fore.GREEN}Extract Endpoints')
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
        with open(f'{output}/{repo_name}_endpoints.txt', 'a') as file:
            file.write(f'{end}\n')
    print(f'{Fore.BLUE}[+] {Fore.GREEN}saving results')
    print(f'{Fore.BLUE}[+] {Fore.GREEN}{len(endpoints)} Endpoints Found!')


if __name__ == '__main__':
    for url in urls_list:
        repo_name = url.split('/')[-1]
        repo_url = url
        output_file = output_path
        try:
            os.mkdir(work_dir)
        except FileExistsError:
            pass
        digit(repo_name, repo_url, output_file)

    print(f'{Fore.BLUE}[+] {Fore.GREEN}deleting temp files')
    rmtree(work_dir)
