import json
import requests
from common import configs, selectors, trace
from enum import Enum


class ClickType(Enum):
    Single = 0
    Doulbe = 1
    Down = 2
    Up = 3


class MouseButton(Enum):
    Left = 0
    Right = 1
    Middle = 2


class Position(Enum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3
    Center = 4


class InputMethod(Enum):
    Empty = -1
    Synthesize = 0
    WindowsMessage = 1
    API = 2


class KeyModifiers(Enum):
    Empty = 0
    Alt = 1
    Ctrl = 2
    Shift = 4
    Win = 8


class uielement(object):
    @staticmethod
    def beforecall(ins, obj): return None

    @staticmethod
    def aftercall(ins, obj): return None

    def __init__(self, selector='', **attrs):
        self.selector = selector
        self.attrs = attrs
        self.selectorkey = selector
        self.recursive = 0

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if(hasattr(attr, '__call__') and not name == 'execute'):
            def newfunc(*args, **kwargs):
                # parse selector
                if(not self.selector == '' and not self.selector.startswith('<')):
                    self.selector = selectors[self.selector]

                # construct request
                locals = attr(*args, **kwargs)
                fargs = {}
                for k in locals:
                    if(k != 'self'):
                        if(isinstance(locals[k], Enum)):
                            fargs[k] = locals[k].value
                        else:
                            fargs[k] = locals[k]
                obj = {"selector": self.selector,
                       "method": attr.__name__, "args": fargs, "attrs": self.attrs}
                trace(json.dumps(obj))

                # use proxy to execute
                if(not self.recursive):
                    self.recursive += 1
                    uielement.beforecall(self, obj)
                    self.recursive -= 1

                result = self.execute(obj)
                trace(result)
                if(not self.recursive):
                    self.recursive += 1
                    uielement.aftercall(self, obj)
                    self.recursive -= 1

                if(result["stat"] == 0):
                    return result["value"]
                raise result["message"]
                # return result
            return newfunc
        return attr

    def execute(self, obj):
        return requests.post(
            configs["adapter"], data=json.dumps(obj)).json()

    def click(self, type=ClickType.Single, button=MouseButton.Left, pos=Position.Center, method=InputMethod.API):
        return locals()

    def highlight(self, seconds=5, color='red'):
        return locals()

    def sendhotkey(self, key, modifiers=KeyModifiers.Empty, isSpecial=0):
        return locals()

    def typetext(self, text, method=InputMethod.WindowsMessage):
        return locals()

    def gettext(self):
        return locals()
