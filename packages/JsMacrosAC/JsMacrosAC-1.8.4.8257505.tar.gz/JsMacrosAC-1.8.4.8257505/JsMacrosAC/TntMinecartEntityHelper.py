from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

TntMinecartEntity = TypeVar["net.minecraft.entity.vehicle.TntMinecartEntity"]

class TntMinecartEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: TntMinecartEntity) -> None:
		pass

	@overload
	def getRemainingTime(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the remaining time in ticks before the tnt explodes, or '-1' if the tnt is not
primed. 
		"""
		pass

	@overload
	def isPrimed(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the tnt is primed, 'false' otherwise. 
		"""
		pass

	pass


