#!/usr/bin/env python2.7
#naive implementation of a program that sorts function definitions alphabetically

import sys
import fileinput

DEBUG = False
function = ''
first_fun = None
output = []
funs = {}
bracket_count = 0

for line in fileinput.input():

    bracket_count += line.count("{")
    if bracket_count:
        # we are in a function
        if not function:
            function = line.split("(")[0].split()[-1]
    else:
        function = None
    if function:
        if first_fun == None:
            first_fun = len(output)
        if function not in funs:
            funs[function] = []
        funs[function].append(line)
    else:
        # sys.stdout.write(line)
        output.append(line)
    bracket_count -= line.count("}")

if DEBUG:
    print(funs)

output_funs = []
for k in sorted(funs.keys()):
    for l in funs[k]:
        output_funs.append(l)

if first_fun != None:
    output = output[:first_fun] + output_funs + output[first_fun:]

for l in output:
    sys.stdout.write(l)
