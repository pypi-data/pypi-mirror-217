from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ICancelable import ICancelable
from .PacketByteBufferHelper import PacketByteBufferHelper

net_minecraft_network_packet_Packet__ = TypeVar("net_minecraft_network_packet_Packet__")
Packet = net_minecraft_network_packet_Packet__


class EventJoinedRecvPacket(BaseEvent, ICancelable):
	"""
	Since: 1.8.4 
	"""
	cancel: bool
	packet: Packet
	type: str

	@overload
	def __init__(self, packet: Packet) -> None:
		pass

	@overload
	def getPacketBuffer(self) -> PacketByteBufferHelper:
		"""After modifying the buffer, use PacketByteBufferHelper#toPacket() to get the modified
packet and replace this packet with the modified one.\n
		Since: 1.8.4 

		Returns:
			a helper for accessing and modifying the packet's data. 
		"""
		pass

	@overload
	def cancel(self) -> None:
		pass

	@overload
	def isCanceled(self) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


