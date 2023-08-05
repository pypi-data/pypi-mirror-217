from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

BlazeEntity = TypeVar["net.minecraft.entity.mob.BlazeEntity"]

class BlazeEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: BlazeEntity) -> None:
		pass

	@overload
	def isOnFire(self) -> bool:
		"""A blaze can only shoot fireballs when it's on fire.\n
		Since: 1.8.4 

		Returns:
			'true' if the blaze is on fire, 'false' otherwise. 
		"""
		pass

	pass


