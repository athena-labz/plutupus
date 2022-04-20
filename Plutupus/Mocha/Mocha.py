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
        result = {}

        for utxo in self.utxos:
            if utxo["address"] in result:
                result[utxo["address"]].add_value(utxo["value"])
            else:
                result[utxo["address"]] = copy.deepcopy(utxo["value"])

        return result

    def submit_transaction(self, body: TxBody):
        tx_hash = secrets.token_hex(32)  # 64 chars

        utxos_dict = {}

        while True:
            if len(self.utxos) == 0:
                break
                
            utxo = copy.deepcopy(self.utxos[0])

            # Remove utxo from our list (since we are consuming it)
            del self.utxos[0]
    
            # Convert our utxos to a dictionary for better performance later
            utxos_dict[utxo["hash"] + str(utxo["index"])] = utxo

        total_input_value = Value()
        for utxo in body.inputs:
            # Make sure all body UTxOs exist
            # Also calculate total input value in the process

            parsed_utxo = utxo["hash"] + str(utxo["index"])

            if not parsed_utxo in utxos_dict:
                raise MochaError(f"UTxO {parsed_utxo} does not exist!")

            total_input_value.add_value(utxos_dict[parsed_utxo]["value"])

        if body.mint_value is not None:
            for asset, amount in body.mint_value.items():
                total_input_value.add_token_amount(asset, amount)

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

        cur_index = 0
        if body.collateral is not None:
            # Add collateral back to output
            collateral_utxo = body.collateral
            parsed_utxo = collateral_utxo["hash"] + str(collateral_utxo["index"])

            if not parsed_utxo in utxos_dict:
                raise MochaError(f"UTxO from collateral {parsed_utxo} does not exist!")
            
            self.utxos.append({
                "hash": tx_hash,
                "index": cur_index,
                "address": utxos_dict[parsed_utxo]["address"],
                "value": utxos_dict[parsed_utxo]["value"]
            })

            cur_index += 1

        # Add change
        if subtraction != zero:
            self.utxos.append({
                "hash": tx_hash,
                "index": cur_index,
                "address": body.change,
                "value": subtraction
            })

            cur_index += 1

        for i, output in enumerate(body.outputs):
            self.utxos.append({
                "hash": tx_hash,
                "index": cur_index+i,
                "address": output["address"],
                "value": Value.from_dictionary(output["value"])
            })

        return tx_hash

    def __eq__(self, other) -> bool:
        return type(other) == type(self) and other.utxos == self.utxos and other.fees == self.fees
