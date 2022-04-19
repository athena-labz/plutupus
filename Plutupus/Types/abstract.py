from __future__ import annotations

import json
from typing import Any


class Abstract(object):

    def __init__(self):
        self.properties: dict[str, Abstract] = {}

    def get(self):
        result = {}

        for name, value in self.properties.items():
            result[name] = value.get()

        return result

    def json(self):
        result = {
            "constructor": 0,
            "fields": []
        }

        for name, value in self.properties.items():
            result["fields"].append(json.loads(value.json()))

        return result

    @staticmethod
    def from_json(_json: dict[str, Any]):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Abstract):
            return type(self) == type(other) and self.get() == other.get()
        else:
            return False
