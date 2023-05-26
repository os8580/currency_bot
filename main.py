import telebot
from config import TOKEN
from extensions import _HiddenAPIException, _HiddenCurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    """
    Обработка команды /start и /help.

    :param message: Объект сообщения
    """
    # Инструкции по использованию бота
    instructions = "Добро пожаловать в Currency Bot!\n\nИнструкции:\n1. Отправьте сообщение в формате " \
                   "<валюта_для_конвертации> <валюта_конвертации> <сумма>\nПример: EUR USD 100\n\n2. Используйте " \
                   "команду /values, чтобы получить информацию о доступных валютах."
    bot.reply_to(message, instructions)


@bot.message_handler(commands=['values'])
def handle_values(message):
    """
    Обработка команды /values.

    :param message: Объект сообщения
    """
    # Отображение доступных валют
    available_currencies = ['EUR', 'USD', 'RUB']
    formatted_currencies = ', '.join(available_currencies)
    bot.reply_to(message, f"Доступные валюты: {formatted_currencies}")


@bot.message_handler(func=lambda message: True)
def handle_conversion(message):
    """
    Обработка конвертации валюты.

    :param message: Объект сообщения
    """
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise _HiddenAPIException("Неверный формат ввода")

        base_currency = parts[0].upper()
        quote_currency = parts[1].upper()
        amount = float(parts[2])

        # Выполняем конвертацию валюты с помощью класса _HiddenCurrencyConverter
        converted_amount = _HiddenCurrencyConverter.get_price(base_currency, quote_currency, amount)
        bot.reply_to(message, f"{amount} {base_currency} примерно равно {converted_amount} {quote_currency}")
    except _HiddenAPIException as e:
        bot.reply_to(message, f"Ошибка: {e.message}")
    except ValueError:
        bot.reply_to(message, "Ошибка: Неверный формат числа")
    except IndexError:
        bot.reply_to(message, "Ошибка: Неверный формат ввода")


bot.polling()
