import json

from Types.TokenName import TokenName
from Types.CurrencySymbol import CurrencySymbol


class AssetClass(object):

    def __init__(self, currency_symbol, token_name):
        self.__currency_symbol = currency_symbol
        self.__token_name = token_name

    def get(self):
        if self.__currency_symbol.get() == "" and self.__token_name.get() == "":
            return "lovelace"
        else:
            return f"{self.__currency_symbol.get()}.{self.__token_name.get()}"

    def get_currency_symbol(self):
        return self.__currency_symbol

    def get_token_name(self):
        return self.__token_name

    def json(self):
        return json.dumps({
            "constructor": 0,
            "fields": [
                json.loads(self.__currency_symbol.json()),
                json.loads(self.__token_name.json())
            ]
        })

    @staticmethod
    def from_raw_values(currency_symbol, token_name):
        cs_obj = CurrencySymbol(currency_symbol)
        tn_obj = TokenName(token_name, hexify=False)

        return AssetClass(cs_obj, tn_obj)

    @staticmethod
    def from_parsed_value(parsed):
        if parsed == "lovelace":
            return AssetClass.lovelace()

        currency_symbol, token_name = ".".split(parsed)

        cs_obj = CurrencySymbol(currency_symbol)
        tn_obj = TokenName(token_name, hexify=False)

        return AssetClass(cs_obj, tn_obj)

    @staticmethod
    def lovelace():
        cs_obj = CurrencySymbol("")
        tn_obj = TokenName("", hexify=False)

        return AssetClass(cs_obj, tn_obj)

    @staticmethod
    def from_json(_json):
        return AssetClass(
            CurrencySymbol.from_json(_json["fields"][0]),
            TokenName.from_json(_json["fields"][1])
        )

    def __eq__(self, other):
        if type(other) is AssetClass:
            return self.get() == other.get()
        else:
            return False