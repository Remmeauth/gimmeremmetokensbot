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
```

Visit [environment variables](#environment-variables) section to make sure you set all environment variables needed for project.

Start server via command line interface:

```
$ python3.6 core/app.py
```

## Environment variables

Environment variables are variables that are defined for the current shell and are inherited by any child shells or processes, 
they are used to pass information into processes that are spawned from the shell. It can be said that environment variables help to create and shape the environment of where a program runs.

We must use environment variable for simultaneous use of bot functions for local and production servers without changing the code.

Create the Telegram test bot with which you will work locally.

Required environment variables:

1. ENVIRONMENT - variable for simultaneous use of bot functions for local and production servers without changing the code. Possible: `local` or `production`.
2. TELEGRAM_BOT_TOKEN - to share bot Telegram bot secure.
3. MASTER_ACCOUNT_PRIVATE_KEY - account's private key to send testing token from.
4. STABLE_REMME_TOKENS_REQUEST_AMOUNT - amount of the Remme tokens to send from master account.
5. NODE_PUBLIC_KEY - node, Telegram bot should make requests, public key.
6. STORAGE_PUBLIC_KEY - storage, Telegram bot should make requests, public key.
7. PRODUCTION_HOST - if you run Telegram bot on production, set host (i.e. `https://intense-harbor-47746.herokuapp.com`)

To get node and storage public keys, visit (RPC API)[https://remmeio.atlassian.net/wiki/spaces/WikiREMME/pages/292814862/RPC+API+specification] of node.

```
$ export ENVIRONMENT="local"
```
To see a list of all of our environment variables and make sure that there is an environment variable, check its value:

```
# env or printenv
$ printenv ENVIRONMENT
```

For the main bot on the Heroku server, set the environment variable `production`:

```
$ heroku config:set ENVIRONMENT=production
```

This environment variable is persistent – it will remain in place across deploys and app restarts – so unless you need to change value, you only need to set it once.

Make sure that there is an environment variable, check its value:

```
$ heroku config or heroku config:get ENVIRONMENT
```

Access the environment variables using the `os.environ['ENVIRONMENT']` template in Python.

For instance:

```
if os.environ.get('ENVIRONMENT') == 'production':
    SERVER.run(host='0.0.0.0'), port=int(os.environ.get('PORT', 5000)))

if os.environ.get('ENVIRONMENT') == 'local':
    bot.polling()
```
