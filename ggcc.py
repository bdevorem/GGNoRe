#!/usr/bin/env python2.7
#naive implementation of a program that fixes gcc errors
#uses https://github.com/thibauts/duckduckgo
import urllib
import string
import sys
import fileinput
import subprocess
import requests
import random
from bs4 import BeautifulSoup as BSHTML

def edit_line(name, line, new):
    with open(name, 'r') as f:
        data = f.readlines()
    try:
        with open(name, 'w') as f:
            new = [x+'\n' for x in new]
            if len(new) == 1:
                if data[line].strip() == new[0].strip():
                    new[0] = '//' + new[0]
            line = line - 1
            data = data[:line] + new + data[line+1:]
            f.writelines(data)
    except:
        with open(name, 'w') as f:
            f.writelines(data)

def get_code(error):
    error = ''.join([x for x in error if x in string.printable])
    error = 'site:stackoverflow.com '+(' '.join(error.strip().split()))

    q = urllib.quote_plus(error, safe='()/\'\"`')

    requests.get('https://duckduckgo.com/html/?t=h_&ia=web&q=helpme')

    r = requests.get('https://duckduckgo.com/html/?t=h_&ia=web&q='+q)
    BS = BSHTML(r.text, "lxml")

    result = BS.find_all('a', class_ = 'result__a', href = True)
    result = random.choice(result)['href']
    result = urllib.unquote_plus(result.split('uddg=')[-1])

    r = requests.get(result)
    BS = BSHTML(r.text, "lxml")

    return random.choice(BS.find_all('code')).contents

if __name__ == '__main__':
    keep_compiling = True

    while keep_compiling:
        try:
            subprocess.check_output(['gcc', '-Wfatal-errors'] + sys.argv[1:],
                                      stderr=subprocess.STDOUT)
            keep_compiling = False
        except subprocess.CalledProcessError as e:
            try:
                error = e.output.split('\n')[1]
                source, line = error.split(':')[:2]
                print source
                print line
                print error
                edit_line(source, int(line), get_code(error))
                keep_compiling = True #keep going
            except Exception:
                print e.output
                keep_compiling = False
            
