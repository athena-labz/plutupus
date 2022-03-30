import json

class PTuple(object):  # Plutus Tuple

    def __init__(self, *elements):
        self.__elements = elements

    def get(self):
        return {
            "tuple": [
                {
                    "type": type(element).__name__,
                    "value": element.get()
                } for element in self.__elements
            ]
        }

    def json(self):
        return json.dumps({
            "constructor": 0,
            "fields": [json.loads(element.json()) for element in self.__elements]
        })

    def __eq__(self, other):
        if type(other) is PTuple:
            return self.get() == other.get()
        else:
            return False