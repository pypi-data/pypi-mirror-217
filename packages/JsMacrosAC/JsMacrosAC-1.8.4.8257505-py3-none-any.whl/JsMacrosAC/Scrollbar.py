from typing import overload
from typing import TypeVar

Consumer = TypeVar["java.util.function.Consumer_java.lang.Double_"]
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
ClickableWidget = TypeVar["net.minecraft.client.gui.widget.ClickableWidget"]

class Scrollbar(ClickableWidget):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, color: int, borderColor: int, highlightColor: int, scrollPages: float, onChange: Consumer) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> "Scrollbar":
		pass

	@overload
	def setScrollPages(self, scrollPages: float) -> None:
		pass

	@overload
	def scrollToPercent(self, percent: float) -> None:
		pass

	@overload
	def onClick(self, mouseX: float, mouseY: float) -> None:
		pass

	@overload
	def onChange(self) -> None:
		pass

	@overload
	def mouseDragged(self, mouseX: float, mouseY: float, button: int, deltaX: float, deltaY: float) -> bool:
		pass

	@overload
	def renderButton(self, drawContext: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


