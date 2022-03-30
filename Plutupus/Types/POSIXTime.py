import json

class POSIXTime(object):

    def __init__(self, time):
        self.__time = time

    def get(self):
        return self.__time

    def json(self):
        return json.dumps({
            "int": self.__time
        })
    
    @staticmethod
    def days_in_ms(days):
        return days * 86400000

    @staticmethod
    def from_json(_json):
        return POSIXTime(_json["int"])

    def __eq__(self, other):
        if type(other) is POSIXTime:
            return self.get() == other.get()
        else:
            return False