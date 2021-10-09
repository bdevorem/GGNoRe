#!/usr/bin/env python2.7
#naive implementation of a program that forces the rule of 30
#on function length

from pycparser import c_parser
import pycparser
import sys
import fileinput

LIMIT = 30
DEBUG = True
function = ''
func_type = ''
lineCount = 0
variables = []
junk = 100000

def parse_types(_type, func=False):
    decl_type = ''
    decl_name = ''
    while(True):
        if DEBUG:
            print(_type)
        if isinstance(_type, pycparser.c_ast.TypeDecl):
            decl_type = ' '.join(_type.type.names) + decl_type
            decl_name = _type.declname 
            if func:
                global function, func_type
                function = decl_name
                func_type = decl_type
            else:
                if (decl_type, decl_name) not in variables:
                    variables.append((decl_type, decl_name))
                elif decl_type in dict(variables):
                    variables.remove((decl_type, dict(variables)[decl_type]))
                    variables.append((decl_type, decl_name))

            break #as far down in the ast you can go for decls
        elif isinstance(_type, pycparser.c_ast.ArrayDecl):
            decl_type += '*'
        elif isinstance(_type, pycparser.c_ast.PtrDecl):
            decl_type += '*'        
        else:
            raise Exception('Unknown type: ' + _type)
            break
        _type = _type.children()[0][1]

parser = c_parser.CParser()
first_fun = None
output = []
funs = {}
for line in fileinput.input():
    if function:
        if first_fun:
            first_fun = len(output)
        lineCount += 1
        if function in funs:
            funs[function] = []
        funs[function].append(line)
    else:
        # sys.stdout.write(line)
        output.append(line)

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
            if len(ast.children()) < 2:
                func_node = ""
            else:
                func_node = ast.children()[1][1]
                parse_types(func_node, func=True)

            if DEBUG:
                print("~~~found function~~~")
                print(function)
                print(func_type)

            lineCount = 0
            for x in ast.children()[0][1].children():
                parse_types(x[1].children()[0][1], func=False)

            if DEBUG:
                print(variables)

        elif isinstance(ast, pycparser.c_ast.PtrDecl) or \
            isinstance(ast, pycparser.c_ast.ArrayDecl) or \
            isinstance(ast, pycparser.c_ast.TypeDecl):
            parse_types(ast, func=False)

            if DEBUG:
                print(variables)

    except Exception as e:
        if DEBUG:
            print(e)
            raise 
        pass

    if lineCount > LIMIT:
        junk += 1
        lineCount = 0
        f = "{}{}".format(function, junk)
        #make new function
        if func_type == 'void':
            ret = ''
        else:
            ret = 'return '
        print("    {}{}({});\n}}\n{} {}({}) {{".format(
            ret,
            f,
            ", ".join([x[1] for x in variables]),
            func_type,
            f,
            ", ".join([" ".join(x) for x in variables])
            ))
            
if DEBUG:
    print(funs)
