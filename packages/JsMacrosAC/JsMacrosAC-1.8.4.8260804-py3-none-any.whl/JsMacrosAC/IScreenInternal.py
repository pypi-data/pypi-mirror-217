from typing import overload
from typing import TypeVar

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class IScreenInternal:

	@overload
	def jsmacros_render(self, stack: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def jsmacros_mouseClicked(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def jsmacros_mouseReleased(self, mouseX: float, mouseY: float, button: int) -> None:
		pass

	@overload
	def jsmacros_mouseDragged(self, mouseX: float, mouseY: float, button: int, deltaX: float, deltaY: float) -> None:
		pass

	@overload
	def jsmacros_mouseScrolled(self, mouseX: float, mouseY: float, amount: float) -> None:
		pass

	@overload
	def jsmacros_keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> None:
		pass

	@overload
	def jsmacros_charTyped(self, chr: str, modifiers: int) -> None:
		pass

	pass


