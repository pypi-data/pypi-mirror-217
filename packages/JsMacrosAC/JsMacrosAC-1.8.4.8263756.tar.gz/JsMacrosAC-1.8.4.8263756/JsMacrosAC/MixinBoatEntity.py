from typing import overload
from typing import TypeVar

BoatEntity_Location = TypeVar["net.minecraft.entity.vehicle.BoatEntity.Location"]

class MixinBoatEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getLocation(self) -> BoatEntity_Location:
		pass

	pass


