#!/usr/bin/env python2.7
#naive implementation of a program that forces the rule of 30
#on function length

from pycparser import c_parser
import pycparser
import sys
import fileinput

LIMIT = 30
DEBUG = True

lineCount = 0
variables = []
function = None
junk = 100000

def parse_types(_type, decl_type, decl_name, param_list=False):
    while(True):
        if DEBUG:
            print _type
        if isinstance(_type, pycparser.c_ast.TypeDecl):
            decl_type = ' '.join(_type.type.names) + decl_type
            decl_name = _type.declname 
            variables.append((decl_type, decl_name))
            break; #as far down in the ast you can go for decls
        elif isinstance(_type, pycparser.c_ast.ArrayDecl):
            decl_type += '*'
        elif isinstance(_type, pycparser.c_ast.PtrDecl):
            decl_type += '*'        
        else:
            raise Exception('Unknown type: ' + _type)
            break;
        _type = _type.children()[0][1]

parser = c_parser.CParser()
for line in fileinput.input():
    sys.stdout.write(line)
    if function:
        lineCount += 1
    try:
        # very brittle, need to fix
        if line[-2] == "{":
            line = line.replace("{", ";")
        if not line[-2] == ";":
            line = line + ';'

        ast = parser.parse(line).children()[0][1].children()[0][1]
        if DEBUG:
            ast.show(showcoord=True)

        if isinstance(ast, pycparser.c_ast.FuncDecl):
            function = ast.children()[1][1].declname
            if DEBUG:
                print function
            func_type = ' '.join(ast.children()[1][1].type.names)

            lineCount = 0
            for x in ast.children()[0][1].children():
                decl_type = ''
                decl_name = ''
                parse_types(x[1].children()[0][1], decl_type, decl_name, param_list=True)

            if DEBUG:
                print variables

        elif isinstance(ast, pycparser.c_ast.PtrDecl) or \
            isinstance(ast, pycparser.c_ast.ArrayDecl) or \
            isinstance(ast, pycparser.c_ast.TypeDecl):

            decl_type = ''
            decl_name = ''
            parse_types(ast, decl_type, decl_name, param_list=True)

            if DEBUG:
                print variables

    except Exception as e:
        if DEBUG:
            print e
        pass

    if lineCount > LIMIT:
        junk += 1
        lineCount = 0
        f = "{}{}".format(function, junk)
        #make new function
        print("    return {}({});\n}}\n{} {}({}) {{".format(
            f,
            ", ".join([x[1] for x in variables]),
            func_type,
            f,
            ", ".join([" ".join(x) for x in variables])
            ))
