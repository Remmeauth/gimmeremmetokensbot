"""
Settings of the database.
"""
import os

import psycopg2

from utils import parse_db_url

DATABASE_URL = os.environ.get('DATABASE_URL')


def connection_to_db():
    """
    Return connection to the database or error.
    """
    credentials = parse_db_url(DATABASE_URL)
    connection = psycopg2.connect(**credentials)

    return connection


def create_db_tables():
    """
    Create database tables.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS remme_tokens_recodring (
        chat_id INTEGER UNIQUE NOT NULL,
        nickname VARCHAR (50) UNIQUE NOT NULL,
        address VARCHAR (128) UNIQUE NOT NULL,
        public_key VARCHAR (128) UNIQUE NOT NULL,
        are_creads_shown BOOLEAN NOT NULL,
        token_request_datetime TIMESTAMP DEFAULT NULL);
        """
    )

    connection.commit()


def check_if_user_exist(chat_id):
    """
    Check if user exists.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM remme_tokens_recodring WHERE chat_id={};".format(chat_id))

    user = cursor.fetchall()

    if user:
        return True

    return False


def insert_starter_user_info(chat_id, nickname, address, public_key, are_creads_shown):
    """
    Insert starter user information to table.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO remme_tokens_recodring (chat_id, nickname, address, public_key, are_creads_shown) "
        "VALUES (%s, %s, %s, %s, %s);", (chat_id, nickname, address, public_key, are_creads_shown)
    )

    connection.commit()


def get_public_key(chat_id):
    """
    Get public key by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT public_key FROM remme_tokens_recodring WHERE chat_id={};".format(chat_id))

    return cursor.fetchone()[0]


def get_address(chat_id):
    """
    Get address by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT address FROM remme_tokens_recodring WHERE chat_id={};".format(chat_id))

    return cursor.fetchone()[0]
