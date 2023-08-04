import telebot
from config import TOKEN
from extensions import _HiddenAPIException, _HiddenCurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    """
    Handling the /start and /help commands.

    :param message: Message object
    """
    # Bot usage instructions
    instructions = "Welcome to Currency Bot!\n\nInstructions:\n1. Send a message in the format " \
                   "<currency_to_convert> <conversion_currency> <amount>\nExample: EUR USD 100\n\n2. Use " \
                   "/values command to get information about available currencies."
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def handle_values(message):
    """
    Handling the /values command.

    :param message: Message object
    """
    # Displaying available currencies
    available_currencies = ['EUR', 'USD', 'RUB']
    formatted_currencies = ', '.join(available_currencies)
    bot.reply_to(message, f"Available currencies: {formatted_currencies}")

@bot.message_handler(func=lambda message: True)
def handle_conversion(message):
    """
    Handling currency conversion.

    :param message: Message object
    """
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise _HiddenAPIException("Incorrect input format")

        base_currency = parts[0].upper()
        quote_currency = parts[1].upper()
        amount = float(parts[2])

        # Perform currency conversion using the _HiddenCurrencyConverter class
        converted_amount = _HiddenCurrencyConverter.get_price(base_currency, quote_currency, amount)
        bot.reply_to(message, f"{amount} {base_currency} is approximately equal to {converted_amount} {quote_currency}")
    except _HiddenAPIException as e:
        bot.reply_to(message, f"Error: {e.message}")
    except ValueError:
        bot.reply_to(message, "Error: Invalid number format")
    except IndexError:
        bot.reply_to(message, "Error: Incorrect input format")

bot.polling()
