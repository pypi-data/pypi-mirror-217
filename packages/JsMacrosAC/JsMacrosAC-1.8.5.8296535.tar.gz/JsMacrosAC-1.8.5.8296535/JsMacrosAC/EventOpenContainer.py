from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ICancelable import ICancelable
from .Inventory import Inventory
from .IScreen import IScreen

net_minecraft_client_gui_screen_ingame_HandledScreen__ = TypeVar("net_minecraft_client_gui_screen_ingame_HandledScreen__")
HandledScreen = net_minecraft_client_gui_screen_ingame_HandledScreen__


class EventOpenContainer(BaseEvent, ICancelable):
	"""
	Since: 1.6.5 
	"""
	inventory: Inventory
	screen: IScreen
	cancelled: bool

	@overload
	def __init__(self, screen: HandledScreen) -> None:
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


