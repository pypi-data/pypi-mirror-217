from typing import overload
from typing import List
from typing import TypeVar
from .BaseEvent import BaseEvent
from .ICancelable import ICancelable
from .PacketByteBufferHelper import PacketByteBufferHelper

Packet = TypeVar["net.minecraft.network.packet.Packet__"]

class EventJoinedSendPacket(BaseEvent, ICancelable):
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
	def replacePacket(self, args: List[object]) -> None:
		"""Replaces the packet of this event with a new one of the same type, created from the given
arguments. It's recommended to use EventJoinedSendPacket#getPacketBuffer() to modify the packet instead.\n
		Since: 1.8.4 

		Args:
			args: the arguments to pass to the packet's constructor 
		"""
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


