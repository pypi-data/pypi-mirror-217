from typing import overload
from typing import TypeVar
from typing import Mapping
from typing import Set

Identifier = TypeVar["net.minecraft.util.Identifier"]
Advancement = TypeVar["net.minecraft.advancement.Advancement"]

class MixinAdvancementManager:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getAdvancements(self) -> Mapping[Identifier, Advancement]:
		pass

	@overload
	def getDependents(self) -> Set[Advancement]:
		pass

	pass


