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
            result["fields"].append(value.json())

        return result

    @staticmethod
    def from_json(_json: dict[str, Any]):
        raise NotImplementedError()
        # if "fields" not in _json or not len(_json["fields"]) or \
        #     "fields" not in _json["fields"][0] or \
        #         not len(_json["fields"][0]["fields"]):
        #     raise ValueError(
        #         "JSON received does not conform to plutus spec or is not a pubkeyhash")

        # pkh_bytes = _json["fields"][0]["fields"][0]
        # return Address(PubKeyHash.from_json(_json["fields"][0]["fields"][0]))

    def __eq__(self, other):
        if isinstance(other, Abstract):
            return type(self) == type(other) and self.get() == other.get()
        else:
            return False
