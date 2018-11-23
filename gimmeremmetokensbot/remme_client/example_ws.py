from remme.remme import Remme
from remme.models.base_transaction_response import BaseTransactionResponse
import asyncio
import json


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    # _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    _address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"
    node_private_key = "4c0393f24225443678543642d5a48ac0534b894ab82ae5f118d330fd2f56dae4"

    batch_id = "bc1b32a5ead06cc9203d0019a54391b40a7eadb61c80675de60ecc83d4be6fed0c795dfbccc717e3d52bf3fec8a3cbfc7cf6ab8fc1cdfd07f8b76bf457288060"
    kwargs = {"node_address": "localhost:8080", "ssl_mode": False, "batch_id": batch_id}
    tx = BaseTransactionResponse(**kwargs)
    async for msg in tx.connect_to_web_socket():
        print("connected")
        print("handle some messages")
        await tx.close_web_socket()

    print("connection closed")


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
