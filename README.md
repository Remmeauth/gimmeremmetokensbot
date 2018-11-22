## Dependencies

Our project have the following dependencies:

1. Python 3.6+

## Getting started

Clone repository from Github:
```
$ git clone https://github.com/Remmeauth/gimmeremmetokensbot
$ cd gimmeremmetokensbot
```

Install requirements via pip:

```
$ git clone https://github.com/Remmeauth/gimmeremmetokensbot
$ cd gimmeremmetokensbot
$ pip3 install -r requirement.txt
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
3. PORT - automatically set by Heroku and do not need for local development.

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
