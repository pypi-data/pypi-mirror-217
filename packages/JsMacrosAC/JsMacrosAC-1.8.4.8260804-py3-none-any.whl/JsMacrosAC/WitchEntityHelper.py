from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper
from .ItemStackHelper import ItemStackHelper

WitchEntity = TypeVar["net.minecraft.entity.mob.WitchEntity"]

class WitchEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: WitchEntity) -> None:
		pass

	@overload
	def isDrinkingPotion(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this witch is drinking a potion, 'false' otherwise. 
		"""
		pass

	@overload
	def getPotion(self) -> ItemStackHelper:
		"""
		Since: 1.8.4 

		Returns:
			the held potion item. 
		"""
		pass

	pass


