from currency.models import Currency, Money
from currency.service import FXService


def test_convert_to_usd_identity():
    fx = FXService()
    usd = Money(5000, Currency.USD)
    assert fx.convert_to_usd(usd).amount_cents == 5000


def test_convert_to_usd_foreign_rates():
    fx = FXService()
    eur = Money(9500, Currency.EUR)
    assert fx.convert_to_usd(eur).amount_cents == 10450


def test_convert_to_usd_rounding_precision():
    fx = FXService()
    eur = Money(2999, Currency.EUR)
    assert fx.convert_to_usd(eur).amount_cents == 3299