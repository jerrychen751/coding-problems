from typing import Dict, Optional
from currency.models import Currency, Money
from ledger.models import LedgerEntry, SpendType
from policies.models import ExpenseCategory

CAPEX_CATEGORIES = {ExpenseCategory.HARDWARE, ExpenseCategory.SOFTWARE}


class LedgerService:
    """Tracks finalized, approved company expenses by category and CapEx/OpEx classification."""

    def __init__(self):
        self._entries: Dict[str, LedgerEntry] = {}

    def record_expense(
        self,
        expense_id: str,
        employee_id: str,
        department_id: str,
        category: ExpenseCategory,
        usd_amount: Money,
    ) -> LedgerEntry:
        if usd_amount.currency != Currency.USD:
            raise ValueError("Ledger entries must be normalized to USD before posting.")
        if expense_id in self._entries:
            raise ValueError(f"Expense {expense_id} has already been posted to the ledger.")

        spend_type = SpendType.CAPEX if category in CAPEX_CATEGORIES else SpendType.OPEX
        entry = LedgerEntry(
            expense_id=expense_id,
            employee_id=employee_id,
            department_id=department_id,
            category=category,
            spend_type=spend_type,
            usd_amount_cents=usd_amount.amount_cents,
        )
        self._entries[expense_id] = entry
        return entry

    def get_total_by_category(self, category: ExpenseCategory) -> int:
        return sum(e.usd_amount_cents for e in self._entries.values() if e.category == category)

    def get_total_capex(self, department_id: Optional[str] = None) -> int:
        # returning capex for all departments or a single specific department
        return sum(
            e.usd_amount_cents
            for e in self._entries.values()
            if e.spend_type == SpendType.CAPEX and (department_id is None or e.department_id == department_id)
        )