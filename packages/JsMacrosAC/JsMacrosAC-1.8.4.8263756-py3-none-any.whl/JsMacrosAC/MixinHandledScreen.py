from typing import overload
from typing import TypeVar
from typing import Generic
from .IInventory import IInventory

T = TypeVar("T")
CallbackInfo = TypeVar["org.spongepowered.asm.mixin.injection.callback.CallbackInfo"]
Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]
DrawContext = TypeVar["net.minecraft.client.gui.DrawContext"]
Slot = TypeVar["net.minecraft.screen.slot.Slot"]

class MixinHandledScreen(IInventory, Generic[T], Screen):

	@overload
	def getX(self) -> int:
		pass

	@overload
	def getY(self) -> int:
		pass

	@overload
	def jsmacros_getSlotUnder(self, x: float, y: float) -> Slot:
		pass

	@overload
	def onDrawForeground(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float, ci: CallbackInfo) -> None:
		pass

	pass


