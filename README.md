# Currency Bot

Currency Bot is a Telegram bot that allows users to perform currency conversions. It uses the `telebot` library for interacting with Telegram and the `requests` library for fetching exchange rates.

## Getting Started

To use the Currency Bot, you need to have Python 3.11 installed. Follow the steps below to get the bot up and running:

1. Clone the repository to your local machine:

git clone https://github.com/os8580/currency_bot.git
cd currency_bot

Install the required dependencies using pipenv:
pip install pipenv
pipenv install

Obtain your Telegram bot token from the BotFather and add it to the config.py file:
TOKEN = 'your_telegram_bot_token_here'


Run the bot:
pipenv run python main.py

Interact with the bot in your Telegram app:
Send the /start or /help command to get instructions on how to use the bot.
Use the /values command to get information about available currencies.
Perform currency conversion by sending a message in the format <currency_to_convert> <conversion_currency> <amount>. For example, EUR USD 100 to convert 100 Euros to US Dollars.
Available Commands
/start, /help - Display bot usage instructions.
/values - Show available currencies for conversion.
Notes
The bot currently supports conversion between the following currencies: EUR, USD, and RUB.
The exchange rates are fetched from the Cryptocompare API.
Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request.

