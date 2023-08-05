from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ICancelable import ICancelable
from .Inventory import Inventory

HandledScreen = TypeVar["net.minecraft.client.gui.screen.ingame.HandledScreen__"]

class EventDropSlot(BaseEvent, ICancelable):
	"""event triggered when an item is dropped\n
	Since: 1.6.4 
	"""
	slot: int
	all: bool
	cancel: bool

	@overload
	def __init__(self, screen: HandledScreen, slot: int, all: bool) -> None:
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


