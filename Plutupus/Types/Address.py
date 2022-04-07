import json

from Plutupus.Types.PubKeyHash import PubKeyHash


class Address(object):

    def __init__(self, _hash):
        if type(_hash) is not PubKeyHash:
            raise ValueError(f"Argument {_hash} not of type PubKeyHash")

        # TODO: Add staking credential
        self.hash = _hash

    def get(self):
        return {
            "pubkeyhash": self.hash.get(),
            "staking_credentials": None
        }

    def json(self):
        return json.dumps({
            "constructor": 0,
            "fields": [
                {
                    "constructor": 0,
                    "fields": [json.loads(self.hash.json())]
                },
                {
                    "constructor": 1,
                    "fields": []
                }
            ]
        })

    @staticmethod
    def from_json(_json):
        if "fields" not in _json or not len(_json["fields"]) or \
            "fields" not in _json["fields"][0] or \
                not len(_json["fields"][0]["fields"]):
            raise ValueError(
                "JSON received does not conform to plutus spec or is not a pubkeyhash")

        pkh_bytes = _json["fields"][0]["fields"][0]
        return Address(PubKeyHash.from_json(_json["fields"][0]["fields"][0]))

    def __eq__(self, other):
        if type(other) is Address:
            return self.get() == other.get()
        else:
            return False
