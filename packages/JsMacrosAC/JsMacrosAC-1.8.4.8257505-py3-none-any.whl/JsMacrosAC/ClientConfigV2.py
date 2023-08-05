from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .Sorting_MacroSortMethod import Sorting_MacroSortMethod
from .Sorting_ServiceSortMethod import Sorting_ServiceSortMethod

JsonObject = TypeVar["com.google.gson.JsonObject"]
Comparator = TypeVar["java.util.Comparator_java.lang.String_"]

class ClientConfigV2:
	sortMethod: Sorting_MacroSortMethod
	sortServicesMethod: Sorting_ServiceSortMethod
	showSlotIndexes: bool
	disableKeyWhenScreenOpen: bool
	editorTheme: Mapping[str, List[float]]
	editorLinterOverrides: Mapping[str, str]
	editorHistorySize: int
	editorSuggestions: bool
	editorFont: str
	externalEditor: bool
	externalEditorCommand: str
	showRunningServices: bool
	serviceAutoReload: bool

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def languages(self) -> List[str]:
		pass

	@overload
	def getFonts(self) -> List[str]:
		pass

	@overload
	def getThemeData(self) -> Mapping[str, List[float]]:
		pass

	@overload
	def setServiceAutoReload(self, value: bool) -> None:
		pass

	@overload
	def getSortComparator(self) -> Comparator:
		pass

	@overload
	def getServiceSortComparator(self) -> Comparator:
		pass

	@overload
	def fromV1(self, v1: JsonObject) -> None:
		pass

	pass


