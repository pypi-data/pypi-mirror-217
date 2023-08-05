from typing import overload
from typing import TypeVar

Prism4j_Grammar = TypeVar["io.noties.prism4j.Prism4j.Grammar"]
Prism4j = TypeVar["io.noties.prism4j.Prism4j"]

class Prism_kotlin:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def create(self, prism4j: Prism4j) -> Prism4j_Grammar:
		pass

	pass


