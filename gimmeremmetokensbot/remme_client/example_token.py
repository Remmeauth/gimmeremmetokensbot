from remme_client.remme.constants.batch_status import BatchStatus
from remme_client.remme.remme import Remme
import asyncio


async def example():
    sender_private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    node_private_key = "4c0393f24225443678543642d5a48ac0534b894ab82ae5f118d330fd2f56dae4"
    # _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    # reciver_address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"

    receiver_private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
    # some_remme_address = "03c75297511ce0cfd1315a045dd0db2a4a1710efed94f0f94ad993b5dfe2e33b62"

    # start remme; some account without funds
    remme_receiver = Remme(private_key_hex=sender_private_key_hex)
    receiver_public_key_hex = remme_receiver.account.public_key_hex
    print(f"generated private key hex for receiving funds {receiver_public_key_hex}\n")

    # start another remme; some account with funds
    remme_sender = Remme(private_key_hex=node_private_key)

    # check balance before transaction
    before_balance = await remme_receiver.token.get_balance(receiver_public_key_hex)
    print(f'balance is : {before_balance} REM\n')
    transaction_result = await remme_sender.token.transfer(receiver_public_key_hex, 100)
    print(f'sending tokens... batch id : {transaction_result.batch_id}\n')

    batch_status = await remme_sender.batch.get_status(transaction_result.batch_id)
    print(f"batch status {batch_status}\n")

    async for batch_info in transaction_result.connect_to_web_socket():
        if batch_info.status == BatchStatus.COMMITTED.value:
            after_balance = await remme_sender.token.get_balance(receiver_public_key_hex)
            print(f'balance is: {after_balance} REM')
            await transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
