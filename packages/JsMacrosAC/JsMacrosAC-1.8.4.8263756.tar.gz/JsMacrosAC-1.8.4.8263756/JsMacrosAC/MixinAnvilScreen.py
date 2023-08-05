from typing import overload
from typing import TypeVar

TextFieldWidget = TypeVar["net.minecraft.client.gui.widget.TextFieldWidget"]

class MixinAnvilScreen:
	"""
	Since: 1.8.4 
	"""

	@overload
	def getNameField(self) -> TextFieldWidget:
		pass

	pass


