from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper
from .DirectionHelper import DirectionHelper
from .DyeColorHelper import DyeColorHelper

ShulkerEntity = TypeVar["net.minecraft.entity.mob.ShulkerEntity"]

class ShulkerEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: ShulkerEntity) -> None:
		pass

	@overload
	def isClosed(self) -> bool:
		pass

	@overload
	def getAttachedSide(self) -> DirectionHelper:
		pass

	@overload
	def getColor(self) -> DyeColorHelper:
		pass

	pass


