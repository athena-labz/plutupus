from __future__ import annotations

import json

from Plutupus.Types import Abstract
from Plutupus.Types import utils


class BaseBytes(Abstract):

    def __init__(self, string: str):
        super().__init__()

        self._string = string

    def get(self) -> str:
        return self._string

    def json(self) -> dict[str, str]:
        return json.dumps({
            "bytes": self._string
        })

    def __hash__(self) -> int:
        return hash(self.get())

    @staticmethod
    def from_json(_json: dict[str, str]) -> BaseBytes:
        if not "bytes" in _json:
            raise ValueError("Cannot create BaseBytes object: invalid JSON!")

        return BaseBytes(_json["bytes"])

    @staticmethod
    def to_hex(string):
        return utils.token_to_hex(string)


class BaseInteger(Abstract):

    def __init__(self, num: int):
        super().__init__()

        self._num = num

    def get(self):
        return self._num

    def json(self):
        return json.dumps({
            "int": self._num
        })

    def __hash__(self) -> int:
        return hash(self.get())

    @staticmethod
    def from_json(_json: dict[str, int]):
        if not "int" in _json:
            raise ValueError("Cannot create BaseInteger object: invalid JSON!")

        return BaseInteger(_json["int"])


class BaseList(Abstract):
    def __init__(self, lst: list[Abstract]):
        super().__init__()

        self._lst = lst

    def get(self):
        return [i.get() for i in self._lst]

    def json(self):
        return json.dumps({
            "list": [json.loads(i.json()) for i in self._lst]
        })

    @staticmethod
    def from_json(_type: Abstract, _json: dict[str, list]):
        if not "list" in _json:
            raise ValueError("Cannot create BaseList object: invalid JSON!")

        return BaseList([_type.from_json(i) for i in _json["list"]])


class BaseMap(Abstract):
    def __init__(self, dct: dict[Abstract, Abstract]):
        super().__init__()

        key_type, value_type = (None, None)
        first = True

        # Make sure our keys and values are from type Abstract
        # Make sure all keys have same type and all values has same type
        for key, value in dct.items():
            if not isinstance(key, Abstract):
                raise ValueError(
                    f"Invalid type for BaseMap key: must be instance of Abstract")

            if not isinstance(value, Abstract):
                raise ValueError(
                    f"Invalid type for BaseMap value: must be instance of Abstract")

            cur_key_type, cur_value_type = type(key), type(value)

            if first is False and (cur_key_type != key_type or value_type != cur_value_type):
                raise ValueError(
                    "BaseMap must have same key and value types for all fields")

            key_type, value_type = cur_key_type, cur_value_type
            first = False

        self._dct = dct
        self.key_type, self.value_type = key_type, value_type

    def add(self, key: Abstract, value: Abstract):
        if self.key_type is not None and type(key) != self.key_type:
            raise ValueError(
                f"Received key type does not match expected map key type!")

        if self.value_type is not None and type(value) != self.value_type:
            raise ValueError(
                f"Received value type does not match expected map value type!")
        
        self._dct[key] = value

    def remove(self, key: Abstract):
        del self._dct[key]

    def get(self):
        return {key.get(): value.get() for key, value in self._dct.items()}

    def json(self):
        return json.dumps({
            "map": [
                {
                    "v": json.loads(value.json()),
                    "k": json.loads(key.json())
                } for key, value in self._dct.items()
            ]
        })

    @staticmethod
    def from_json(key_type: Abstract, value_type: Abstract, _json: dict[str, list]):
        if not "map" in _json:
            raise ValueError("Cannot create BaseMap object: invalid JSON!")

        return BaseMap({
            key_type.from_json(field["k"]): value_type.from_json(field["v"])
            for field in _json["map"]
        })
