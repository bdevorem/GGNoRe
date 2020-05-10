#!/usr/bin/env python3

from __future__ import print_function
import sys

from pycparser import c_parser, c_ast, parse_file

class FuncDefVisitor(c_ast.NodeVisitor):
    def visit_FuncDef(self, node):
        print(node.decl.name)


def show_func_defs(filename):
    ast = parse_file(filename, use_cpp=True, cpp_args='-Iutils/fake_libc_include')

    v = FuncDefVisitor()
    v.visit(ast)


show_func_defs(sys.argv[1])
