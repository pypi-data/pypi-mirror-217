from typing import overload
from typing import TypeVar
from .MobEntityHelper import MobEntityHelper

SlimeEntity = TypeVar["net.minecraft.entity.mob.SlimeEntity"]

class SlimeEntityHelper(MobEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: SlimeEntity) -> None:
		pass

	@overload
	def getSize(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the size of this slime. 
		"""
		pass

	@overload
	def isSmall(self) -> bool:
		"""Small slimes, with a size less than 1, don't attack the player.\n
		Since: 1.8.4 

		Returns:
			'true' if this slime is small, 'false' otherwise. 
		"""
		pass

	pass


