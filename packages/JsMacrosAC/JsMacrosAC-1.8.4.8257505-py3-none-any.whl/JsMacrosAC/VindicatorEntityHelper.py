from typing import overload
from typing import TypeVar
from .IllagerEntityHelper import IllagerEntityHelper

VindicatorEntity = TypeVar["net.minecraft.entity.mob.VindicatorEntity"]

class VindicatorEntityHelper(IllagerEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: VindicatorEntity) -> None:
		pass

	@overload
	def isJohnny(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this vindicator is johnny, 'false' otherwise. 
		"""
		pass

	pass


