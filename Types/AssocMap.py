import json

class AssocMap(object):

    def __init__(self):
        self.__items = []

    def get(self):
        result = {}

        for item in self.__items:
            result[item["key"].get()] = item["value"].get()

        return result

    def update(self, key, value):
        for item in self.__items:
            if item["key"] == key:
                item["value"] = value
                return

        self.__items.append({
            "key": key,
            "value": value
        })

    def remove(self, key):
        del self.__items[self.__items.index(key)]

    def json(self):
        return json.dumps({
            "map": [
                {
                    "v": json.loads(item["value"].json()),
                    "k": json.loads(item["key"].json())
                } for item in self.__items
            ]
        })

    @staticmethod
    def from_json(_json, key, value):

        result = AssocMap()
        for item in _json["map"]:
            if key["name"] == "assoc_map":
                key_json = key["type"].from_json(
                    item["k"], key["extra_key"], key["extra_value"])
            else:
                key_json = key["type"].from_json(item["k"])

            if value["name"] == "assoc_map":
                value_json = value["type"].from_json(
                    item["v"], value["extra_key"], value["extra_value"])
            else:
                value_json = value["type"].from_json(item["v"])

            result.update(key_json, value_json)

        return result

    def __eq__(self, other):
        if type(other) is AssocMap:
            return self.get() == other.get()
        else:
            return False