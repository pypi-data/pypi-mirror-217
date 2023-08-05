from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

MooshroomEntity = TypeVar["net.minecraft.entity.passive.MooshroomEntity"]

class MooshroomEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: MooshroomEntity) -> None:
		pass

	@overload
	def isShearable(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this mooshroom can be sheared, 'false' otherwise. 
		"""
		pass

	@overload
	def isRed(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this mooshroom is a red mooshroom, 'false' otherwise. 
		"""
		pass

	@overload
	def isBrown(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this mooshroom is a brown mooshroom, 'false' otherwise. 
		"""
		pass

	pass


