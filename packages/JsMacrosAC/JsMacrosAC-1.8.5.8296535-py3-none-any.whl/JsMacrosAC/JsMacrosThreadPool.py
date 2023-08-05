from typing import overload
from typing import List
from typing import TypeVar

java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable


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


