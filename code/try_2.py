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

UMLET="""
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<diagram program="umlet" version="14.2">
  <zoom_level>10</zoom_level>
  <element>
    <type>com.baselet.element.old.allinone.ActivityDiagramText</type>
    <coordinates>
      <x>190</x>
      <y>0</y>
      <w>548</w>
      <h>1187</h>
    </coordinates>
    <panel_attributes>title:Редактирование списка модальной формой.
Start
Отобразить форму-список
If
	[редактировать строку]
	открыть форму
	загрузить данные
	
	[создать новый]
	открыть форму
	отобразить стартовые\данные
EndIf
Отобразить модальную\форму
просмотр/\редактирование\данных~runForm
Сохранить/\отменить&gt;
&gt;сохранить
выполнить сохранение
If
	[Успешно]
	закрыть модаль

	[Ошибки]
	Отобразить ошибки
	-&gt;runForm
EndIf
обновить список
-&gt;End

&gt;отменить
Закрыть модаль
Обновить список
|

End</panel_attributes>
    <additional_attributes/>
  </element>
</diagram>
"""

def run():
	diagram = Diagram()
	d = diagram.init_draw("mermaid")

	d.code(DIAGRAMM)

	diagram.open_in_browser(d)

	s = diagram.init_draw("graphviz")

	s.code(SAMPLE)

	diagram.open_in_browser(s)

	u = diagram.init_draw("umlet")

	u.code(UMLET)

	diagram.open_in_browser(u)

if __name__=="__main__":
	run()


