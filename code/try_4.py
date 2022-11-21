#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-11-20 12:58:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


from danc_python import Diagram

DIAGRAMM = """
stateDiagram-v2
    [*] --> ListTable
    ListTable --> InitObj : NewObj
    ListTable --> LoadObj : EditObj
    InitObj --> ShowModal
    LoadObj --> ShowModal
    ShowModal --> EditModal
    EditModal --> StoreDetail : Accept
    state if_state <<choice>>
    StoreDetail --> if_state
    if_state --> CloseModal: success
    if_state --> ShowErrors: error
    ShowErrors --> EditModal
    EditModal --> CloseModal : Cancel
    EditModal --> CloseModal : Error
    CloseModal --> RefreshList
    RefreshList --> ListTable
    ListTable --> [*]
"""

SAMPLE="""
digraph G {Hello->World}
"""

import marm_example


def run_module(module):
    diagram = Diagram()
    d = diagram.init_draw(module.DIAGRAM_TYPE)
    module.draw(d)
    diagram.open_in_browser(d)

if __name__=="__main__":
    run_module(marm_example)


