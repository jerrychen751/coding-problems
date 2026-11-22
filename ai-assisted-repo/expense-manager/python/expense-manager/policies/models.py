from dataclasses import dataclass
from enum import Enum
from typing import Optional
from employees.models import Role


class ExpenseCategory(Enum):
    FOOD_AND_BEVERAGE = "FOOD_AND_BEVERAGE"
    AIRFARE = "AIRFARE"
    LODGING = "LODGING"
    SOFTWARE = "SOFTWARE"
    HARDWARE = "HARDWARE"


class PolicyAction(Enum):
    AUTO_APPROVE = "AUTO_APPROVE"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    REJECT = "REJECT"


@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    category: ExpenseCategory
    action: PolicyAction = PolicyAction.AUTO_APPROVE
    priority: int = 100
    department_id: Optional[str] = None      # None = Global Company-wide Baseline
    role: Optional[Role] = None              # None = Matches any role
    max_amount_cents: Optional[int] = None   # None = Applies regardless of amount
    min_amount_cents: Optional[int] = None
    unconditional: bool = False              # Beats every overridable rule, even a more specific one

    def __post_init__(self):
        if self.priority < 0:
            raise ValueError(f"priority must be non-negative, got {self.priority}")

