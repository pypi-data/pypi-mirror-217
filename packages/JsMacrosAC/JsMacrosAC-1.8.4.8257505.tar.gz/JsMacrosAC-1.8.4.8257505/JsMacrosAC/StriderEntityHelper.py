from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

StriderEntity = TypeVar["net.minecraft.entity.passive.StriderEntity"]

class StriderEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: StriderEntity) -> None:
		pass

	@overload
	def isSaddled(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this strider is saddled, 'false' otherwise. 
		"""
		pass

	@overload
	def isShivering(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this strider is shivering in the cold, 'false' otherwise. 
		"""
		pass

	pass


