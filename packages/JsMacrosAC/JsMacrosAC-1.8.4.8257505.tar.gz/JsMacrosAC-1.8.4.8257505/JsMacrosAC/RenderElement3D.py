from typing import overload
from typing import TypeVar

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
BufferBuilder = TypeVar["net.minecraft.client.render.BufferBuilder"]

class RenderElement3D(Comparable):

	@overload
	def render(self, drawContext: MatrixStack, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	@overload
	def compareTo(self, o: "RenderElement3D") -> int:
		pass

	pass


