"""
	Диаграмма в модуле
"""

DIAGRAM_TYPE = "mermaid.state"
TITLE = "Mermaid state пример 1"
DESCRIPTION = "Для демонстрации концепции с использованием Mermaid"
TAGS=["mermaid", "example", "py"]
DETAIL="""
А тут большое и толстое описание всего
"""


def draw(d):
    d.l(None, "A")
    s_fork = d.fork()
    d.l("A",s_fork)
    d.l(s_fork, "B")
    d.l(s_fork, "C")
    s_join = d.join()
    d.l("B",s_join)
    d.l("C",s_join)
    d.l(s_join, "D1")
    d.l("D1", None)
