from typing import overload
from typing import TypeVar

Slot = TypeVar["net.minecraft.screen.slot.Slot"]

class IInventory:

	@overload
	def getX(self) -> int:
		pass

	@overload
	def getY(self) -> int:
		pass

	@overload
	def jsmacros_getSlotUnder(self, x: float, y: float) -> Slot:
		pass

	pass


