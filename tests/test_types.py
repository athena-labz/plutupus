import json
import pytest
import Types


def test_address_success():
    address = Types.Address(Types.PubKeyHash("<pubkeyhash>"))

    assert address.get() == {
        "pubkeyhash": "<pubkeyhash>",
        "staking_credentials": None
    }

    assert address.json() == json.dumps({
        "constructor": 0,
        "fields": [
            {
                "constructor": 0,
                "fields": [{
                    "bytes": "<pubkeyhash>"
                }]
            },
            {
                "constructor": 1,
                "fields": []
            }
        ]
    })

    assert Types.Address.from_json({
        "constructor": 0,
        "fields": [
            {
                "constructor": 0,
                "fields": [{
                    "bytes": "<pubkeyhash>"
                }]
            },
            {
                "constructor": 1,
                "fields": []
            }
        ]
    }) == address


def test_address_failure():
    with pytest.raises(ValueError):
        Types.Address("<pubkeyhash>")

    with pytest.raises(ValueError):
        Types.Address(37)

    with pytest.raises(ValueError):
        Types.Address.from_json({
            "constructor": 0,
            "fields": [
                {
                    "constructor": 1,
                    "fields": []
                }
            ]
        })

# TODO: Add other tests