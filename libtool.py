#!/usr/bin/python3
# _*_ coding=utf-8 _*_

from ctypes import *
import argparse
import code
import signal
import sys
import subprocess
#import ccsyspath

import struct;print(struct.calcsize("P") * 8)
library = cdll.LoadLibrary("C:\\Program Files\\LLVM\\bin\\libclang.dll")

#shell_result = subprocess.run(["llvm-config", "--src-root"], capture_output=True)
#sys.path.insert(0, shell_result.stdout.decode("utf-8")[:-1] + "/bindings/python")
#sys.path.insert(0, shell_result.stdout.decode("utf-8")[:-1] + "/tools/clang/bindings/python")
sys.path.insert(0, "C:\\Program Files\\LLVM\\llvm-8.0.1.src\\bindings\\python")
sys.path.insert(0, "C:\\Program Files\\LLVM\\llvm-8.0.1.src\\tools\\clang\\bindings\\python")
#sys.path.insert(0, "/cygdrive/c/Program Files/LLVM/llvm-8.0.1.src/bindings/python")
#sys.path.insert(0, "")
import llvm
import clang.cindex
from clang.cindex import Config
#Config.set_library_path("C:\\Program Files\\LLVM\\bin")
Config.set_library_file("C:\\Program Files\\LLVM\\bin\\libclang.dll")

def SigHandler_SIGINT(signum, frame):
    print()
    sys.exit(0)

class Argparser(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", type=str, help="string")
        parser.add_argument("--symbol", type=str, help="string")
        parser.add_argument("--bool", action="store_true", help="bool", default=False)
        parser.add_argument("--dbg", action="store_true", help="debug", default=False)
        self.args = parser.parse_args()

def find_typerefs(node, typename):
    if node.kind.is_reference():
        #print(node.spelling)
        if node.spelling == typename:
            print("Found %s [Line=%s, Col=%s]"%(typename, node.location.line, node.location.column))
    for c in node.get_children():
        find_typerefs(c, typename)

def find_structs(node):
    #if node.kind.is_declaration():
    if node.kind.is_declaration():
        if node.kind == node.kind.STRUCT_DECL and node.is_definition:
            print(node.spelling)
            for c in node.get_children():
                #if array
                try:
                    print(c.type.element_count)
                    print(c.type.element_type.spelling)
                #if not array
                except:
                    #print(c.spelling)
                    #print("printf(" + node.type.spelling + "->" + c.type.spelling + " " + c.spelling + ");")
                    if node.type.kind == node.type.kind.INT:
                        print("ffffffffffffcuk")
                    if node.lexical_parent.kind.is_declaration():
                        print(node.lexical_parent.spelling)
                    print("printf(" + repr(node.type.get_named_type()) + "->" + c.type.spelling + " " + c.spelling + ");")
                    #print(c.location)
    for c in node.get_children():
        find_structs(c)


# write code here
def premain(argparser):
    signal.signal(signal.SIGINT, SigHandler_SIGINT)
    #here
    args = "-x c --std=c99".split()
    #syspath = ccsyspath.system_include_paths("gcc")
    #inc_args = [b'-I ' + inc for inc in syspath]
    #args = args + inc_args
    index = clang.cindex.Index.create()
    #tu = index.parse(argparser.args.file, args=args)
    tu = index.parse(argparser.args.file)
    print("TU:", tu.spelling)
    find_structs(tu.cursor)

def main():
    argparser = Argparser()
    if argparser.args.dbg:
        try:
            premain(argparser)
        except Exception as e:
            if hasattr(e, "__doc__"):
                print(e.__doc__)
            if hasattr(e, "message"):
                print(e.message)
    else:
        premain(argparser)

if __name__ == "__main__":
    main()
