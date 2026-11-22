from dataclasses import dataclass
from enum import Enum


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: Currency = Currency.USD

    def __lt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot compare money across currencies without conversion: "
                f"{self.currency.value} vs {other.currency.value}"
            )
        return self.amount_cents < other.amount_cents

    def __le__(self, other: "Money") -> bool:
        return self == other or self < other