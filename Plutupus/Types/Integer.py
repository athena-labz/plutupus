import json

class Integer(object):

    def __init__(self, num):
        self.__num = num

    def get(self):
        return self.__num

    def json(self):
        return json.dumps({
            "int": self.__num
        })

    @staticmethod
    def from_json(_json):
        return Integer(_json["int"])

    def __eq__(self, other):
        if type(other) is Integer:
            return self.get() == other.get()
        else:
            return False