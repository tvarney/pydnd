
import typing
if typing.TYPE_CHECKING:
    from typing import Dict, List
    from dnd.item.item import Item


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
