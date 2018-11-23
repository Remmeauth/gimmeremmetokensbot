"""
Provide utils for `gimmeremmetokensbot` Telegram bot.
"""


def parse_db_url(url):
    """
    Parse database DSN to particular entities (host, port, database, user, password).
    """
    url = url.replace('postgres://', '').replace('@', ' ').replace(':', ' ').replace('/', ' ').split()

    database_url = {}

    for part, credential in zip(range(len(url)), ['user', 'password', 'host', 'port', 'database']):
        database_url[credential] = url[part]

    return database_url
