#!/usr/bin/env python2.7
#naive implementation of a program that fixes gcc errors
#uses https://github.com/thibauts/duckduckgo

import sys
import fileinput
import subprocess
import duckduckgo
import requests
from bs4 import BeautifulSoup as BSHTML

def edit_line(name, line, new):
    with open(name, 'r') as f:
        data = f.readlines()
    with open(name, 'w') as f:
        new = [x+'\n' for x in new]
        line = line - 1
        data = data[:line] + new + data[line+1:]
        f.writelines(data)

def get_code(error):
    error = 'site:stackoverflow.com '+error
    result = [l for l in duckduckgo.search(error, max_results=1)][0]
    print result
    r = requests.get(result)
    BS = BSHTML(r.text, "lxml")
    return BS.find_all('code')[-1].contents

if __name__ == '__main__':
    keep_compiling = True

    while keep_compiling:
        try:
            subprocess.check_output(['gcc', '-Wfatal-errors'] + sys.argv[1:],
                                      stderr=subprocess.STDOUT)
            keep_compiling = False
        except subprocess.CalledProcessError as e:
            print e.output
            line = e.output.split(':')[1]
            error = e.output.split('\n')[1]
            source = error.split(':')[:2]
            print source
            print line
            print error
            edit_line(source, int(line), get_code(error))
            keep_compiling = False
            
