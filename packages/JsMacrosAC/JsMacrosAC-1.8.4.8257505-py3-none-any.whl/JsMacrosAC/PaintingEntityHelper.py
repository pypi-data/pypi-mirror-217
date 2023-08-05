from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

PaintingEntity = TypeVar["net.minecraft.entity.decoration.painting.PaintingEntity"]

class PaintingEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PaintingEntity) -> None:
		pass

	@overload
	def getWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of this painting. 
		"""
		pass

	@overload
	def getHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of this painting. 
		"""
		pass

	@overload
	def getIdentifier(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the identifier of this painting's art. 
		"""
		pass

	pass


