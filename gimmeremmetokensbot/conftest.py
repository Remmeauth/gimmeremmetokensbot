"""
Provide functionality for test fixtures, settings and helpers.
"""
import pytest

from gimmeremmetokensbot.database import (
    create_db_tables,
    drop_db_tables,
    insert_starter_user_info,
)


@pytest.fixture
def insert_user_info():
    """
    Insert starter user information for testing purposes.
    """
    insert_starter_user_info(
        chat_id=33667738,
        nickname='pickles',
        address='112007725c102f8166397a343707421b1adaa09f4a64347b79dc4217df825123hb34jk',
        public_key='02b2cde4828e9800d4740f37de8118cfef59a8508163b3f1b0c9200shieow346hh',
        are_creads_shown=True,
    )


@pytest.yield_fixture
def db_table():
    """
    Initialize real database scheme for testing purposes dropping existing one.
    """
    create_db_tables()
    yield
    drop_db_tables()
