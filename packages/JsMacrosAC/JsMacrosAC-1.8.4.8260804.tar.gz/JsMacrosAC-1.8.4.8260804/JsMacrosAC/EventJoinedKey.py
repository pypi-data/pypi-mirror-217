from typing import overload
from .ICancelable import ICancelable
from .EventKey import EventKey


class EventJoinedKey(ICancelable, EventKey):
	cancel: bool

	@overload
	def __init__(self, action: int, key: str, mods: str) -> None:
		pass

	@overload
	def cancel(self) -> None:
		pass

	@overload
	def isCanceled(self) -> bool:
		pass

	pass


