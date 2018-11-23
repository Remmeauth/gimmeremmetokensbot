"""
Settings of the database.
"""
import os
from datetime import datetime

import psycopg2

from utils import parse_db_url

DATABASE_URL = os.environ.get('DATABASE_URL')


def connection_to_db():
    """
    Get connection to the database.
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
    Check if user exists by chat id.
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


def update_request_tokens_datetime(chat_id):
    """
    Update request tokens datetime by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'

    cursor.execute(
        "UPDATE remme_tokens_recodring SET token_request_datetime=%s WHERE chat_id=%s;", (date_string, chat_id),
    )

    connection.commit()


def get_public_key(chat_id):
    """
    Get public key by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT public_key FROM remme_tokens_recodring WHERE chat_id={};".format(chat_id))

    try:
        return cursor.fetchone()[0]
    except TypeError:
        raise psycopg2.ProgrammingError('Fetching went wrong! No database record found.')


def get_address(chat_id):
    """
    Get address by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT address FROM remme_tokens_recodring WHERE chat_id={};".format(chat_id))

    try:
        return cursor.fetchone()[0]
    except TypeError:
        raise psycopg2.ProgrammingError('Fetching went wrong! No database record found.')


def get_request_tokens_datetime(chat_id):
    """
    Get request tokens datetime by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT token_request_datetime FROM remme_tokens_recodring WHERE chat_id={};".format(chat_id))

    try:
        return cursor.fetchone()[0]
    except TypeError:
        raise psycopg2.ProgrammingError('Fetching went wrong! No database record found.')
