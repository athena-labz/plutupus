import copy
import json

from Plutupus.Types.AssetClass import AssetClass
from Plutupus.Types.CurrencySymbol import CurrencySymbol
from Plutupus.Types.TokenName import TokenName
from Plutupus.Types.AssocMap import AssocMap
from Plutupus.Types.Integer import Integer


class Value(object):

    def __init__(self):
        self.value = {}

    def __remove_empties(self):
        untouchable = copy.deepcopy(self.value)
        for asset, amount in untouchable.items():
            if amount == 0:
                del self.value[asset]

    def add_value(self, value):
        for asset, amount in value.value.items():
            self.add_token_amount(asset, amount)

    def subtract_value(self, value):
        for asset, amount in value.value.items():
            self.subtract_token_amount(asset, amount)

    def add_token_amount(self, asset, amount):
        if asset in self.value:
            self.value[asset] += amount
        else:
            self.value[asset] = amount

        self.__remove_empties()

    def subtract_token_amount(self, asset, amount):
        if asset in self.value:
            self.value[asset] -= amount
        else:
            self.value[asset] = -amount

        self.__remove_empties()

    def get(self):
        result = {}
        for asset, amount in self.value.items():
            result[asset] = amount

        return result

    def json(self):
        value = {}

        for asset, amount in self.value.items():
            asset_class = AssetClass.from_parsed_value(asset)
            currency_symbol = asset_class.get_currency_symbol()
            token_name = asset_class.get_token_name()

            if currency_symbol.get() not in value:
                value[currency_symbol.get()] = AssocMap()

            value[currency_symbol.get()].update(token_name, Integer(amount))

        result_map = AssocMap()
        for currency_symbol, assoc_map in value.items():
            result_map.update(CurrencySymbol(currency_symbol), assoc_map)

        return result_map.json()

    def __repr__(self):
        return "<Value " + json.dumps(self.get()) + ">"

    @staticmethod
    def from_dictionary(value_dict):
        value = Value()
        value.value = value_dict

        return value

    @staticmethod
    def from_plutus_like_dictionary(value_dict):
        value = Value()
        for currency, token_or_amount in value_dict.items():
            if currency == "lovelace":
                amount = token_or_amount
                value.add_token_amount("lovelace", amount)
            else:
                token = token_or_amount
                for name, amount in token.items():
                    if currency == "" and name == "":
                        value.add_token_amount("lovelace", amount)
                    else:
                        value.add_token_amount(f"{currency}.{name}", amount)

        return value
    
    @staticmethod
    def lovelace(amount):
        value = Value()
        value.add_token_amount("lovelace", amount)
        
        return value

    @staticmethod
    def add_values(value_1, value_2):
        value = copy.deepcopy(value_1)
        value.add_value(value_2)

        return value

    @staticmethod
    def subtract_values(value_1, value_2):
        value = copy.deepcopy(value_1)
        value.subtract_value(value_2)

        return value

    @staticmethod
    def equal(value_1, value_2):
        subtraction = Value.subtract_values(value_1, value_2)

        return subtraction.get() == {}

    @staticmethod
    def greater(value_1, value_2):
        # Is value_1 greater than value_2?

        subtraction = Value.subtract_values(value_1, value_2)

        if len(subtraction.get().values()) == 0:
            return False
        else:
            for amount in subtraction.get().values():
                if amount <= 0:
                    return False

        return True

    @staticmethod
    def greater_or_equal(value_1, value_2):
        return Value.greater(value_1, value_2) or Value.equal(value_1, value_2)

    @staticmethod
    def less(value_1, value_2):
        # Is value_1 less than value_2?

        subtraction = Value.subtract_values(value_1, value_2)

        if len(subtraction.get().values()) == 0:
            return False
        else:
            for amount in subtraction.get().values():
                if amount >= 0:
                    return False

        return True

    @staticmethod
    def less_or_equal(value_1, value_2):
        return Value.less(value_1, value_2) or Value.equal(value_1, value_2)

    @staticmethod
    def from_json(_json):

        assoc_map = AssocMap.from_json(
            _json,
            {"name": "currency_symbol", "type": CurrencySymbol},
            {
                "name": "assoc_map",
                "type": AssocMap,
                "extra_key": {"name": "token_name", "type": TokenName},
                "extra_value": {"name": "integer", "type": Integer}
            },
        )

        return Value.from_plutus_like_dictionary(assoc_map.get())

    def __eq__(self, other):
        if type(other) is Value:
            return self.get() == other.get()
        else:
            return False