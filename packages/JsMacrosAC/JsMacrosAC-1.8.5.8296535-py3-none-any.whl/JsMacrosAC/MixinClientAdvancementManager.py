from typing import overload
from typing import TypeVar
from typing import Mapping

net_minecraft_advancement_AdvancementProgress = TypeVar("net_minecraft_advancement_AdvancementProgress")
AdvancementProgress = net_minecraft_advancement_AdvancementProgress

net_minecraft_advancement_Advancement = TypeVar("net_minecraft_advancement_Advancement")
Advancement = net_minecraft_advancement_Advancement


class MixinClientAdvancementManager:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getAdvancementProgresses(self) -> Mapping[Advancement, AdvancementProgress]:
		pass

	pass


