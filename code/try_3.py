#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-11-20 12:58:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


from danc_python import Diagram


def run():
    diagram = Diagram()
    d = diagram.init_draw("mermaid.state")

    d.l(None, "ListTable")
    d.l("ListTable", "InitObj", "NewObj")
    d.l("ListTable", "LoadObj", "EditObj")
    d.l("InitObj", "ShowModal")
    d.l("LoadObj", "ShowModal")
    d.l("LoadObj", "EditModal")
    d.l("EditModal", "StoreDetail", "Accept")
    if_state = d.iif()
    d.l("StoreDetail", if_state)
    d.l(if_state, "CloseModal", "success")
    d.l(if_state, "ShowErrors", "error")
    d.l("ShowErrors", "EditModal")
    d.l("EditModal", "CloseModal", "Cancel")
    d.l("EditModal", "CloseModal", "Error")
    d.l("CloseModal", "RefreshList")
    d.l("RefreshList", "ListTable")
    d.l("ListTable", None)

    diagram.open_in_browser(d)

if __name__=="__main__":
    run()


