"""
Provide utils for `gimmeremmetokensbot` Telegram bot.
"""
import os


def parse_db_url(url):
    """
    Parse database DSN to particular entities (host, port, database, user, password).
    """
    url = url.replace('postgres://', '').replace('@', ' ').replace(':', ' ').replace('/', ' ').split()

    database_url = {}

    for part, credential in zip(range(len(url)), ['user', 'password', 'host', 'port', 'database']):
        database_url[credential] = url[part]

    return database_url


def send_keystore_file(bot, message, account):
    """
    Send keystore file in `txt` format with public and private key.
    """
    file_content = '{' + f'"publicKey":"{account.public_key_hex}","privateKey":"{account.private_key_hex}"' + '}'

    with open(f'keystore_{message.chat.id}.txt', 'w+') as keystore_file:
        keystore_file.write(file_content)

    with open(f'keystore_{message.chat.id}.txt', 'r') as keystore_file:
        bot.send_document(message.chat.id, keystore_file)

    os.remove(f'keystore_{message.chat.id}.txt')
