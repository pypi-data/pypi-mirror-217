from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .BaseHelper import BaseHelper

com_mojang_brigadier_context_CommandContext__ = TypeVar("com_mojang_brigadier_context_CommandContext__")
CommandContext = com_mojang_brigadier_context_CommandContext__

com_mojang_brigadier_context_StringRange = TypeVar("com_mojang_brigadier_context_StringRange")
StringRange = com_mojang_brigadier_context_StringRange


class CommandContextHelper(BaseEvent, BaseHelper):
	"""
	Since: 1.4.2 
	"""

	@overload
	def __init__(self, base: CommandContext) -> None:
		pass

	@overload
	def getArg(self, name: str) -> object:
		"""
		Since: 1.4.2 

		Args:
			name: 
		"""
		pass

	@overload
	def getChild(self) -> "CommandContextHelper":
		pass

	@overload
	def getRange(self) -> StringRange:
		pass

	@overload
	def getInput(self) -> str:
		pass

	pass


