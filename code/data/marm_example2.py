"""
    Диаграмма в модуле
"""

DIAGRAM_TYPE = "mermaid.state"

def grp_2(d, sid=None):
    g = d.grp(sid=sid)
    g.start()
    for i in range(1,4):
        d.l(None, f"a{i}")
        d.l(f"a{i}", f"b{i}")
        d.l(f"b{i}", f"c{i}")
        d.l(f"c{i}", None)
        if i<3:
            d.thr()
    g.end()
    return g

def draw(d):
    d.l(None, "a")
    s_fork = d.fork()
    d.l("a",s_fork)
    d.l(s_fork, "b")
    d.l(s_fork, "c")
    s_join = d.join()
    d.l("b",s_join)
    d.l("c",s_join)
    d.l(s_join, "d")
    d.l("d", "A1")
    with d.grp(sid="A1"):
        d.l(None, "e")
        d.l("e", "F")
        grp_2(d, sid="F")
        d.l("F", None)
    d.l("A1", None)
