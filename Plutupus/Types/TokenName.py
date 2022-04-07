import json

from Plutupus.Types.utils import token_to_hex


class TokenName(object):

    def __init__(self, token_name, hexify=True):
        self.__token_name = token_name
        self.__hex = hexify

    def get(self):
        if self.__hex:
            return token_to_hex(self.__token_name)
        else:
            return self.__token_name

    def json(self):
        if self.__hex:
            return json.dumps({
                "bytes": token_to_hex(self.__token_name)
            })
        else:
            return json.dumps({
                "bytes": self.__token_name
            })

    @staticmethod
    def from_json(_json):
        return TokenName(_json["bytes"], hexify=False)

    def __eq__(self, other):
        if type(other) is TokenName:
            return self.get() == other.get()
        else:
            return False