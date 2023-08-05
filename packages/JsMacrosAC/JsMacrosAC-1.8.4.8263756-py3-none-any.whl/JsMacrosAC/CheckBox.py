from typing import overload
from typing import TypeVar

Consumer = TypeVar["java.util.function.Consumer_xyz.wagyourtail.wagyourgui.elements.CheckBox_"]
CheckboxWidget = TypeVar["net.minecraft.client.gui.widget.CheckboxWidget"]
Text = TypeVar["net.minecraft.text.Text"]

class CheckBox(CheckboxWidget):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, checked: bool, action: Consumer) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, checked: bool, showMessage: bool, action: Consumer) -> None:
		pass

	@overload
	def onPress(self) -> None:
		pass

	pass


