from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from remme.constants.batch_status import BatchStatus
from remme.remme import Remme
import asyncio
from datetime import datetime, timedelta

# variant with extracting keys from file
#
# private_key_file = open("test_rsa_private.key", "rb")
# public_key_file = open("test_rsa_public.key", "rb")
# data = {
#     "data": "store data",
#     "private_key": private_key_file.read(),
#     "public_key": public_key_file.read(),
#     "valid_from": int(datetime.utcnow().strftime("%s")),
#     "valid_to": int((datetime.utcnow() + timedelta(days=365)).strftime("%s"))
# }


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    node_private_key = "4c0393f24225443678543642d5a48ac0534b894ab82ae5f118d330fd2f56dae4"
    remme = Remme(private_key_hex=node_private_key)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    # check balance before transaction
    before_balance = await remme.token.get_balance(remme.account.public_key_hex)
    print(f'balance is : {before_balance} REM\n')

    data = {
        "data": "store data",
        "private_key": private_key,
        "public_key": private_key.public_key(),
        "valid_from": int(datetime.utcnow().strftime("%s")),
        "valid_to": int((datetime.utcnow() + timedelta(days=365)).strftime("%s"))
    }
    pubkey_storage_transaction_result = await remme.public_key_storage.store(**data)

    batch_status = await remme.batch.get_status(pubkey_storage_transaction_result.batch_id)
    print(f"batch status {batch_status}\n")

    async for response in pubkey_storage_transaction_result.connect_to_web_socket():
        print("connected")

        print(f"response status :{response.status}")
        batch_status = await remme.batch.get_status(pubkey_storage_transaction_result.batch_id)
        print(f"batch status {batch_status}\n")

        if response.status == BatchStatus.INVALID.value:
            print(f"Error occurs : {response.invalid_transactions}")
            await pubkey_storage_transaction_result.close_web_socket()
            break

        if response.status == BatchStatus.COMMITTED.value:
            print("Batch COMMITTED")

            # check public key in chain

            # revoke public key in chain

            # check public key in chain

            await pubkey_storage_transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
