#!/usr/bin/env python2.7
#naive implementation of a program that fixes gcc errors
#uses https://github.com/thibauts/duckduckgo

# Copyright (c) 2019 Breanna Devore-McDonald and John Westhoff.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import urllib
import string
import sys
import fileinput
import subprocess
import requests
from time import sleep
import random
from datetime import datetime
from bs4 import BeautifulSoup as BSHTML

def edit():
    history = set()
    def edit_line(name, line, new):
        print(history)
        with open(name, 'r') as f:
            data = f.readlines()
        try:
            with open(name, 'w') as f:
                new = [x+'\n' for x in new]
                line = line - 1
                if (name, line, data[line]) in history:
                    new[0] = '//' + new[0]
                data2 = data[:line] + new + data[line+1:]
                f.writelines(data2)
                history.add((name, line, data[line]))
        except:
            try:
                with open(name, 'w') as f:
                    f.writelines(data)
            except Exception as E:
                togo = random.choice(list(history))
                history.remove(togo)
                edit_line(togo[0], togo[1], '\\oops')
                print(E)
    return edit_line


def get_code(error):
    error = ''.join([x for x in error if x in string.printable])
    error = 'site:stackoverflow.com '+(' '.join(error.strip().split()))

    while True:
        try:
            q = urllib.parse.quote_plus(error, safe='()/\'\"`')
            r = requests.get('https://duckduckgo.com/html/?t=h_&ia=web&q='+q)
            BS = BSHTML(r.text, "lxml")

            result = BS.find_all('a', class_ = 'result__a', href = True)
            result = random.choice(result)['href']
            print(result)
            result = urllib.parse.unquote_plus(result.split('uddg=')[-1])

            r = requests.get(result)
            BS = BSHTML(r.text, "lxml")

            return random.choice(BS.find_all('code')).contents
        except Exception as E:
            print('gimme something: ',)
            q = sys.stdin.readline()
            q = urllib.parse.quote_plus(q)
            requests.get('https://duckduckgo.com/html/?t=h_&ia=web&q='+q)
            sleep(1)


if __name__ == '__main__':
    keep_compiling = True
    edit_line = edit()

    while keep_compiling:
        try:
            subprocess.check_output(['gcc', '-Wfatal-errors'] + sys.argv[1:],
                                      stderr=subprocess.STDOUT)
            keep_compiling = False
        except subprocess.CalledProcessError as e:
            try:
                output = e.output.decode("utf-8") 
                error = [line for line in output.split('\n') if 'error' in line][0]
                source, line = error.split(':')[:2]
                print(source, line)
                edit_line(source, int(line), get_code(error))
                keep_compiling = True #keep going
            except Exception as E:
                print(E)
                print(output)
                keep_compiling = False
            
