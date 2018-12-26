"""
Provide constants for `gimmeremmetokensbot` Telegram bot.
"""
REQUEST_TOKENS_KEYBOARD_BUTTON = 'Request a new batch of tokens'
CHECK_MY_BALANCE_KEYBOARD_BUTTON = 'Check my address tokens balance'

START_COMMAND_BOT_GREETING_PHRASE = """
Hello user, and welcome to REMME community!
I am a Telegram bot designed to help you interact with REMME testnet functionality. 

For the testing purposes you can request a batch of tokens. To receive it on your address, click on the keyboard below.
"""

START_COMMAND_BOT_TESTNET_INTERACTIONS_PHRASE = """
\n[Blockexplorer](https://blockexplorer.remme.io) can be useful to check sent transactions, including yours!
Broaden horizon - [use libraries written in several programming languages](https://docs.remme.io/) to work with blockchain in many different ways!

If you are more a user than a developer, take a look at our [certificate-based authentication](https://webauth-testnet.remme.io/how-to-use) called *WebAuth*.
It allows you to log in without the password. Use keystore file generated especially for you.

If you have any questions, just ping us in the [Gitter](https://gitter.im/REMME-Tech) channel.
"""

ALREADY_GOTTEN_ACCOUNT_CREDENTIALS_PHRASE = \
    'You already got the credentials. Find it at the start of this dialog.'

SOMETHING_WENT_WRONG_PHRASE = \
    'Something went wrong! Please, contact administrator — @SergYelagin.'
