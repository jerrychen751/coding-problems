from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple
from currency.models import Money
from policies.models import ExpenseCategory, PolicyAction


class ExpenseStatus(Enum):
    APPROVED = "APPROVED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class Expense:
    expense_id: str
    employee_id: str
    amount: Money
    category: ExpenseCategory
    merchant: str


@dataclass
class ExpenseRecord:
    expense: Expense
    status: ExpenseStatus
    usd_amount: Money
    matched_rule_id: Optional[str] = None
    approver_chain: List[str] = field(default_factory=list)
    current_step: int = 0
    approval_history: List[Tuple[str, str]] = field(default_factory=list)

    @property
    def current_required_approver(self) -> Optional[str]:
        if self.status != ExpenseStatus.PENDING_APPROVAL:
            return None
        if self.current_step < len(self.approver_chain):
            return self.approver_chain[self.current_step]
        return None