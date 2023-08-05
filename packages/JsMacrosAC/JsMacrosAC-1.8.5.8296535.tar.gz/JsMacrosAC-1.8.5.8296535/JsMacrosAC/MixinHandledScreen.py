from typing import overload
from typing import TypeVar
from typing import Generic
from .IInventory import IInventory

T = TypeVar("T")
org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_screen_slot_Slot = TypeVar("net_minecraft_screen_slot_Slot")
Slot = net_minecraft_screen_slot_Slot


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


