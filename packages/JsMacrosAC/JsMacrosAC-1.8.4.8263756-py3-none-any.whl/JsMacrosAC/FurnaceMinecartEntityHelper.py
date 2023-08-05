from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

FurnaceMinecartEntity = TypeVar["net.minecraft.entity.vehicle.FurnaceMinecartEntity"]

class FurnaceMinecartEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FurnaceMinecartEntity) -> None:
		pass

	@overload
	def isPowered(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'' true if the furnace minecart is powered, 'false' otherwise. 
		"""
		pass

	pass


