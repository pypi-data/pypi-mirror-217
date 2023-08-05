from typing import overload
from typing import TypeVar

Text = TypeVar["net.minecraft.text.Text"]

class TranslationUtil:
	"""
	Since: 1.6.4 
	"""

	@overload
	def getTranslatedEventName(self, eventName: str) -> Text:
		pass

	pass


