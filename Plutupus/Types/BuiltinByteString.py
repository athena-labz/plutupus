import json

from Plutupus.Types.utils import token_to_hex


class BuiltinByteString(object):

    def __init__(self, string):
        self.__string = string
        self.hexify = True

    def get(self):
        return self.__string

    def json(self):
        if self.hexify:
            return json.dumps({
                "bytes": token_to_hex(self.__string)
            })
        else:
            return json.dumps({
                "bytes": self.__string
            })

    @staticmethod
    def from_hex(_hex):
        bbs = BuiltinByteString(_hex)
        bbs.hexify = False

        return bbs

    @staticmethod
    def from_json(_json):
        return BuiltinByteString.from_hex(_json["bytes"])

    def __eq__(self, other):
        if type(other) is BuiltinByteString:
            return self.get() == other.get()
        else:
            return False