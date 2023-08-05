from typing import overload
from typing import TypeVar
from typing import Mapping
from typing import Set

net_minecraft_util_Identifier = TypeVar("net_minecraft_util_Identifier")
Identifier = net_minecraft_util_Identifier

net_minecraft_advancement_Advancement = TypeVar("net_minecraft_advancement_Advancement")
Advancement = net_minecraft_advancement_Advancement


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


