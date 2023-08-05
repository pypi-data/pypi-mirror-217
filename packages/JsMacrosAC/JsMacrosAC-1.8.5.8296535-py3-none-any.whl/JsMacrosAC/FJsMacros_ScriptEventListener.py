from typing import overload
from typing import TypeVar
from .IEventListener import IEventListener
from .MethodWrapper import MethodWrapper

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread


class FJsMacros_ScriptEventListener(IEventListener):

	@overload
	def getCreator(self) -> Thread:
		pass

	@overload
	def getWrapper(self) -> MethodWrapper:
		pass

	pass


