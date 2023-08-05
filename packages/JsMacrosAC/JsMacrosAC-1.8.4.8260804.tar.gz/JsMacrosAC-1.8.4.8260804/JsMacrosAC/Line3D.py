from typing import overload
from typing import TypeVar
from .RenderElement3D import RenderElement3D
from .Vec3D import Vec3D

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
BufferBuilder = TypeVar["net.minecraft.client.render.BufferBuilder"]

class Line3D(RenderElement3D):
	"""
	"""
	pos: Vec3D
	color: int
	cull: bool

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, cull: bool) -> None:
		pass

	@overload
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, color: int, alpha: int, cull: bool) -> None:
		pass

	@overload
	def setPos(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
		"""
		Since: 1.0.6 

		Args:
			z1: 
			y1: 
			z2: 
			x1: 
			y2: 
			x2: 
		"""
		pass

	@overload
	def setColor(self, color: int) -> None:
		"""
		Since: 1.0.6 

		Args:
			color: 
		"""
		pass

	@overload
	def setColor(self, color: int, alpha: int) -> None:
		"""
		Since: 1.1.8 

		Args:
			color: 
			alpha: 
		"""
		pass

	@overload
	def setAlpha(self, alpha: int) -> None:
		"""
		Since: 1.1.8 

		Args:
			alpha: 
		"""
		pass

	@overload
	def render(self, matrixStack: MatrixStack, builder: BufferBuilder, tickDelta: float) -> None:
		pass

	pass


