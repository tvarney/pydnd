
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional, Tuple


class Money(object):
    def __init__(self, **kwargs) -> None:
        self._pp = int(kwargs.get('pp', 0))
        self._gp = int(kwargs.get('gp', 0))
        self._sp = int(kwargs.get('sp', 0))
        self._cp = int(kwargs.get('cp', 0))

    def cp(self) -> int:
        return self._cp

    def sp(self) -> int:
        return self._sp

    def gp(self) -> int:
        return self._gp

    def pp(self) -> int:
        return self._pp

    def weight(self) -> float:
        return (self._cp + self._sp + self._gp + self._pp) * 0.02

    def __str__(self):
        parts = list()
        if self._pp != 0:
            parts.append("{} pp".format(self._pp))
        if self._gp != 0:
            parts.append("{} gp".format(self._gp))
        if self._sp != 0:
            parts.append("{} sp".format(self._sp))
        if self._cp != 0:
            parts.append("{} cp".format(self._cp))
        if len(parts) > 0:
            return " ".join(parts)
        return "0 gp"

    def __repr__(self):
        parts = list()
        if self._pp != 0:
            parts.append("pp={}".format(self._pp))
        if self._gp != 0:
            parts.append("gp={}".format(self._gp))
        if self._sp != 0:
            parts.append("sp={}".format(self._sp))
        if self._cp != 0:
            parts.append("cp={}".format(self._cp))
        return "Money({})".format(", ".join(parts))


class Item(object):
    All = dict()
    Category = dict()

    Misc = 0
    Weapon = 1
    Armor = 2

    def __init__(self, key: str, type_: int, name: str, value: 'Money', **kwargs) -> None:
        self._key = key
        self._type = type_
        self._name = name
        self._value = value
        self._desc = str(kwargs.get("description", ""))  # type: str
        self._categories = list(kwargs.get("categories", list()))  # type: List[str]

    def register(self, replace: bool = False) -> 'Tuple[bool, Optional[str]]':
        err_str = None
        if self._key in Item.All:
            err_str = "Item with key={} already exists in Item.All".format(self._key)
            if not replace:
                return False, err_str
            raise NotImplementedError("Item Replacement not implemented")
        Item.All[self._key] = self
        return True, err_str

    def key(self) -> str:
        return self._key

    def type(self) -> int:
        return self._type

    def name(self) -> str:
        return self._name

    def value(self) -> 'Money':
        return self._value

    def description(self) -> str:
        return self._desc

    def categories(self) -> str:
