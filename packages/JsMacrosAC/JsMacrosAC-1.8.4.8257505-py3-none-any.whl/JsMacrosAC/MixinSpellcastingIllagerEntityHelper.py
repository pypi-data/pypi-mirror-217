from typing import overload
from typing import TypeVar

TrackedData = TypeVar["net.minecraft.entity.data.TrackedData_java.lang.Byte_"]

class MixinSpellcastingIllagerEntityHelper:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getSpellKey(self) -> TrackedData:
		pass

	pass


