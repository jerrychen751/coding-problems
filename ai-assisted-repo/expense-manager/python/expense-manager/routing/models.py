from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class ApprovalChain:
    approvers: List[str] = field(default_factory=list)
    requires_finance_signoff: bool = False