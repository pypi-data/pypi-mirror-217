from typing import overload
from typing import TypeVar
from typing import Mapping

AdvancementProgress = TypeVar["net.minecraft.advancement.AdvancementProgress"]
Advancement = TypeVar["net.minecraft.advancement.Advancement"]

class MixinClientAdvancementManager:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getAdvancementProgresses(self) -> Mapping[Advancement, AdvancementProgress]:
		pass

	pass


