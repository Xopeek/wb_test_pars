import requests

from exception import WildberriesAPIError


def get_wildberries_prices(article):
    url = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=27&nm={article};{article}'
    result = {}
    try:
        # GET-запрос к API Wildberries
        response = requests.get(url)

        # Проверяем успешность запроса
        response.raise_for_status()

        data = response.json()

        product = data.get('data').get('products')[0]

        if not product:
            raise WildberriesAPIError('No product information found.')

        result['price_without_sale'] = product.get('priceU')
        result['sale_price'] = product.get('salePriceU')

        return result
    except requests.exceptions.RequestException as e:
        raise WildberriesAPIError(f'Request error: {e}') from e
    except (KeyError, IndexError) as e:
        raise WildberriesAPIError(f'Error parsing API response: {e}') from e


def format_price(price):
    if price is not None:
        return f'{price / 100:.2f}'
    return None


if __name__ == "__main__":
    article_number = input('Введите артикул товара: ')

    try:
        prices_info = get_wildberries_prices(article_number)
        formatted_base_price = format_price(prices_info.get('price_without_sale'))
        formatted_sale_price = format_price(prices_info.get('sale_price'))

        print(f'Цена без скидок: {formatted_base_price} руб.')
        print(f'Цена со скидкой и СПП: {formatted_sale_price} руб.')
    except WildberriesAPIError as e:
        print(f'Ошибка при работе с API Wildberries: {e}')
