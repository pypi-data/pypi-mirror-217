from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

BeeEntity = TypeVar["net.minecraft.entity.passive.BeeEntity"]

class BeeEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: BeeEntity) -> None:
		pass

	@overload
	def hasNectar(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the bee has nectar, 'false' otherwise. 
		"""
		pass

	@overload
	def isAngry(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the bee is angry at a player, 'false' otherwise. 
		"""
		pass

	@overload
	def hasStung(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the bee has already stung a player, 'false' otherwise. 
		"""
		pass

	pass


