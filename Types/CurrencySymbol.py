import json

class CurrencySymbol(object):

    def __init__(self, currency_symbol):
        self.__currency_symbol = currency_symbol

    def get(self):
        return self.__currency_symbol

    def json(self):
        return json.dumps({
            "bytes": self.__currency_symbol
        })

    @staticmethod
    def from_json(_json):
        return CurrencySymbol(_json["bytes"])

    def __eq__(self, other):
        if type(other) is CurrencySymbol:
            return self.get() == other.get()
        else:
            return False