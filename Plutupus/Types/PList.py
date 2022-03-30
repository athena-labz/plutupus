import json

class PList(object):

    def __init__(self, lst):
        self.__lst = lst

    def insert(self, idx, element):
        self.__lst.insert(idx, element)

    def append(self, element):
        self.__lst.append(element)
        
    def remove(self, idx):
        del self.__lst[idx]
        
    def element(self, idx):
        return self.__lst[idx]

    def get(self):
        return [element.get() for element in self.__lst]

    def json(self):
        return json.dumps({
            "list": [json.loads(element.json()) for element in self.__lst]
        })

    @staticmethod
    def from_json(_json, type):
        return PList([type["type"].from_json(i) for i in _json["list"]])

    def __eq__(self, other):
        if type(other) is PList:
            return self.get() == other.get()
        else:
            return False