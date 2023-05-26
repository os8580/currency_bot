import telebot
import requests
import json

TOKEN = '6276511393:AAFxb2SsNUVUpqtJ0OnO4cJuF74Lh4_c6DI'
bot = telebot.TeleBot(TOKEN)

api_url = 'https://min-api.cryptocompare.com/data/price'


class APIException(Exception):
    def __init__(self, message):
        self.message = message


class CurrencyConverter:
    @staticmethod
    def get_price(base_currency, quote_currency, amount):
        """
        Получить цену конвертации одной валюты в другую.

        :param base_currency: Исходная валюта для конвертации
        :param quote_currency: Валюта, в которую нужно конвертировать
        :param amount: Количество исходной валюты для конвертации
        :return: Конвертированная сумма в указанной валюте
        """
        # Проверяем, разрешены ли исходная и целевая валюты
        allowed_currencies = ['EUR', 'USD', 'RUB']
        if base_currency not in allowed_currencies or quote_currency not in allowed_currencies:
            raise APIException("Неверная валюта")

        params = {'fsym': base_currency, 'tsyms': quote_currency}
        response = requests.get(api_url, params=params)
        data = json.loads(response.text)

        if quote_currency in data:
            rate = data[quote_currency]
            converted_amount = amount * rate
            return converted_amount
        else:
            raise APIException("Неверная валюта")


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
            raise APIException("Неверный формат ввода")

        base_currency = parts[0].upper()
        quote_currency = parts[1].upper()
        amount = float(parts[2])

        # Выполняем конвертацию валюты с помощью класса CurrencyConverter
        converted_amount = CurrencyConverter.get_price(base_currency, quote_currency, amount)
        bot.reply_to(message, f"{amount} {base_currency} примерно равно {converted_amount} {quote_currency}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e.message}")
    except ValueError:
        bot.reply_to(message, "Неверный формат числа")
    except IndexError:
        bot.reply_to(message, "Неверный формат ввода")


bot.polling()
