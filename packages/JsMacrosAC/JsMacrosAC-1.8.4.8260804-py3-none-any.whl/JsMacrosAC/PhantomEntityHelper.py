from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

PhantomEntity = TypeVar["net.minecraft.entity.mob.PhantomEntity"]

class PhantomEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: PhantomEntity) -> None:
		pass

	@overload
	def getSize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the size of this phantom. 
		"""
		pass

	pass


