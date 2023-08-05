from typing import overload
from typing import List
from typing import TypeVar

Runnable = TypeVar["java.lang.Runnable"]

class JsMacrosThreadPool:
	minFreeThreads: int
	maxFreeThreads: int

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def __init__(self, minFreeThreads: int, maxFreeThreads: int) -> None:
		pass

	@overload
	def runTask(self, task: Runnable) -> None:
		pass

	@overload
	def main(self, args: List[str]) -> None:
		pass

	pass


