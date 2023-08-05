from typing import overload
from typing import TypeVar
from .AnimalEntityHelper import AnimalEntityHelper

OcelotEntity = TypeVar["net.minecraft.entity.passive.OcelotEntity"]

class OcelotEntityHelper(AnimalEntityHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, base: OcelotEntity) -> None:
		pass

	@overload
	def isTrusting(self) -> bool:
		"""Ocelots trust players after being fed with cod or salmon.\n
		Since: 1.8.4 

		Returns:
			'true' if this ocelot is trusting player and not running away form them, 'false' otherwise. 
		"""
		pass

	pass


