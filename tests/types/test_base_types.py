import json

import pytest

from Plutupus.Types import BaseBytes
from Plutupus.Types import BaseInteger
from Plutupus.Types import BaseList
from Plutupus.Types import BaseMap

from Plutupus.Types import BuiltinByteString


def test_byte():
    byte = BaseBytes("hello there")

    assert byte.get() == "hello there"

    # json
    assert byte.json() == json.dumps({"bytes": "hello there"})

    # helper method to convert string to hex (useful for token names)
    assert BaseBytes.to_hex("hello there") == "68656C6C6F207468657265"

    # assert object equality works
    assert BaseBytes("hello there") == BaseBytes("hello there")
    assert BaseBytes("hello there") != BaseBytes("hello world")
    assert BaseBytes("hello there") != BuiltinByteString("hello there")

    with pytest.raises(ValueError):
        BaseBytes.from_json({"int": 7})

    assert BaseBytes.from_json({
        "bytes": "hello there"
    }) == byte


def test_integer():
    bint = BaseInteger(7)

    assert bint.get() == 7

    # json
    assert bint.json() == json.dumps({"int": 7})

    # assert object equality works
    assert BaseInteger(7) == BaseInteger(7)
    assert BaseInteger(7) != BaseInteger(11)

    with pytest.raises(ValueError):
        BaseInteger.from_json({"bytes": 7})

    assert BaseInteger.from_json({"int": 7}) == bint


def test_list():
    blist = BaseList([BaseInteger(7)])

    assert blist.get() == [7]

    # json
    assert blist.json() == json.dumps({
        "list": [{"int": 7}]
    })

    # assert object equality works
    assert BaseList([BaseInteger(7)]) == BaseList([BaseInteger(7)])
    assert BaseList([BaseInteger(7)]) != BaseList([BaseInteger(11)])
    assert BaseList([BaseInteger(7)]) != BaseList(
        [BaseInteger(7), BaseInteger(11)])
    assert BaseList([BaseInteger(7)]) != BaseInteger(7)

    with pytest.raises(ValueError):
        BaseList.from_json(BaseInteger, {"int": 7})

    assert BaseList.from_json(BaseInteger, {"list": [{"int": 7}]}) == blist


def test_map():
    bmap = BaseMap({
        BaseBytes("hello"): BaseInteger(42),
        BaseBytes("prime"): BaseInteger(97),
    })

    assert bmap.get() == {
        "hello": 42,
        "prime": 97
    }

    # json
    assert bmap.json() == json.dumps({
        "map": [
            {"v": {"int": 42}, "k": {"bytes": "hello"}},
            {"v": {"int": 97}, "k": {"bytes": "prime"}}
        ]
    })

    # assert object equality works
    assert BaseMap({BaseBytes("hello"): BaseBytes("there")}) == BaseMap(
        {BaseBytes("hello"): BaseBytes("there")})
    assert BaseMap({
        BaseBytes("hello"): BaseBytes("there"),
        BaseBytes("bounjour"): BaseBytes("world")
    }) == BaseMap({
        BaseBytes("bounjour"): BaseBytes("world"),
        BaseBytes("hello"): BaseBytes("there"),
    })
    assert BaseMap({BaseBytes("hello"): BaseBytes("there")}) != BaseMap(
        {BaseBytes("hello"): BaseBytes("world")})
    assert BaseMap({}) != BaseMap(
        {BaseBytes("bounjour"): BaseBytes("monsieur")})
    assert BaseMap({}) != BaseInteger(7)

    with pytest.raises(ValueError):
        BaseMap.from_json(BaseBytes, BaseInteger, {
            "map": [{"v": {"int": 42}, "k": {"int": 33}}]
        })

    assert BaseMap.from_json(BaseBytes, BaseInteger, {
        "map": [
            {"v": {"int": 42}, "k": {"bytes": "hello"}},
            {"v": {"int": 97}, "k": {"bytes": "prime"}}
        ]
    }) == bmap

    bm = BaseMap({BaseBytes("hello"): BaseBytes("there")})
    bm.add(BaseBytes("bonjour"), BaseBytes("monsieur"))

    assert bm == BaseMap({
        BaseBytes("hello"): BaseBytes("there"),
        BaseBytes("bonjour"): BaseBytes("monsieur")
    })

    bm.remove(BaseBytes("hello"))

    assert bm == BaseMap({BaseBytes("bonjour"): BaseBytes("monsieur")})
