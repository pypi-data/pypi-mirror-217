from typing import overload
from typing import TypeVar

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
MinecraftClient = TypeVar["net.minecraft.client.MinecraftClient"]
Drawable = TypeVar["net.minecraft.client.gui.Drawable"]

class RenderElement(Drawable):
	"""
	"""
	mc: MinecraftClient

	@overload
	def getZIndex(self) -> int:
		pass

	@overload
	def render3D(self, drawContext: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def setupMatrix(self, matrices: MatrixStack, x: float, y: float, scale: float, rotation: float) -> None:
		pass

	@overload
	def setupMatrix(self, matrices: MatrixStack, x: float, y: float, scale: float, rotation: float, width: float, height: float, rotateAroundCenter: bool) -> None:
		pass

	pass


