from typing import overload
from typing import TypeVar

DrawContext = TypeVar["net.minecraft.client.gui.DrawContext"]
BufferBuilder = TypeVar["net.minecraft.client.render.BufferBuilder"]

class RenderElement3D(Comparable):

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	@overload
	def compareTo(self, o: "RenderElement3D") -> int:
		pass

	pass


