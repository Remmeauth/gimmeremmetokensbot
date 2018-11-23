from remme.models.create_certificate_dto import CreateCertificateDto
from remme.remme import Remme
import asyncio
import time


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    another_private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"

    remme = Remme(private_key_hex=private_key_hex)
    serial = int(time.time())
    certificate_data = CreateCertificateDto(common_name="user_name", email="user@email.com", name="John",
                                            surname="Smith", country_name="US", validity=360, serial=serial)
    certificate_transaction_result = await remme.certificate.create_and_store(certificate_data)
    async for response in certificate_transaction_result.connect_to_web_socket():
        print("connected")
        await certificate_transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
