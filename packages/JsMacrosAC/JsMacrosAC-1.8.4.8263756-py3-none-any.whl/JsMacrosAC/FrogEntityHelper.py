from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper
from .EntityHelper import EntityHelper

FrogEntity = TypeVar["net.minecraft.entity.passive.FrogEntity"]

class FrogEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FrogEntity) -> None:
		pass

	@overload
	def getVariant(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this frog. 
		"""
		pass

	@overload
	def getTarget(self) -> EntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			the target of this frog, or 'null' if it has none. 
		"""
		pass

	@overload
	def isCroaking(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this frog is croaking, 'false' otherwise. 
		"""
		pass

	pass


