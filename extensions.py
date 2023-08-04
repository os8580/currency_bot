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
        Get the conversion price from one currency to another.

        :param base_currency: Source currency for conversion
        :param quote_currency: Currency to convert to
        :param amount: Amount of source currency to convert
        :return: Converted amount in the specified currency
        """
        # Check if the source and target currencies are allowed
        allowed_currencies = ['EUR', 'USD', 'RUB']
        if base_currency not in allowed_currencies or quote_currency not in allowed_currencies:
            raise _HiddenAPIException("Invalid currency")

        params = {'fsym': base_currency, 'tsyms': quote_currency}
        response = requests.get(api_url, params=params)
        data = json.loads(response.text)

        if quote_currency in data:
            rate = data[quote_currency]
            converted_amount = amount * rate
            return converted_amount
        else:
            raise _HiddenAPIException("Invalid currency")
