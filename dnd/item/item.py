from dnd.item import money

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Union


class Item(object):
    Item = 0
    Weapon = 1
    Armor = 2
    ItemTypeLookup = {"Item": 0, "Weapon": 1, "Armor": 2}

    @staticmethod
    def from_json(json_data: 'Dict[str, Union[str, int, float, list, dict]]'):
        type_str = json_data.pop("type", "Item")
        type_ = Item.ItemTypeLookup.get(type_str, -1)
        if type_ == -1:
            raise KeyError("Invalid Item Type {}".format(type_str))

        if type_ == Item.Weapon:
            raise NotImplementedError()
        if type_ == Item.Armor:
            raise NotImplementedError()

        key = json_data.pop("key", None)
        if key is None:
            raise KeyError("Missing required field 'key'")

        value = money.Money(json_data.pop("value", None))

        name = json_data.pop("name", "")
        return Item(key, type_, name, value=value, **json_data)

    def __init__(self, key: str, type_: int, name: str, **kwargs) -> None:
        self._key = key
        self._type = type_
        self._name = name
        self._weight = float(kwargs.pop("weight", 0.001))  # type: float
        self._value = kwargs.pop("value", money.Money())   # type: money.Money
        self._desc = str(kwargs.pop("description", ""))    # type: str
        self._source = str(kwargs.pop("source", ""))       # type: str

        # These are derived from the key
        self._categories = self._key.split('.')
        self._short_key = self._categories.pop()

        if len(kwargs.keys()) > 0:
            raise KeyError("Unknown keyword arguments: {}".format(", ".join(kwargs.keys())))

    def key(self, full: bool = True) -> str:
        return self._key if full else self._short_key

    def type(self) -> int:
        return self._type

    def name(self) -> str:
        return self._name

    def weight(self) -> float:
        return self._weight

    def value(self) -> 'money.Money':
        return self._value

    def description(self) -> str:
        return self._desc

    def source(self) -> str:
        return self._source

    def categories(self) -> 'List[str]':
        return self._categories

    def to_json(self) -> 'Dict':
        d = dict()
        d["key"] = self._key
        d["type"] = "Item"
        d["name"] = self._name
        d["weight"] = self._weight
        d["value"] = self._value.json()
        if self._desc != "":
            d["desc"] = self._desc
        if self._source != "":
            d["source"] = self._source
        return d
