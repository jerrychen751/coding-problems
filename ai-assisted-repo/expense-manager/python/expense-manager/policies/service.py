from typing import List, Optional, Tuple
from currency.models import Money
from employees.models import Role
from employees.service import EmployeeService
from policies.models import ExpenseCategory, PolicyAction, PolicyRule


class PolicyService:
    def __init__(self, employee_service: EmployeeService):
        self.employee_service = employee_service
        self._rules: List[PolicyRule] = []

    def register_rule(self, rule: PolicyRule) -> None:
        self._rules.append(rule)

    def evaluate_policy(
        self,
        department_id: str,
        category: ExpenseCategory,
        usd_amount: Money,
        role: Optional[Role] = None,
    ) -> Tuple[PolicyAction, Optional[str]]:
        """
        Evaluates applicable policy rules and returns (PolicyAction, matched_rule_id).

        Unconditional rules are resolved first and, if any match, win outright over every
        overridable rule, however specific. Within a tier, a role-specific rule beats a
        role-agnostic one, a rule scoped to a closer department beats one scoped to an
        ancestor department, and priority (ascending) breaks any remaining tie.
        """
        dept_chain = self.employee_service.get_department_hierarchy(department_id)
        candidates = [
            rule
            for rule in self._rules
            if self._rule_matches(rule, category, usd_amount, dept_chain, role)
        ]

        for tier in (
            [rule for rule in candidates if rule.unconditional],
            [rule for rule in candidates if not rule.unconditional],
        ):
            best = self._best_rule(tier, dept_chain)
            if best is not None:
                return best.action, best.rule_id

        return PolicyAction.REQUIRE_APPROVAL, None

    def _rule_matches(
        self,
        rule: PolicyRule,
        category: ExpenseCategory,
        usd_amount: Money,
        dept_chain: List[str],
        role: Optional[Role],
    ) -> bool:
        if rule.category != category:
            return False
        if rule.department_id is not None and rule.department_id not in dept_chain:
            return False
        if rule.role is not None and rule.role != role:
            return False
        if rule.min_amount_cents is not None and usd_amount.amount_cents < rule.min_amount_cents:
            return False
        if rule.max_amount_cents is not None and usd_amount.amount_cents > rule.max_amount_cents:
            return False
        return True

    def _best_rule(self, rules: List[PolicyRule], dept_chain: List[str]) -> Optional[PolicyRule]:
        if not rules:
            return None

        def rank(rule: PolicyRule) -> Tuple[int, int, int]:
            role_rank = 0 if rule.role is not None else 1
            department_rank = (
                dept_chain.index(rule.department_id) if rule.department_id is not None else len(dept_chain)
            )
            return role_rank, department_rank, rule.priority

        return min(rules, key=rank)