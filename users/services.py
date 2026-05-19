import stripe
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """
    Создать продукт в Stripe.
    """
    try:
        product = stripe.Product.create(name=name)
        return product
    except Exception as e:
        raise Exception(f"Ошибка создания продукта в Stripe: {str(e)}")


def create_stripe_price(product_id, amount):
    """
    Создать цену в Stripe.

    :param product_id: ID продукта в Stripe
    :param amount: Сумма в рублях (будет переведена в копейки)
    """
    try:
        # Конвертируем рубли в копейки (умножаем на 100)
        amount_in_cents = int(Decimal(amount) * 100)

        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount_in_cents,
            currency='rub',
        )
        return price
    except Exception as e:
        raise Exception(f"Ошибка создания цены в Stripe: {str(e)}")


def create_stripe_session(price_id):
    """
    Создать сессию оплаты в Stripe.

    :param price_id: ID цены в Stripe
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/api/payments/success/',
            cancel_url='http://127.0.0.1:8000/api/payments/cancel/',
        )
        return session
    except Exception as e:
        raise Exception(f"Ошибка создания сессии в Stripe: {str(e)}")


def retrieve_stripe_session(session_id):
    """
    Получить информацию о сессии оплаты.

    :param session_id: ID сессии в Stripe
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except Exception as e:
        raise Exception(f"Ошибка получения сессии из Stripe: {str(e)}")
