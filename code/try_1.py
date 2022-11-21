#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-11-20 12:23:46
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
	Генерирует диаграму используя синтаксис mermaid и сервер kroki.io
"""

import os
import webbrowser
import sys
import base64
import zlib

DIAGRAMM_URL="""
https://mermaid.live/edit#pako:eNqFkt9vgjAQx_8Vco8LGER-zMaYLOrDEt2SuaeNZalwDBagpi1zzvi_r6WKPJjIC737fr53vfQOkLAUgYCQVOK8oF-cVs6PF9eW-t7vPizHmVrLQshXuinRpLuwFR_rQj5vvi1iPeFOHa4xS0ZTwyzSljbQ2aqRdc52K5bS8uQ_Oa5IXdiKumBP7ELjlIzjHCUtStX7IUlwKw3XzmsV2ac5TCZJzooEp9NTj55RFzqDRu1sWpqVTGDbkliiUS2EuELpSy84Z1wQC_X_MotJ3x7m0kjNMqN1grexxaVVL6-xF8w4ily_k9F7iduPrjYjruMabKiQV7RI1QodNBiDzLHCGIg6ppjRppQxxPVRobSRbL2vEyCSN2hDs00vSwcko6VQWVTTML4ya9lupw1bWr8xVp2NKgRygF8goT_wPTcKAn9874ZeFNqwB-L4YTQIgpHreWHgBd7o_mjDX1tgOIiiYRAOvdAfj4dR6I6O_w6c8Yc
"""


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

#https://kroki.io/graphviz/svg/eNpLyUwvSizIUHBXqPZIzcnJ17ULzy_KSanlAgB1EAjQ
KROKI = "https://kroki.io/mermaid/svg/"

def code(txt):
	#import sys; import base64; import zlib; print(base64.urlsafe_b64encode(zlib.compress(sys.stdin.read().encode('utf-8'), 9)).decode('ascii'))
	res = base64.urlsafe_b64encode(zlib.compress(txt.encode('utf-8'), 9)).decode('ascii')
	return res

def run():
	c = code(DIAGRAMM)
	print(c)
	webbrowser.open(KROKI+c)


if __name__=="__main__":
	run()

