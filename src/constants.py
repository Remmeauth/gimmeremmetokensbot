"""
Provide constants for `gimmeremmetokensbot` Telegram bot.
"""
REQUEST_TOKENS_KEYBOARD_BUTTON = 'Request a new batch of tokens'
CHECK_MY_BALANCE_KEYBOARD_BUTTON = 'Check my address tokens balance'

START_COMMAND_BOT_GREETING_PHRASE = """
Hello!
Welcome to Remme Protocol TestChain!
I am a Telegram bot designed to help you to get started. 

For the testing purposes you can request a batch of tokens. To receive it on your account, click on the keyboard below.
"""

START_COMMAND_BOT_TESTNET_INTERACTIONS_PHRASE = """
\n[Blockexplorer](https://testchain.remme.io) can be useful to check sent transactions, including yours!

If you have any questions, just ping us in the [Gitter](https://gitter.im/REMME-Tech) channel.
"""

ALREADY_GOTTEN_ACCOUNT_CREDENTIALS_PHRASE = \
    'You already got the credentials. Find it at the start of this dialog.'

SOMETHING_WENT_WRONG_PHRASE = \
    'Something went wrong! Please, contact administrator — @dmytrostriletskyi.'

FAUCET_IS_EMPTY_PHRASE = \
    'Faucet is empty. Please, contact administrator to top up its tokens — @dmytrostriletskyi.'
