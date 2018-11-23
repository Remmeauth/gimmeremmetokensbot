"""
Provide tests for database layer implementation of `gimmeremmetokensbot` Telegram bot.
"""
from datetime import datetime

from gimmeremmetokensbot.database import (
    check_if_user_exist,
    get_address,
    get_public_key,
    get_request_tokens_datetime,
    insert_starter_user_info,
    update_request_tokens_datetime,
)


def test_check_if_user_exist(db_table, insert_user_info):
    """
    Case: check if user exists by chat id.
    Expect: user does not exists.
    """
    expected_result, result = False, check_if_user_exist(chat_id=17913)

    assert expected_result == result


def test_insert_starter_user_info(db_table):
    """
    Case: insert starter user info to database table.
    Expect: starter user info inserted to database.
    """
    insert_starter_user_info(
        chat_id=28446283,
        nickname='dog',
        address='112007725c102f8166397a343707421b1adaa09f4a64347b79dc4217dfwjfij8438543',
        public_key='02b2cde4828e9800d4740f37de8118cfef59a8508163b3f1b0cefiowjifwi89g9e',
        are_creads_shown=True,
    )

    expected_result, result = True, check_if_user_exist(28446283)

    assert expected_result == result


def test_update_request_tokens_datetime(db_table, insert_user_info):
    """
    Case: update request tokens datetime by chat id.
    Expect: tokens datetime updated from null to the present time.
    """
    update_request_tokens_datetime(chat_id=33667738)
    result = get_request_tokens_datetime(chat_id=33667738)

    assert result is not None


def test_get_public_key(db_table, insert_user_info):
    """
    Case: get user public key by chat id.
    Expect: public key is returned.
    """
    expected_public_key = '02b2cde4828e9800d4740f37de8118cfef59a8508163b3f1b0c9200shieow346hh'
    result = get_public_key(chat_id=33667738)

    assert expected_public_key == result


def test_address(db_table, insert_user_info):
    """
    Case: get user address by chat id.
    Expect: address is returned.
    """
    expected_address = '112007725c102f8166397a343707421b1adaa09f4a64347b79dc4217df825123hb34jk'
    result = get_address(chat_id=33667738)

    assert expected_address == result


def test_request_tokens_datetime(db_table, insert_user_info):
    """
    Case: get request tokens datetime by chat id.
    Expect: type datetime is returned.
    """
    update_request_tokens_datetime(chat_id=33667738)
    result = get_request_tokens_datetime(chat_id=33667738)

    assert type(datetime.now()) == type(result)
