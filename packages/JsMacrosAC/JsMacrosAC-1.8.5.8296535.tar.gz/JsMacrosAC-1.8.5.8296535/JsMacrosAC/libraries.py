from typing import TypeVar

from .EventContainer import EventContainer
from .BaseEvent import BaseEvent
from .FChat import FChat
from .FPlayer import FPlayer
from .FRequest import FRequest
from .FKeyBind import FKeyBind
from .FHud import FHud
from .FJavaUtils import FJavaUtils
from .FTime import FTime
from .FFS import FFS
from .FJsMacros import FJsMacros
from .FReflection import FReflection
from .FUtils import FUtils
from .FClient import FClient
from .FWorld import FWorld
from .FGlobalVars import FGlobalVars
from .IFWrapper import IFWrapper
from .FPositionCommon import FPositionCommon

File = TypeVar("java.io.File")



Chat = FChat()
Player = FPlayer()
Request = FRequest()
KeyBind = FKeyBind()
Hud = FHud()
JavaUtils = FJavaUtils()
Time = FTime()
FS = FFS()
JsMacros = FJsMacros()
Reflection = FReflection()
Utils = FUtils()
Client = FClient()
World = FWorld()
GlobalVars = FGlobalVars()
JavaWrapper = IFWrapper()
PositionCommon = FPositionCommon()
context = EventContainer()
file = File()
event = BaseEvent()
