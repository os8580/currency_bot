import requests
import json

api_url = 'https://min-api.cryptocompare.com/data/price'


class _HiddenAPIException(Exception):
    def __init__(self, message):
        self.message = message


class _HiddenCurrencyConverter:
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
            raise _HiddenAPIException("Неверная валюта")

        params = {'fsym': base_currency, 'tsyms': quote_currency}
        response = requests.get(api_url, params=params)
        data = json.loads(response.text)

        if quote_currency in data:
            rate = data[quote_currency]
            converted_amount = amount * rate
            return converted_amount
        else:
            raise _HiddenAPIException("Неверная валюта")
