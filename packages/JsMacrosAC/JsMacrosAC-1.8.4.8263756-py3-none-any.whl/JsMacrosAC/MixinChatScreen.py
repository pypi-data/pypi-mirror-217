from typing import overload
from typing import TypeVar

CallbackInfoReturnable = TypeVar["org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable_java.lang.Boolean_"]
Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]

class MixinChatScreen(Screen):

	@overload
	def onSendChatMessage(self, chatText: str, addToHistory: bool, cir: CallbackInfoReturnable) -> None:
		pass

	pass


