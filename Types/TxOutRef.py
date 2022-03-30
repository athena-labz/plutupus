import json

class TxOutRef(object):

    def __init__(self, tx_id, tx_ix):
        self.__tx_id = tx_id
        self.__tx_ix = tx_ix

    def get(self):
        return f"{self.__tx_id}#{str(self.__tx_ix)}"

    def json(self):
        return json.dumps({
            "constructor": 0,
            "fields": [
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "bytes": self.__tx_id
                        }
                    ]
                },
                {
                    "int": int(self.__tx_ix)
                }
            ]
        })

    def __eq__(self, other):
        if type(other) is TxOutRef:
            return self.get() == other.get()
        else:
            return False