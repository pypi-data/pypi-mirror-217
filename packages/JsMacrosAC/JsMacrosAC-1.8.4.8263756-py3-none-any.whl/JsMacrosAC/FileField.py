from typing import overload
from typing import TypeVar
from .AbstractSettingField import AbstractSettingField
from .AbstractSettingContainer import AbstractSettingContainer
from .SettingsOverlay_SettingField import SettingsOverlay_SettingField

DrawContext = TypeVar["net.minecraft.client.gui.DrawContext"]
File = TypeVar["java.io.File"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class FileField(AbstractSettingField):

	@overload
	def __init__(self, x: int, y: int, width: int, textRenderer: TextRenderer, parent: AbstractSettingContainer, field: SettingsOverlay_SettingField) -> None:
		pass

	@overload
	def getTopLevel(self, setting: SettingsOverlay_SettingField) -> File:
		pass

	@overload
	def relativize(self, setting: SettingsOverlay_SettingField, file: File) -> str:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


