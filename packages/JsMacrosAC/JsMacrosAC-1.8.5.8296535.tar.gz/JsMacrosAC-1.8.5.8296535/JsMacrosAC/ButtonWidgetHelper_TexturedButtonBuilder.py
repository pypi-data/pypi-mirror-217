from typing import overload
from .AbstractWidgetBuilder import AbstractWidgetBuilder
from .IScreen import IScreen
from .MethodWrapper import MethodWrapper
from .ButtonWidgetHelper import ButtonWidgetHelper


class ButtonWidgetHelper_TexturedButtonBuilder(AbstractWidgetBuilder):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, screen: IScreen) -> None:
		pass

	@overload
	def height(self, height: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			height: this argument is ignored and will always be set to 20 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def size(self, width: int, height: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			width: the width of the button 
			height: this argument is ignored and will always be set to 20 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getAction(self) -> MethodWrapper:
		"""
		Since: 1.8.4 

		Returns:
			the action to run when the button is pressed. 
		"""
		pass

	@overload
	def action(self, action: MethodWrapper) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			action: the action to run when the button is pressed 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getU(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the x position in the texture to start drawing from. 
		"""
		pass

	@overload
	def u(self, u: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			u: the x position in the texture to start drawing from 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getV(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the y position in the texture to start drawing from. 
		"""
		pass

	@overload
	def v(self, v: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			v: the y position in the texture to start drawing from 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def uv(self, u: int, v: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			u: the x position in the texture to start drawing from 
			v: the y position in the texture to start drawing from 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getHoverOffset(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the hover offset of the button. 
		"""
		pass

	@overload
	def hoverOffset(self, hoverOffset: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""The hover offset is the vertical amount of pixels to offset the texture when the button
is hovered.\n
		Since: 1.8.4 

		Args:
			hoverOffset: the hover offset 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTexture(self) -> str:
		"""
		Since: 1.8.4 

		Returns:
			the id of the texture to use or 'null' if none is set. 
		"""
		pass

	@overload
	def texture(self, texture: str) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""

		Args:
			texture: the texture id to use for the button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTextureWidth(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the width of the texture. 
		"""
		pass

	@overload
	def textureWidth(self, textureWidth: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			textureWidth: the width of the texture 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def getTextureHeight(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the height of the texture. 
		"""
		pass

	@overload
	def textureHeight(self, textureHeight: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			textureHeight: the height of the texture 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def textureSize(self, textureWidth: int, textureHeight: int) -> "ButtonWidgetHelper_TexturedButtonBuilder":
		"""
		Since: 1.8.4 

		Args:
			textureWidth: the width of the texture 
			textureHeight: the height of the texture 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def createWidget(self) -> ButtonWidgetHelper:
		pass

	pass


