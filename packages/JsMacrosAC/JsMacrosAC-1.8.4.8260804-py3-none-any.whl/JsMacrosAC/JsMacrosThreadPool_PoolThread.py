from typing import overload
from typing import TypeVar

Runnable = TypeVar["java.lang.Runnable"]
Thread = TypeVar["java.lang.Thread"]

class JsMacrosThreadPool_PoolThread(Thread):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def start(self) -> None:
		pass

	@overload
	def runTask(self, task: Runnable) -> None:
		pass

	@overload
	def run(self) -> None:
		pass

	pass


