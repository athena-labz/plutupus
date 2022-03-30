import json

class PubKeyHash(object):

    def __init__(self, pkh):
        if not isinstance(pkh, str):
            raise Exception(
                f"PubKeyHash contructor argument, must be string - {pkh}")

        self.__pkh = pkh

    def get(self):
        return self.__pkh

    def json(self):
        return json.dumps({
            "bytes": self.__pkh
        })

    @staticmethod
    def from_json(_json):
        return PubKeyHash(_json["bytes"])

    def __eq__(self, other):
        if type(other) is PubKeyHash:
            return self.get() == other.get()
        else:
            return False