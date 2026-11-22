import pytest
from currency.models import Currency, Money
from ledger.service import LedgerService
from policies.models import ExpenseCategory


def test_ledger_capex_and_category_totals():
    ledger = LedgerService()
    ledger.record_expense("exp_1", "e_dev", "ENG", ExpenseCategory.HARDWARE, Money(150_000, Currency.USD))
    ledger.record_expense("exp_2", "e_dev", "ENG", ExpenseCategory.FOOD_AND_BEVERAGE, Money(2_500, Currency.USD))

    assert ledger.get_total_by_category(ExpenseCategory.HARDWARE) == 150_000
    assert ledger.get_total_capex("ENG") == 150_000


def test_ledger_prevents_duplicate_posting():
    ledger = LedgerService()
    ledger.record_expense("exp_1", "e_dev", "ENG", ExpenseCategory.HARDWARE, Money(150_000, Currency.USD))

    with pytest.raises(ValueError):
        ledger.record_expense("exp_1", "e_dev", "ENG", ExpenseCategory.HARDWARE, Money(150_000, Currency.USD))