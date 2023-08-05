from typing import overload
from typing import TypeVar

Comparator = TypeVar["java.util.Comparator_java.lang.String_"]

class Sorting_SortServiceByFileName(Comparator):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def compare(self, a: str, b: str) -> int:
		pass

	pass


