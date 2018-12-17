# Gimmeremmetokensbot

![Python3](https://img.shields.io/badge/Python-3.6-brightgreen.svg)

`Gimmeremmetokensbot` — [Telegram bot](https://core.telegram.org/bots) for [Remme](https://remme.io) tokens distribution for testing purposes.

![example-of-usage](https://github.com/Remmeauth/gimmeremmetokensbot/blob/develop/assets/bot_usage_example_600_520.gif)

Bot's the following functionality:
1. Create new account for user;
2. Distribute Remme tokens to account address;
3. Inform user about account tokens balance.

Bots ready to use: [@RemmeFaucetBot](https://t.me/RemmeFaucetBot)

## Dependencies

Our project have the following dependencies:

1. Python 3.6+;
2. libsecp256k1-dev;
3. Required by one of the requirements [system packages list](https://github.com/ludbb/secp256k1-py#installation-with-compilation).

## Getting started

Clone repository from Github:
```
$ git clone https://github.com/Remmeauth/gimmeremmetokensbot
$ cd gimmeremmetokensbot
```

Install requirements via pip:

```
$ pip3 install -r requirements.txt
$ pip3 install -r requirements-dev.txt
```

Visit [environment variables](#environment-variables) section to make sure you set all environment variables needed for project.

Start server via command line interface:

```
$ python3.6 gimmeremmetokensbot/app.py
```

## Environment variables

Environment variables are variables that are defined for the current shell and are inherited by any child shells or processes, 
they are used to pass information into processes that are spawned from the shell. It can be said that environment variables help to create and shape the environment of where a program runs.

Variable for simultaneous use of bot functions for development and production servers without changing the code.

Required environment variables:

1. `ENVIRONMENT` - `development` or `production`.
2. `TELEGRAM_BOT_TOKEN` - to share bot Telegram bot secure.
3. `MASTER_ACCOUNT_PRIVATE_KEY` - account's private key to send testing token from.
4. `STABLE_REMME_TOKENS_REQUEST_AMOUNT` - amount of the Remme tokens to send from master account.
5. `NODE_HOST` - node, Telegram bot should make requests, host (`i.e. node-genesis-testnet.remme.io`).
6. `NODE_PUBLIC_KEY` - node, Telegram bot should make requests, public key.
7. `STORAGE_PUBLIC_KEY` - storage, Telegram bot should make requests, public key.
8. `PRODUCTION_HOST` - if you run Telegram bot on production, set host (i.e. `https://intense-harbor-47746.herokuapp.com`)
9. `DATABASE_URL` - production database DSN URL to store information about users.
10. `REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT` - request tokens period in hours limit.

To get node and storage public keys, visit [RPC API](https://remmeio.atlassian.net/wiki/spaces/WikiREMME/pages/292814862/RPC+API+specification) of node.

```
$ export ENVIRONMENT="development"
```
To see a list of all of our environment variables and make sure that there is an environment variable, check its value:

```
# env or printenv
$ printenv ENVIRONMENT
```

Access the environment variables using the `os.environ.get('ENVIRONMENT')` template in Python.

For instance:

```python
if os.environ.get('ENVIRONMENT') == 'production':
    server.run(host='0.0.0.0'), port=int(os.environ.get('PORT', 5000)))

if os.environ.get('ENVIRONMENT') == 'development':
    bot.polling()
```

## Development

Environment variable `TESTING_DATABASE_URL` to access the test database is required:

```
$ export TESTING_DATABASE_URL=
```

To run all tests or run particular test use the following command:

```
$ pytest -vv gimmeremmetokensbot
$ pytest -vv gimmeremmetokensbot/tests/test_database.py
$ pytest -vv gimmeremmetokensbot/tests/test_database.py::test_check_if_user_exist
```
