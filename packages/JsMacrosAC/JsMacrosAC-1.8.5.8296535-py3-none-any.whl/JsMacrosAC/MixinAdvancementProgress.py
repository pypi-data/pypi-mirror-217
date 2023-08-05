from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping

net_minecraft_advancement_criterion_CriterionProgress = TypeVar("net_minecraft_advancement_criterion_CriterionProgress")
CriterionProgress = net_minecraft_advancement_criterion_CriterionProgress


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


