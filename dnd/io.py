
import json

import dnd.item as _item

import typing
if typing.TYPE_CHECKING:
    from typing import Optional


class FileData(object):
    def __init__(self) -> None:
        self._log = None
        self.items = _item.ItemCollection()

    def log(self, message) -> None:
        if self._log is not None:
            self._log.append(message)
        else:
            print(message)

    def items(self) -> _item.ItemCollection:
        return self.items

    def load_filename(self, filename: str) -> None:
        with open(filename, "rb") as fp:
            data = json.load(fp)
            items = data.pop("items", None)
            if items is not None:
                if type(items) is not list:
                    self.log("base-level items collection expected list, got {}".format(type(items)))
                else:
                    for index, item_data in enumerate(items):
                        try:
                            item = _item.Item.from_json(item_data)
                            status, err_msg = self.items.register(item, False)
                            if not status:
                                self.log("Error while registering item {}: {}".format(index, err_msg))
                        except Exception as e:
                            self.log("{} while parsing item {}: {}".format(type(e), index, str(e)))


class Scanner(object):
    def __init__(self, data: str) -> None:
        self._data = data
        self._len = len(data)
        self._idx = 0

    def discard_spaces(self) -> None:
        while self._idx < self._len and self._data[self._idx].isspace():
            self._idx += 1

    def next_token(self) -> 'Optional[str]':
        self.discard_spaces()
        if self._idx >= self._len:
            return None

        start = self._idx
        while self._idx < self._len and not self._data[self._idx].isspace():
            self._idx += 1

        return self._data[start:self._idx]

    def next_int(self, require_space: bool = True):
        self.discard_spaces()
        start = self._idx

        # TODO: This

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def current_char(self) -> 'Optional[str]':
        if self._idx >= self._len:
            return None
        return self._data[self._idx]

