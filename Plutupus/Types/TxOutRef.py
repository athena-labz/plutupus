import json

class TxOutRef(object):

    def __init__(self, tx_id, tx_ix):
        self.tx_id = tx_id
        self.tx_ix = tx_ix

    def get(self):
        return f"{self.tx_id}#{str(self.tx_ix)}"

    def json(self):
        return json.dumps({
            "constructor": 0,
            "fields": [
                {
                    "constructor": 0,
                    "fields": [
                        {
                            "bytes": self.tx_id
                        }
                    ]
                },
                {
                    "int": int(self.tx_ix)
                }
            ]
        })

    def __eq__(self, other):
        if type(other) is TxOutRef:
            return self.get() == other.get()
        else:
            return False