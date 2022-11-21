"""
	Диаграмма в модуле
"""

DIAGRAM_TYPE = "mermaid.state"
TITLE = "Mermaid пример 1"
DESCRIPTION = "Для демонстрации концепции с использованием Mermaid"
TAGS=["mermaid", "example", "py"]
DETAIL="""
А тут большое и толстое описание всего
"""

def draw(d):
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
