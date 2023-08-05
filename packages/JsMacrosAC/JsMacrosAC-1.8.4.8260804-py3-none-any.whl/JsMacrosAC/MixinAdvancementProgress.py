from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping

CriterionProgress = TypeVar["net.minecraft.advancement.criterion.CriterionProgress"]

class MixinAdvancementProgress:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getRequirements(self) -> List[List[str]]:
		pass

	@overload
	def invokeCountObtainedRequirements(self) -> int:
		pass

	@overload
	def getCriteriaProgresses(self) -> Mapping[str, CriterionProgress]:
		pass

	pass


