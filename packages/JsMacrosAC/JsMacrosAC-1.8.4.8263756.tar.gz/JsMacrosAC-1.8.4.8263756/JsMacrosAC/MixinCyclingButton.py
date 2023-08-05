from typing import overload
from typing import TypeVar

Function = TypeVar["java.util.function.Function_T,net.minecraft.text.Text_"]
T = TypeVar("T")
Text = TypeVar["net.minecraft.text.Text"]

class MixinCyclingButton:
	"""
	Since: 1.8.4 
	"""

	@overload
	def invokeCycle(self, amount: int) -> None:
		pass

	@overload
	def invokeComposeText(self, value: T) -> Text:
		pass

	@overload
	def getValueToText(self) -> Function:
		pass

	pass


