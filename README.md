# Gimmeremmetokensbot

![Python3](https://img.shields.io/badge/Python-3.7-brightgreen.svg)

`Gimmeremmetokensbot` — [Telegram bot](https://core.telegram.org/bots) for [Remme](https://remme.io) tokens distribution for testing purposes.

![example-of-usage](https://github.com/Remmeauth/gimmeremmetokensbot/blob/develop/assets/bot_usage_example_600_520.gif)

Bot's the following functionality:
1. Create new account for user;
2. Distribute Remme tokens to account address;
3. Inform user about account tokens balance.

Bots ready to use: [@RemmeProtocolTestnetFaucetBot](https://t.me/RemmeProtocolTestnetFaucetBot)

## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/Remmeauth/gimmeremmetokensbot.git
$ cd gimmeremmetokensbot
```

To build the project, use the following command:

```bash
$ docker build -t gimmeremmetokensbot . -f Dockerfile.development
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -v $PWD:/gimmeremmetokensbot \
      -e ENVIRONMENT=development \
      -e TELEGRAM_BOT_TOKEN='918231803:AAHLN7w1xg82ziHzI3Pgb0NnG0pAFErFS2Q' \
      -e DATABASE_URL='postgres://vtlavnrs:C1y8UMym4YCHMk7Mw26MfX9nGzUOmq2i@raja.db.elephantsql.com:5432/vtlavnrs' \
      -e NODEOS_HOST='api.jungle.greeneosio.com' \
      -e NODEOS_PORT='443' \
      -e MASTER_WALLET_PRIVATE_KEY='5JpmiRtExjyyRWsGHnqEtfUNZQsuVDUZZHbRhDHJgqzkCcpMeo5' \
      -e MASTER_ACCOUNT_NAME='remmefaucetp' \
      -e TRANSACTIONS_SYMBOL='EOS' \
      -e STABLE_REMME_TOKENS_REQUEST_AMOUNT='3' \
      --name gimmeremmetokensbot gimmeremmetokensbot
```

If you need to enter the bash of the container, use the following command:

```bash
$ docker exec -it gimmeremmetokensbot bash
```

Clean all containers with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
```

Clean all images with the following command:

```bash
$ docker rmi $(docker images -q) -f
```

## Production


Clone the project with the following command:

```bash
$ git clone https://github.com/Remmeauth/gimmeremmetokensbot.git
$ cd gimmeremmetokensbot
```

To build the project, use the following command:

```bash
$ docker build -t gimmeremmetokensbot . -f Dockerfile.production
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -p 8000:8000 -e PORT=8000 -v $PWD:/gimmeremmetokensbot \
      -e ENVIRONMENT=production \
      -e TELEGRAM_BOT_TOKEN='918231803:AAHLN7w1xg82ziHzI3Pgb0NnG0pAFErFS2Q' \
      -e DATABASE_URL='postgres://vtlavnrs:C1y8UMym4YCHMk7Mw26MfX9nGzUOmq2i@raja.db.elephantsql.com:5432/vtlavnrs' \
      -e NODEOS_HOST='api.jungle.greeneosio.com' \
      -e NODEOS_PORT='443' \
      -e MASTER_WALLET_PRIVATE_KEY='5JpmiRtExjyyRWsGHnqEtfUNZQsuVDUZZHbRhDHJgqzkCcpMeo5' \
      -e MASTER_ACCOUNT_NAME='remmefaucetp' \
      -e TRANSACTIONS_SYMBOL='EOS' \
      -e STABLE_REMME_TOKENS_REQUEST_AMOUNT=3 \
      -e PRODUCTION_HOST='https://gimmeremmetokensbot-staging.herokuapp.com' \
      -e REQUEST_TOKENS_PERIOD_IN_HOURS_LIMIT=1 \
      --name gimmeremmetokensbot gimmeremmetokensbot
```
