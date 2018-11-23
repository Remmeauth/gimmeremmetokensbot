import asyncio
from unittest import TestCase
from remme.remme import Remme


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)

    return wrapper


class RemmeTokenTest(TestCase):

    @async_test
    def tests_balance(self):
        remme = Remme()
        address = "Weird address"
        with self.assertRaises(Exception) as error:
            yield remme.token.transfer(address, 100)
