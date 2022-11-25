# 
DIAGRAM_TYPE = "graphviz"
#TITLE = "Mermaid state пример 1"
DESCRIPTION = "Проба GraphViz"
CODE = """
digraph {
  compound=true
  graph [fontname="Arial", rankdir=TB, ranksep=1.0, nodesep=1.0]
  node [fontname="Arial", shape=box, margin="0.4,0.3"]
  edge [fontname="Arial"]
  label=<<br /><font point-size="34">Software System - System Context</font>>

  1 [id=1,shape=rect, label=<<font point-size="34">User</font><br /><font point-size="19">[Person]</font><br /><br /><font point-size="24">A user of my software<br />system.</font>>, style=filled, color="#052e56", fillcolor="#08427b", fontcolor="#ffffff"]
  2 [id=2,shape=rect, label=<<font point-size="34">Software System</font><br /><font point-size="19">[Software System]</font><br /><br /><font point-size="24">My software system.</font>>, style=filled, color="#0b4884", fillcolor="#1168bd", fontcolor="#ffffff"]

  1 -> 2 [id=3, label=<<font point-size="24">Uses</font>>, style="dashed", color="#707070", fontcolor="#707070"]
}
"""