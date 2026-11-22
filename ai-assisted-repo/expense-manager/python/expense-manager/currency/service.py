from decimal import Decimal, ROUND_HALF_UP
from typing import Dict
from currency.models import Currency, Money


class FXService:
    """Provides currency conversion into normalized USD cents."""

    def __init__(self):
        self._rates: Dict[Currency, Decimal] = {
            Currency.USD: Decimal("1.0"),
            Currency.EUR: Decimal("1.10"),  # 1 EUR = 1.10 USD
            Currency.GBP: Decimal("1.30"),  # 1 GBP = 1.30 USD
            Currency.CAD: Decimal("0.75"),  # 1 CAD = 0.75 USD
        }

    def convert_to_usd(self, money: Money) -> Money:
        if money.currency == Currency.USD:
            return money
        rate = self._rates.get(money.currency)
        if rate is None:
            raise ValueError(f"Unsupported currency: {money.currency}")
        converted_cents = (Decimal(money.amount_cents) * rate).to_integral_value(rounding=ROUND_HALF_UP)
        return Money(amount_cents=int(converted_cents), currency=Currency.USD)