
import json

import dnd.item as item


class FileData(object):
    def __init__(self) -> None:
        self._log = None
        self.items = item.ItemCollection()

    def log(self, message) -> None:
        if self._log is not None:
            self._log.append(message)
        else:
            print(message)

    def items(self) -> item.ItemCollection:
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
                            i = item.Item.from_json(item_data)
                            status, err_msg = self.items.register(i, False)
                            if not status:
                                self.log("Error while registering item {}: {}".format(index, err_msg))
                        except Exception as e:
                            self.log("{} while parsing item {}: {}".format(type(e), index, str(e)))
