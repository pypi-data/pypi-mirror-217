from typing import overload
from typing import TypeVar
from .FishEntityHelper import FishEntityHelper

TropicalFishEntity = TypeVar["net.minecraft.entity.passive.TropicalFishEntity"]

class TropicalFishEntityHelper(FishEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: TropicalFishEntity) -> None:
		pass

	@overload
	def getVariant(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the variant of this tropical fish. 
		"""
		pass

	@overload
	def getSize(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the size of this tropical fish's variant. 
		"""
		pass

	@overload
	def getBaseColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the base color of this tropical fish's pattern. 
		"""
		pass

	@overload
	def getPatternColor(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the pattern color of this tropical fish's pattern. 
		"""
		pass

	@overload
	def getVarietyId(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the id of this tropical fish's variant. 
		"""
		pass

	pass


