from dataclasses import dataclass
from enum import Enum
from policies.models import ExpenseCategory


class SpendType(Enum):
    CAPEX = "CAPEX"
    OPEX = "OPEX"


@dataclass(frozen=True)
class LedgerEntry:
    expense_id: str
    employee_id: str
    department_id: str
    category: ExpenseCategory
    spend_type: SpendType
    usd_amount_cents: int