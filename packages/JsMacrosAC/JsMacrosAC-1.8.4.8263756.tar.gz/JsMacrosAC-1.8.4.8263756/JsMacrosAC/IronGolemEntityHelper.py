from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

IronGolemEntity = TypeVar["net.minecraft.entity.passive.IronGolemEntity"]

class IronGolemEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: IronGolemEntity) -> None:
		pass

	@overload
	def isPlayerCreated(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this iron golem was created by a player, 'false' otherwise. 
		"""
		pass

	pass


