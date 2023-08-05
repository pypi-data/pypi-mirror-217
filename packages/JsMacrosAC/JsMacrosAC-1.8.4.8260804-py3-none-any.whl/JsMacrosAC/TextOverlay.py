from typing import overload
from typing import TypeVar
from .OverlayContainer import OverlayContainer
from .IOverlayParent import IOverlayParent

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
Text = TypeVar["net.minecraft.text.Text"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class TextOverlay(OverlayContainer):
	centered: bool

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: IOverlayParent, text: Text) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def render(self, drawContext: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


