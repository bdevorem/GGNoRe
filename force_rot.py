#!/usr/bin/env python2.7
#naive implementation of a program that forces the rule of 30
#on function length

from pycparser import c_parser
import pycparser
import sys
import fileinput

LIMIT = 30
DEBUG = False

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
        if DEBUG:
            ast.show(showcoord=True)

        if isinstance(ast, pycparser.c_ast.FuncDecl):
            function = ast.children()[1][1].declname
            if DEBUG:
                print function

            lineCount = 0
            for x in ast.children()[0][1].children():
                node = x[1]
                decl_type = ''
                decl_name = ''

                while(True):
                    _type = node.children()[0][1]
                    if DEBUG:
                        print _type

                    if isinstance(_type, pycparser.c_ast.TypeDecl):
                        decl_type = ' '.join(node.children()[0][1].type.names) + decl_type
                        decl_name = node.children()[0][1].declname 
                        variables.append((decl_type, decl_name))
                        break; #as far down in the ast you can go for decls
                    elif isinstance(_type, pycparser.c_ast.ArrayDecl):
                        decl_type += '*'
                        node = node.children()[0][1]
                    elif isinstance(_type, pycparser.c_ast.PtrDecl):
                        decl_type += '*'        
                        node = node.children()[0][1]
                    else:
                        raise Exception('Unknown type: ' + _type)
                        break;

            #variables = [(' '.join(x[1].children()[0][1].type.names),
            #             x[1].children()[0][1].declname)
            #             for x in ast.children()[0][1].children()]
            if DEBUG:
                print variables

        elif isinstance(ast, pycparser.c_ast.TypeDecl):
            variables.append((' '.join(ast.type.names), ast.declname))
    except Exception as e:
        print e
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
