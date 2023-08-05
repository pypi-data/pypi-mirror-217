from typing import overload


class ICancelable:
	"""
	Since: 1.8.4 
	"""

	@overload
	def cancel(self) -> None:
		pass

	@overload
	def isCanceled(self) -> bool:
		pass

	pass


