
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Optional, Tuple, Union


class Money(object):
    @staticmethod
    def from_json(json_data: 'Dict'):
        if type(json_data) == dict:
            return Money(**json_data)
        if type(json_data) == str:
            raise NotImplementedError("Value string parsing not implemented")
        if type(json_data) == int or type(json_data) == float:
            raise NotImplementedError("Value numeric parsing not implemented")

    def __init__(self, **kwargs) -> None:
        self._pp = int(kwargs.pop('pp', 0))
        self._gp = int(kwargs.pop('gp', 0))
        self._sp = int(kwargs.pop('sp', 0))
        self._cp = int(kwargs.pop('cp', 0))

        if len(kwargs.keys()) > 0:
            raise KeyError("Unknown keyword arguments: {}".format(", ".join(kwargs.keys())))

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

    def to_json(self) -> 'Dict':
        d = dict()
        if self._pp != 0:
            d["pp"] = self._pp
        if self._gp != 0:
            d["gp"] = self._gp
        if self._sp != 0:
            d["sp"] = self._sp
        if self._cp != 0:
            d["cp"] = self._cp
        return d

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

    def items(self) -> 'List[Item]':
        return self._items

    def subcategories(self) -> 'Dict[str, Category]':
        return self._subcategories

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

    def build_str(self, space: str = "", details: bool = False) -> str:
        tab = space + "  "
        parts = ["{}{}:".format(space, self._name)]
        if len(self._items) > 0:
            if details:
                fmt_str = "{}{} - {}, {} lbs"
                parts.append("\n".join([fmt_str.format(tab, i.name(), i.value(), i.weight()) for i in self._items]))
            else:
                parts.append("\n".join(list("{}{}".format(tab, i.name()) for i in self._items)))
        if len(self._subcategories.keys()):
            parts.append("\n".join([c.build_str(tab, details) for c in self._subcategories.values()]))
        return "\n".join(parts)

    def __str__(self) -> str:
        return self.build_str("", False)

    def __getitem__(self, key: 'str') -> 'Category':
        return self._subcategories.__getitem__(key)


class ItemCollection(object):
    def __init__(self) -> None:
        self._root_category = Category("All")
        self._all_items = dict()  # type: Dict[str, Item]

    def category(self) -> 'Category':
        return self._root_category

    def all(self) -> 'Dict[str, Item]':
        return self._all_items

    def register(self, item: 'Item', replace: bool = False) -> 'Tuple[bool, Optional[str]]':
        err_str = None
        if item.key() in self._all_items:
            err_str = "Item with key={} already exists in Item.All".format(item.key())
            if not replace:
                return False, err_str
            raise NotImplementedError("Item Replacement not implemented")
        self._all_items[item.key()] = self
        self._root_category.add(item, item.categories())
        return True, err_str


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

        value = json_data.pop("value", None)
        if value is None:
            value = Money()
        else:
            value = Money.from_json(value)

        name = json_data.pop("name", "")
        return Item(key, type_, name, value=value, **json_data)

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

    def key(self, full: bool = True) -> str:
        return self._key if full else self._short_key

    def type(self) -> int:
        return self._type

    def name(self) -> str:
        return self._name

    def weight(self) -> float:
        return self._weight

    def value(self) -> 'Money':
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
        d["value"] = self._value.to_json()
        if self._desc != "":
            d["desc"] = self._desc
        if self._source != "":
            d["source"] = self._source
        return d
