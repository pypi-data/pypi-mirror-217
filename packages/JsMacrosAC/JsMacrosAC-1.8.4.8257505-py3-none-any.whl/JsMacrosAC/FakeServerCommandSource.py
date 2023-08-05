from typing import overload
from typing import List
from typing import TypeVar
from typing import Set

CompletableFuture = TypeVar["java.util.concurrent.CompletableFuture_com.mojang.brigadier.suggestion.Suggestions_"]
CommandContext = TypeVar["com.mojang.brigadier.context.CommandContext__"]
ClientCommandSource = TypeVar["net.minecraft.client.network.ClientCommandSource"]
CommandSource_RelativePosition = TypeVar["net.minecraft.command.CommandSource.RelativePosition"]
DynamicRegistryManager = TypeVar["net.minecraft.registry.DynamicRegistryManager"]
Stream = TypeVar["java.util.stream.Stream_net.minecraft.util.Identifier_"]
Supplier = TypeVar["java.util.function.Supplier_net.minecraft.text.Text_"]
Text = TypeVar["net.minecraft.text.Text"]
ClientPlayerEntity = TypeVar["net.minecraft.client.network.ClientPlayerEntity"]
RegistryKey = TypeVar["net.minecraft.registry.RegistryKey_net.minecraft.world.World_"]
ServerCommandSource = TypeVar["net.minecraft.server.command.ServerCommandSource"]

class FakeServerCommandSource(ServerCommandSource):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, source: ClientCommandSource, player: ClientPlayerEntity) -> None:
		pass

	@overload
	def getEntitySuggestions(self) -> List[str]:
		pass

	@overload
	def getChatSuggestions(self) -> List[str]:
		pass

	@overload
	def getPlayerNames(self) -> List[str]:
		pass

	@overload
	def getTeamNames(self) -> List[str]:
		pass

	@overload
	def getSoundIds(self) -> Stream:
		pass

	@overload
	def getRecipeIds(self) -> Stream:
		pass

	@overload
	def getCompletions(self, context: CommandContext) -> CompletableFuture:
		pass

	@overload
	def getBlockPositionSuggestions(self) -> List[CommandSource_RelativePosition]:
		pass

	@overload
	def getPositionSuggestions(self) -> List[CommandSource_RelativePosition]:
		pass

	@overload
	def getWorldKeys(self) -> Set[RegistryKey]:
		pass

	@overload
	def getRegistryManager(self) -> DynamicRegistryManager:
		pass

	@overload
	def sendFeedback(self, feedbackSupplier: Supplier, broadcastToOps: bool) -> None:
		pass

	@overload
	def sendFeedback(self, message: Text, broadcastToOps: bool) -> None:
		pass

	pass


