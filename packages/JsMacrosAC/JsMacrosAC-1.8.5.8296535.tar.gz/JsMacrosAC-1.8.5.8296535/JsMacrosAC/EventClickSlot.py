from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ICancelable import ICancelable
from .Inventory import Inventory

net_minecraft_client_gui_screen_ingame_HandledScreen__ = TypeVar("net_minecraft_client_gui_screen_ingame_HandledScreen__")
HandledScreen = net_minecraft_client_gui_screen_ingame_HandledScreen__


class EventClickSlot(BaseEvent, ICancelable):
	"""event triggered when the user "clicks" a slot in an inventory\n
	Since: 1.6.4 
	"""
	mode: int
	button: int
	slot: int
	cancel: bool

	@overload
	def __init__(self, screen: HandledScreen, mode: int, button: int, slot: int) -> None:
		pass

	@overload
	def getInventory(self) -> Inventory:
		"""

		Returns:
			inventory associated with the event 
		"""
		pass

	@overload
	def cancel(self) -> None:
		pass

	@overload
	def isCanceled(self) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


