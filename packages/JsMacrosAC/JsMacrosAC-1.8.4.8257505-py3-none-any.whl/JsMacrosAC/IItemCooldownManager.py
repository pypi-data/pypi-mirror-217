from typing import overload
from typing import TypeVar
from typing import Mapping
from .IItemCooldownEntry import IItemCooldownEntry

Item = TypeVar["net.minecraft.item.Item"]

class IItemCooldownManager:

	@overload
	def jsmacros_getCooldownItems(self) -> Mapping[Item, IItemCooldownEntry]:
		pass

	@overload
	def jsmacros_getManagerTicks(self) -> int:
		pass

	pass


