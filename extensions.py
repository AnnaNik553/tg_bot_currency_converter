import requests

from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        data = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()

        if quote == 'рубль':
            res = round(data['rates'][base_ticker] / quote_ticker * float(amount), 2)
        elif base == 'рубль':
            res = round(base_ticker / data['rates'][quote_ticker] * float(amount), 2)
        else:
            res = round(data['rates'][base_ticker] / data['rates'][quote_ticker] * float(amount), 2)

        return res