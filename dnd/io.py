
import json
import dnd.item as _item


def load_file(filename: str):
    data = json.load(open(filename, "rb"))
    items = data.pop("items", None)
    if items is not None:
        if type(items) is not list:
            print("base-level items collection expected list, got {}".format(type(items)))
        for index, item_data in enumerate(items):
            try:
                item = _item.Item.from_json(item_data)
                status, err_msg = item.register(False)
                if not status:
                    print("Error while registering item {}: {}".format(index, err_msg))
            except Exception as e:
                print("{} while parsing item {}: {}".format(type(e), index, str(e)))
