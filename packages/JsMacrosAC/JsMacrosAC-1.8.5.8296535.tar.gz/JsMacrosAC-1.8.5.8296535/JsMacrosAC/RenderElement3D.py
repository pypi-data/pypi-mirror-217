from typing import overload
from typing import TypeVar

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_render_BufferBuilder = TypeVar("net_minecraft_client_render_BufferBuilder")
BufferBuilder = net_minecraft_client_render_BufferBuilder


class RenderElement3D(Comparable):

	@overload
	def render(self, drawContext: DrawContext, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	@overload
	def compareTo(self, o: "RenderElement3D") -> int:
		pass

	pass


