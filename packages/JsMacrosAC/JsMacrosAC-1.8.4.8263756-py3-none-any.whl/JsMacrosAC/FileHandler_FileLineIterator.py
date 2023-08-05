from typing import overload
from typing import TypeVar

File = TypeVar["java.io.File"]

class FileHandler_FileLineIterator(iter, AutoCloseable):

	@overload
	def __init__(self, file: File, charset: Charset) -> None:
		pass

	@overload
	def hasNext(self) -> bool:
		pass

	@overload
	def next(self) -> str:
		pass

	@overload
	def close(self) -> None:
		pass

	pass


