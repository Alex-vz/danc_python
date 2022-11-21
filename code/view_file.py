#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-11-20 12:58:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
 
python view_file.py umlet ./data/NativeLangDiagramStruct.uxf

python view_file.py -u umlet ./data/NativeLangDiagramStruct.uxf

python view_file.py -o my.svg umlet ./data/NativeLangDiagramStruct.uxf

python view_file.py -o my.svg umlet ./data/Pattern_Edit_Modal_Concept.uxf

python view_file.py umlet ./data/Pattern_Edit_Modal_Concept.uxf

python view_file.py py ./data/marm_example2.py

python view_file.py py ./data/subdir/marm_example.py

python view_file.py py ./data/subdir/aws_example.py

python view_file.py structurizr ./data/structuriz.dsl

python view_file.py structurizr ./data/subdir/aws.dsl

"""

import argparse

from danc_python import Diagram


def run_module(args):
    buf = args.dia_file.read()
    mc = compile(buf, "<string>", "exec")
    module = {}
    exec(mc, module)
    draw_func = module.get("draw")
    code_block = module.get("CODE")
    if not (draw_func or code_block):
        raise Exception("No diagram code!")

    diagram = Diagram()
    d = diagram.init_draw(module["DIAGRAM_TYPE"])
    if draw_func:
        draw_func(d)
    else:
        d.code(code_block)
    return (diagram, d)

def run(args):
    if args.dia_type=="py":
        diagram, d = run_module(args)
    else:
        diagram, d = run_file(args)

    if args.out_file:
        diagram.render_to_file(d, args.out_file)
        print("File {} created.".format(args.out_file))
    elif args.url_only=='1':
        print(diagram.perp_url(d))
    else:
        diagram.open_in_browser(d)

def run_file(args):
    buf = args.dia_file.read()

    diagram = Diagram()
    d = diagram.init_draw(args.dia_type)

    d.code(buf)
    return (diagram, d)



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process diagram and open in browser.')
    parser.add_argument('-o', type=str, dest="out_file", 
                        help='Name of file to load in')  
    parser.add_argument('-u', action='store_const', const='1', default='0', dest="url_only", 
                        help='Output URL only, do not start browser.')  
    parser.add_argument('dia_type', type=str,  
                        help='Name of diagram type')  
    parser.add_argument('dia_file', metavar="file", type=argparse.FileType('r', encoding="utf-8"),
                        help='filename')  
    run(parser.parse_args())


