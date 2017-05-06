#!/usr/bin/env python2.7
#naive implementation of a program that forces the rule of 30
#on function length
from pycparser import c_parser
import pycparser
import sys
import fileinput

LIMIT = 30

lineCount = 0
variables = []
function = None
junk = 100000

parser = c_parser.CParser()
for line in fileinput.input():
    sys.stdout.write(line)
    if function:
        lineCount += 1
    try:
        line = line.replace("{", ";")
        ast = parser.parse(line).children()[0][1].children()[0][1]

        if isinstance(ast, pycparser.c_ast.FuncDecl):
            function = ast.children()[1][1].declname
            lineCount = 0
            variables = [(' '.join(x[1].children()[0][1].type.names),
                         x[1].children()[0][1].declname)
                         for x in ast.children()[0][1].children()]
        elif isinstance(ast, pycparser.c_ast.TypeDecl):
            variables.append((' '.join(ast.type.names), ast.declname))
    except Exception as e:
        pass

    if lineCount > LIMIT:
        junk += 1
        lineCount = 0
        f = "{}{}".format(function, junk)
        #make new function
        print("    return {}({});\n}}\nint {}({}) {{".format(
            f,
            ", ".join([x[1] for x in variables]),
            f,
            ", ".join([" ".join(x) for x in variables])
            ))
