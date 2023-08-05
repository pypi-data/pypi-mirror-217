from typing import overload
from typing import TypeVar

TrackedData = TypeVar["net.minecraft.entity.data.TrackedData_java.lang.Byte_"]

class MixinTridentEntity:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getLoyalty(self) -> TrackedData:
		pass

	pass


