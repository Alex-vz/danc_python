"""
	mermaid diagrams
"""

from .bases import DrawBase, DrawItem


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


class ItmState(DrawItem):
	prefix = "st"
	def __init__(self, text, sid=None):
		super().__init__(sid)
		self.base._add(f"{self.state_id} : {text}")


class ItmChoice(DrawItem):
	prefix = "ch"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add(f"state {self.state_id} <<choice>>")


class ItmFork(DrawItem):
	prefix = "fork"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add(f"state {self.state_id} <<fork>>")


class ItmJoin(DrawItem):
	prefix = "join"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add(f"state {self.state_id} <<join>>")


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

class ItmTread(DrawItem):
	prefix = "thr"
	def __init__(self, sid=None):
		super().__init__(sid)
		self.base._add("--")


class MermaidStateDiagram(DrawBase):
	"""
	"""

	@property
	def l(self):
		return self._prep_item(ItmConnect)

	@property
	def state(self):
		return self._prep_item(ItmState)

	@property
	def iif(self):
		return self._prep_item(ItmChoice)

	@property
	def fork(self):
		return self._prep_item(ItmFork)

	@property
	def join(self):
		return self._prep_item(ItmJoin)

	@property
	def grp(self):
		return self._prep_item(ItmGroup)

	@property
	def thr(self):
		return self._prep_item(ItmTread)

	def __init__(self, *args, **kwargs):
		super().__init__("mermaid")
		self._add("stateDiagram-v2")
		self._inc_level()
