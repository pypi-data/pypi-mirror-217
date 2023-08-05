from typing import overload
from typing import TypeVar
from .Inventory import Inventory
from .ItemStackHelper import ItemStackHelper

CartographyTableScreen = TypeVar["net.minecraft.client.gui.screen.ingame.CartographyTableScreen"]

class CartographyInventory(Inventory):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, inventory: CartographyTableScreen) -> None:
		pass

	@overload
	def getMapItem(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the map item. 
		"""
		pass

	@overload
	def getMaterial(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the paper item. 
		"""
		pass

	@overload
	def getOutput(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the output item. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


