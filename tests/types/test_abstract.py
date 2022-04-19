# There are four base abstracts
#   byte
#   number
#   list
#   map
#   void

# Abstracts have a "poperties" property (lol),
#   a map matching property names to other abstracts
# The base abstracts have "properties" empty

# abstracts will have a "properties" property
# each property should be another abstract

from Plutupus.Types.abstract import Abstract
from Plutupus.Types.base_types import BaseBytes, BaseInteger, BaseList, BaseMap


def test_abstract():

    abstract = Abstract()
    abstract.properties = {
        "field1": BaseBytes("field1"),
        "field2": BaseInteger(2),
        "field3": BaseList([BaseBytes("field"), BaseInteger(3)]),
        "field4": BaseMap({BaseBytes("field"): BaseInteger(4)}),
    }

    assert abstract.get() == {
        "field1": "field1",
        "field2": 2,
        "field3": ["field", 3],
        "field4": {
            "field": 4
        }
    }

    assert abstract.json() == {
        "constructor": 0,
        "fields": [{
            "bytes": "field1"
        }, {
            "int": 2
        }, {
            "list": [{
                "bytes": "field"
            }, {
                "int": 3
            }]
        }, {
            "map": [
                {"v": {"int": 4}, "k": {"bytes": "field"}}
            ]
        }]
    }