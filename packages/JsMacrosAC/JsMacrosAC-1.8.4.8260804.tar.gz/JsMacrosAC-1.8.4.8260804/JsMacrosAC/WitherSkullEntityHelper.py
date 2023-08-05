from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

WitherSkullEntity = TypeVar["net.minecraft.entity.projectile.WitherSkullEntity"]

class WitherSkullEntityHelper(EntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: WitherSkullEntity) -> None:
		pass

	@overload
	def isCharged(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if the wither skull is charged, 'false' otherwise. 
		"""
		pass

	pass


