from remme.remme import Remme
from remme.models.base_transaction_response import BaseTransactionResponse
import asyncio
import json


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    # _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    _address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"
    node_private_key = "4c0393f24225443678543642d5a48ac0534b894ab82ae5f118d330fd2f56dae4"
    sender_private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"

    remme = Remme(private_key_hex=sender_private_key_hex)

    data = "transaction data"
    print(f"data {data}")
    signed_data = remme.account.sign(data)
    print(f"signed by our account: {signed_data}")

    is_verify = remme.account.verify(signed_data, data)
    print(f"is verified by our account: {is_verify}")  # True

    another_account = Remme()
    is_verify_in_another_account = another_account.account.verify(signed_data, data)
    print(f"is verified by another account: {is_verify_in_another_account}")  # False


loop = asyncio.get_event_loop()
loop.run_until_complete(example())