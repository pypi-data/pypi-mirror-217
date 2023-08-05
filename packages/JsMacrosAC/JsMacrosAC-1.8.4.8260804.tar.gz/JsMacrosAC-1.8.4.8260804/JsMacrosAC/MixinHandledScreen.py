from typing import overload
from typing import TypeVar
from typing import Generic
from .IInventory import IInventory

T = TypeVar("T")
CallbackInfo = TypeVar["org.spongepowered.asm.mixin.injection.callback.CallbackInfo"]
Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
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
	def onDrawForeground(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float, ci: CallbackInfo) -> None:
		pass

	pass


