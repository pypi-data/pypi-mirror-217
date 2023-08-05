from typing import overload
from typing import TypeVar

ItemStack = TypeVar["net.minecraft.item.ItemStack"]
PropertyDelegate = TypeVar["net.minecraft.screen.PropertyDelegate"]

class MixinAbstractFurnaceScreenHandler:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeIsSmeltable(self, itemStack: ItemStack) -> bool:
		pass

	@overload
	def invokeIsFuel(self, itemStack: ItemStack) -> bool:
		pass

	@overload
	def getPropertyDelegate(self) -> PropertyDelegate:
		pass

	pass


