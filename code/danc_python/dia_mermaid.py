"""
	mermaid diagrams
"""

from .bases import DrawBase, DrawItem


class MermaidStateDiagram(DrawBase):
	"""
	"""

	def __init__(self, type_name, diagram, *args, **kwargs):
		super().__init__("mermaid", diagram)
		self.start()
		#self._add("stateDiagram-v2")
		#self._inc_level()


@DrawBase.register_item("connect", "l")
class ItmConnect(DrawItem):
	def __init__(self, itm_from, itm_to, text=None):
		super().__init__()
		line = "-->"
		if not itm_from:
			itm_from = "[*]"
		if not itm_to:
			itm_to = "[*]"
		if isinstance(itm_from, DrawItem):
			itm_from = itm_from.state_id
		if isinstance(itm_to, DrawItem):
			itm_to = itm_to.state_id
		if text:
			cmd = f"{itm_from} {line} {itm_to} : {text}"
		else:
			cmd = f"{itm_from} {line} {itm_to}"
		self.base._add(cmd)


@DrawBase.register_item("state")
class ItmState(DrawItem):
	prefix = "st"
	def __init__(self, text, sid=None):
		super().__init__(sid)
		self.base._add(f"{self.state_id} : {text}")


@DrawBase.register_item("iif")
class ItmChoice(DrawItem):
	prefix = "ch"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add(f"state {self.state_id} <<choice>>")


@DrawBase.register_item("fork")
class ItmFork(DrawItem):
	prefix = "fork"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add(f"state {self.state_id} <<fork>>")


@DrawBase.register_item("join")
class ItmJoin(DrawItem):
	prefix = "join"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add(f"state {self.state_id} <<join>>")


@DrawBase.register_item("group", "grp")
class ItmGroup(DrawItem):
	prefix = "grp"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.started=None

	def start(self):
		if self.started:
			return
		self.base._add(f"state {self.state_id} {{")
		self.base._inc_level()
		self.started=True

	def end(self):
		if not self.started:
			return
		self.base._dec_level()
		self.base._add("}")
		self.started=False

	def __enter__(self):
		self.start()

	def __exit__(self, exc_type, exc_value, traceback):
		self.end()


@DrawBase.register_item("thr")
class ItmTread(DrawItem):
	prefix = "thr"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add("--")


@DrawBase.register_item("start")
class ItmStart(DrawItem):
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add("stateDiagram-v2")
		self.base._inc_level()

