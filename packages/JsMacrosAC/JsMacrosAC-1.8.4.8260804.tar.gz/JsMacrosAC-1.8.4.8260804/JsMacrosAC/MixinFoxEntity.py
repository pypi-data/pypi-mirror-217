from typing import overload
from typing import List
from typing import TypeVar

UUID = TypeVar["java.util.UUID"]

class MixinFoxEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeIsAggressive(self) -> bool:
		pass

	@overload
	def invokeGetTrustedUuids(self) -> List[UUID]:
		pass

	pass


