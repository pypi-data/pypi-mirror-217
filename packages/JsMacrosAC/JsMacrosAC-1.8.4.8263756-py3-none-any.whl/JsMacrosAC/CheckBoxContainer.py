from typing import overload
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .IContainerParent import IContainerParent

Consumer = TypeVar["java.util.function.Consumer_java.lang.Boolean_"]
DrawContext = TypeVar["net.minecraft.client.gui.DrawContext"]
Text = TypeVar["net.minecraft.text.Text"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class CheckBoxContainer(MultiElementContainer):
	message: Text

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, defaultState: bool, message: Text, parent: IContainerParent, setState: Consumer) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


