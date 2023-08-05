from typing import overload
from typing import TypeVar
from .Pos2D import Pos2D
from .Vec3D import Vec3D
from .BlockPosHelper import BlockPosHelper

BlockPos = TypeVar["net.minecraft.util.math.BlockPos"]
Vec3d = TypeVar["net.minecraft.util.math.Vec3d"]

class Pos3D(Pos2D):
	"""
	Since: 1.2.6 [citation needed] 
	"""
	ZERO: "Pos3D"
	z: float

	@overload
	def __init__(self, vec: Vec3d) -> None:
		pass

	@overload
	def __init__(self, x: float, y: float, z: float) -> None:
		pass

	@overload
	def getZ(self) -> float:
		pass

	@overload
	def add(self, pos: "Pos3D") -> "Pos3D":
		pass

	@overload
	def add(self, x: float, y: float, z: float) -> "Pos3D":
		"""
		Since: 1.6.3 

		Args:
			x: 
			y: 
			z: 
		"""
		pass

	@overload
	def sub(self, pos: "Pos3D") -> "Pos3D":
		"""
		Since: 1.8.4 

		Args:
			pos: the position to subtract 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def sub(self, x: float, y: float, z: float) -> "Pos3D":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to subtract 
			y: the y coordinate to subtract 
			z: the z coordinate to subtract 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def multiply(self, pos: "Pos3D") -> "Pos3D":
		pass

	@overload
	def multiply(self, x: float, y: float, z: float) -> "Pos3D":
		"""
		Since: 1.6.3 

		Args:
			x: 
			y: 
			z: 
		"""
		pass

	@overload
	def divide(self, pos: "Pos3D") -> "Pos3D":
		"""
		Since: 1.8.4 

		Args:
			pos: the position to divide by 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def divide(self, x: float, y: float, z: float) -> "Pos3D":
		"""
		Since: 1.8.4 

		Args:
			x: the x coordinate to divide by 
			y: the y coordinate to divide by 
			z: the z coordinate to divide by 

		Returns:
			the new position. 
		"""
		pass

	@overload
	def scale(self, scale: float) -> "Pos3D":
		"""
		Since: 1.6.3 

		Args:
			scale: 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def toVector(self) -> Vec3D:
		pass

	@overload
	def toVector(self, start_pos: Pos2D) -> Vec3D:
		"""
		Since: 1.6.4 

		Args:
			start_pos: 
		"""
		pass

	@overload
	def toVector(self, start_pos: "Pos3D") -> Vec3D:
		"""
		Since: 1.6.4 

		Args:
			start_pos: 
		"""
		pass

	@overload
	def toVector(self, start_x: float, start_y: float, start_z: float) -> Vec3D:
		"""
		Since: 1.6.4 

		Args:
			start_x: 
			start_z: 
			start_y: 
		"""
		pass

	@overload
	def toReverseVector(self) -> Vec3D:
		"""
		Since: 1.6.4 
		"""
		pass

	@overload
	def toReverseVector(self, end_pos: Pos2D) -> Vec3D:
		pass

	@overload
	def toReverseVector(self, end_pos: "Pos3D") -> Vec3D:
		"""
		Since: 1.6.4 

		Args:
			end_pos: 
		"""
		pass

	@overload
	def toReverseVector(self, end_x: float, end_y: float, end_z: float) -> Vec3D:
		"""
		Since: 1.6.4 

		Args:
			end_z: 
			end_x: 
			end_y: 
		"""
		pass

	@overload
	def toBlockPos(self) -> BlockPosHelper:
		"""
		Since: 1.8.0 
		"""
		pass

	@overload
	def toRawBlockPos(self) -> BlockPos:
		"""
		Since: 1.8.0 
		"""
		pass

	@overload
	def toMojangDoubleVector(self) -> Vec3d:
		"""
		Since: 1.8.4 

		Returns:
			the raw minecraft double vector with the same coordinates as this position. 
		"""
		pass

	pass


