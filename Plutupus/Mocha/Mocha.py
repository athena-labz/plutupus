from __future__ import annotations

import secrets
import copy

from Plutupus.TxBody import TxBody
from Plutupus.Types.Value import Value


class MochaError(Exception):
    pass


class Mocha(object):

    def __init__(self, initial_utxos: dict, fees: int):
        self.utxos = initial_utxos
        self.fees = fees

    def current_utxos(self) -> list[dict]:
        return self.utxos

    def current_balances(self) -> dict:
        return {utxo["address"]: utxo["value"] for utxo in self.utxos}

    def submit_transaction(self, body: TxBody):
        tx_hash = secrets.token_hex(32)  # 64 chars

        utxos_dict = {}
        for i, utxo in enumerate(self.utxos):
            # Convert our utxos to a dictionary for better performance later
            utxos_dict[utxo["hash"] + str(utxo["index"])] = copy.deepcopy(utxo)

            # Remove utxo from our list (since we are consuming it)
            del self.utxos[i]

        total_input_value = Value()
        for utxo in body.inputs:
            # Make sure all body UTxOs exist
            # Also calculate total input value in the process

            parsed_utxo = utxo["hash"] + str(utxo["index"])

            if not parsed_utxo in utxos_dict:
                raise MochaError(f"UTxO {parsed_utxo} does not exist!")

            total_input_value.add_value(utxos_dict[parsed_utxo]["value"])

        total_output_value = Value()
        for output in body.outputs:
            total_output_value.add_value(Value.from_dictionary(output["value"]))

        subtraction = Value.subtract_values(
            total_input_value,
            Value.add_values(total_output_value, Value.lovelace(self.fees))
        )
        zero = Value()

        # If our outputs + fees is greater than our inputs
        if Value.less(subtraction, zero):
            raise MochaError(f"Unbalanced transaction {subtraction.get()}")

        if subtraction != zero:
            self.utxos.append({
                "hash": tx_hash,
                "index": 0,
                "address": body.change,
                "value": subtraction
            })

        for i, output in enumerate(body.outputs):
            self.utxos.append({
                "hash": tx_hash,
                "index": i+1,
                "address": output["address"],
                "value": Value.from_dictionary(output["value"])
            })

        return tx_hash

    def __eq__(self, other) -> bool:
        return type(other) == type(self) and other.utxos == self.utxos and other.fees == self.fees
