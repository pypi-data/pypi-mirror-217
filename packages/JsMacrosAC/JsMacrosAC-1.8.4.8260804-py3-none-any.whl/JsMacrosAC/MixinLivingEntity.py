from typing import overload
from typing import TypeVar

EntityType = TypeVar["net.minecraft.entity.EntityType__"]
Entity = TypeVar["net.minecraft.entity.Entity"]
CallbackInfo = TypeVar["org.spongepowered.asm.mixin.injection.callback.CallbackInfo"]
World = TypeVar["net.minecraft.world.World"]

class MixinLivingEntity(Entity):

	@overload
	def __init__(self, arg: EntityType, arg2: World) -> None:
		pass

	@overload
	def getMaxHealth(self) -> float:
		pass

	@overload
	def onSetHealth(self, health: float, ci: CallbackInfo) -> None:
		pass

	pass


