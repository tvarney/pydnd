
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Optional, Tuple, Union


def parse_coin_spec(data: str) -> 'Tuple[int, int, int, int]':
    """Parses a string into a set of coin values.

    This function is used by the Money type to parse and initialize a
    Money value from a string. The spec must consist of pairs of values
    where each pair consists of a numeric value and a coin spec. Valid
    coin specs are 'cp', 'sp', 'gp', and 'pp'. The numeric value must
    be the first item of each pair. If any of these constraints are
    violated, a ValueError is raised. A coin spec may be used multiple
    times, but this is not recommended.

    The value returned is not normalized at all - giving this function
    the string "10000 cp" will return (10000, 0, 0, 0).

    :param data: The coin spec to parse.
    :return: A tuple of the form [cp, sp, gp, pp]
    """
    cp, sp, gp, pp = 0, 0, 0, 0
    parsed, idx = 0, 0
    speclen = len(data)


class Money(object):
    """Money is the value object for Items.

    Money values on items are split into 4 coin types - pp, gp, sp, and
    cp. These stand for, respectively:
      * platinum pieces
      * gold pieces
      * silver pieces
      * copper pieces

    The Money type ensures that a value is always valid, and always
    normalized - that is, the value for gp, sp, and cp stay under the
    maximal value prior to converting. Money types may not be negative,
    if an operation would set one of the values to be negative, then it
    will 'borrow' from the value higher than it in the hierarchy. If it
    is unable to do that (i.e. the highest value, pp, would be set to a
    negative value), a ValueError is raised.
    """
    def __init__(self, data: 'Union[Dict, str, int, float, None]') -> None:
        """Create a Money value with the given data.

        If the data value is a dictionary, it is unpacked as is into
        the resulting Money value. If there are keys in this dictionary
        which are not one of ['cp', 'sp', 'gp', 'pp'], then a KeyError
        is raised.

        If the data value is a numeric type (int or float), then it the
        value is multiplied by 100 and the cp type is set to that
        value, which should cascade the value up into higher types.
        Fractional cp values are truncated, though any negative value
        will result in a ValueError.

        If the data value is a string, that string will be parsed. The
        string must consist of pairs of values followed by a coin type.
        See the parse_coin_spec() function for more information.

        :param data: The data to unpack into a Money value.
        """
        self._cp, self._sp, self._gp, self._pp = 0, 0, 0, 0
        if data is None:
            return

        if type(data) == dict:
            self.pp = int(data.pop('pp', 0))
            self.gp = int(data.pop('gp', 0))
            self.sp = int(data.pop('sp', 0))
            self.cp = int(data.pop('cp', 0))
            if len(data.keys()) > 0:
                raise KeyError("Unknown keyword arguments: {}".format(", ".join(data.keys())))
        elif type(data) == str:
            raise NotImplementedError("Money(str) not implemented")
        elif type(data) == int or type(data) == float:
            if data < 0:
                raise ValueError("Money value may not be negative")
            self.cp = int(data * 100)
        else:
            raise ValueError("Money must be initialized with a dictionary, string, or number")

    @property
    def cp(self) -> int:
        return self._cp

    @cp.setter
    def cp(self, value: int) -> None:
        if value < 0:
            value = -value
            # Attempt to borrow from the next highest
            self.sp -= (value // 100) + 1
            remainder = value % 100
            if remainder > 0:
                self._cp = 100 - remainder
            else:
                self._cp = 0
            return

        self._cp = int(value)
        if self._cp > 100:
            self.sp += int(self._cp // 100)
            self._cp %= 100

    @property
    def sp(self) -> int:
        return self._sp

    @sp.setter
    def sp(self, value: int) -> None:
        if value < 0:
            value = -value
            # Attempt to borrow from the next highest
            self.gp -= (value // 100) + 1
            remainder = value % 100
            if remainder > 0:
                self._sp = 100 - remainder
            else:
                self._sp = 0
            return

        self._sp = int(value)
        if self._sp > 100:
            self.gp += int(self._sp // 100)
            self._sp %= 100

    @property
    def gp(self) -> int:
        return self._gp

    @gp.setter
    def gp(self, value: int) -> None:
        if value < 0:
            value = -value
            # Attempt to borrow from the next highest
            self.pp -= (value // 100) + 1
            remainder = value % 100
            if remainder > 0:
                self._gp = 100 - remainder
            else:
                self._gp = 0
            return

        self._gp = int(value)
        if self._gp > 100:
            self.pp += int(self._gp // 100)
            self._gp %= 100

    @property
    def pp(self) -> int:
        return self._pp

    @pp.setter
    def pp(self, value: int) -> None:
        if value < 0:
            raise ValueError("money value may not be negative")
        self._pp = int(value)

    @property
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
        return "Money({{{}}})".format(", ".join(parts))


class Category(object):
    def __init__(self, name: str):
        self._name = name             # type: str
        self._subcategories = dict()  # type: Dict[str, Category]
        self._items = list()          # type: List[Item]

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
            value = Money(None)
        else:
            value = Money(value)

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
