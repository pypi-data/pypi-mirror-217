from typing import overload
from typing import TypeVar

Consumer = TypeVar["java.util.function.Consumer_xyz.wagyourtail.wagyourgui.elements.Slider_"]
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
ClickableWidget = TypeVar["net.minecraft.client.gui.widget.ClickableWidget"]
Text = TypeVar["net.minecraft.text.Text"]

class Slider(ClickableWidget):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, value: float, action: Consumer, steps: int) -> None:
		pass

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, text: Text, value: float, action: Consumer) -> None:
		pass

	@overload
	def keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		pass

	@overload
	def roundValue(self, value: float) -> float:
		pass

	@overload
	def getValue(self) -> float:
		pass

	@overload
	def setValue(self, mouseX: float) -> None:
		pass

	@overload
	def getSteps(self) -> int:
		pass

	@overload
	def setSteps(self, steps: int) -> None:
		pass

	@overload
	def renderButton(self, drawContext: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def onRelease(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def setMessage(self, message: str) -> None:
		pass

	@overload
	def setMessage(self, message: Text) -> None:
		pass

	pass


