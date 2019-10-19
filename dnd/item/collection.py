
from dnd.item import category

import typing
if typing.TYPE_CHECKING:
    from typing import Dict, Optional, Tuple
    from dnd.item.item import Item
    from dnd.item.category import Category


class Collection(object):
    def __init__(self) -> None:
        self._root_category = category.Category("All")
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
