#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-11-20 12:58:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import io

from danc_python import Diagram


#import marm_example


def run_module_0(module):
    diagram = Diagram()
    d = diagram.init_draw(module.DIAGRAM_TYPE)
    module.draw(d)
    diagram.open_in_browser(d)

def run_module(module_name):
    with open(module_name, 'r', encoding="utf-8") as fm:
        #print("".join([l for l in fm]))
        #return
        mc = compile("".join([l for l in fm]), module_name, "exec")
        module = {}
        exec(mc, module)
    diagram = Diagram()
    d = diagram.init_draw(module["DIAGRAM_TYPE"])
    module["draw"](d)
    diagram.open_in_browser(d)

if __name__=="__main__":
    #run_module("/home/alex/zwork1/diagrams/code/marm_example.py")
    run_module("./marm_example.py")


