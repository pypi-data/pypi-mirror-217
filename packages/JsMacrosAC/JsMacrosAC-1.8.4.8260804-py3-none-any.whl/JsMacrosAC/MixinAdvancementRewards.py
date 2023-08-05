from typing import overload
from typing import List
from typing import TypeVar

Identifier = TypeVar["net.minecraft.util.Identifier"]

class MixinAdvancementRewards:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getExperience(self) -> int:
		pass

	@overload
	def getLoot(self) -> List[Identifier]:
		pass

	pass


