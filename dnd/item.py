
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Optional, Tuple, Union


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


class Category(object):
    def __init__(self, name: str):
        self._name = name  # type: str
        self._subcategories = dict()  # type: Dict[str, Category]
        self._items = list()  # type: List[Item]

    def name(self) -> str:
        return self._name

    def add(self, item: 'Item', category_list: 'List[str]') -> None:
        category_obj = self  # type: Category
        for subcategory in category_list:
            if subcategory not in category_obj._subcategories:
                category_obj._subcategories[subcategory] = Category(subcategory)
            category_obj = category_obj._subcategories[subcategory]
        category_obj._items.append(item)

    def remove(self, item: 'Item', category_list: 'List') -> None:
        category_obj = self  # type: Category
        for subcategory in category_list:
            category_obj = category_obj._subcategories[subcategory]
        category_obj._items.remove(item)


class Item(object):
    All = dict()
    Category = Category("All")

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

        name = json_data.pop("name", "")
        return Item(key, type_, name, **json_data)

    def __init__(self, key: str, type_: int, name: str, **kwargs) -> None:
        self._key = key
        self._type = type_
        self._name = name
        self._weight = float(kwargs.pop("weight", 0.001))  # type: float
        self._value = kwargs.pop("value", Money())  # type: Money
        self._desc = str(kwargs.pop("description", ""))  # type: str
        self._source = str(kwargs.pop("source", ""))  # type: str

        # These are derived from the key
        self._categories = self._key.split('.')
        self._short_key = self._categories.pop()
        
        if len(kwargs.keys()) > 0:
            raise KeyError("Unknown keyword arguments: {}".format(", ".join(kwargs.keys())))

    def register(self, replace: bool = False) -> 'Tuple[bool, Optional[str]]':
        err_str = None
        if self._key in Item.All:
            err_str = "Item with key={} already exists in Item.All".format(self._key)
            if not replace:
                return False, err_str
            raise NotImplementedError("Item Replacement not implemented")
        Item.All[self._key] = self
        return True, err_str

    def key(self, full: bool = True) -> str:
        return self._key if full else self._short_key

    def type(self) -> int:
        return self._type

    def name(self) -> str:
        return self._name

    def value(self) -> 'Money':
        return self._value

    def description(self) -> str:
        return self._desc

    def categories(self) -> 'List[str]':
        return self._categories
