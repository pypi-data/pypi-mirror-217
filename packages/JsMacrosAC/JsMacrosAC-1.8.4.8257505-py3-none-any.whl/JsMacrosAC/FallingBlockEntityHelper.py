from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper
from .BlockPosHelper import BlockPosHelper
from .BlockStateHelper import BlockStateHelper

FallingBlockEntity = TypeVar["net.minecraft.entity.FallingBlockEntity"]

class FallingBlockEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: FallingBlockEntity) -> None:
		pass

	@overload
	def getOriginBlockPos(self) -> BlockPosHelper:
		"""
		Since: 1.8.4 

		Returns:
			the block position this block is falling from. 
		"""
		pass

	@overload
	def getBlockState(self) -> BlockStateHelper:
		"""
		Since: 1.8.4 

		Returns:
			the block state of this falling block. 
		"""
		pass

	pass


