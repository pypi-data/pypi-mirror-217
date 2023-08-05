from typing import overload
from typing import TypeVar

net_minecraft_network_packet_s2c_play_WorldTimeUpdateS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_WorldTimeUpdateS2CPacket")
WorldTimeUpdateS2CPacket = net_minecraft_network_packet_s2c_play_WorldTimeUpdateS2CPacket

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_network_packet_s2c_play_GameJoinS2CPacket = TypeVar("net_minecraft_network_packet_s2c_play_GameJoinS2CPacket")
GameJoinS2CPacket = net_minecraft_network_packet_s2c_play_GameJoinS2CPacket


class MixinClientPlayNetworkHandler:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def onServerTime(self, packet: WorldTimeUpdateS2CPacket, info: CallbackInfo) -> None:
		pass

	@overload
	def onGameJoin(self, packet: GameJoinS2CPacket, info: CallbackInfo) -> None:
		pass

	pass


