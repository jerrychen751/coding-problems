from typing import Dict, Optional
from currency.service import FXService
from employees.service import EmployeeService
from expenses.models import Expense, ExpenseRecord, ExpenseStatus
from ledger.service import LedgerService
from policies.models import PolicyAction
from policies.service import PolicyService
from routing.service import RoutingService


class ExpenseService:
    """Orchestrates employee validation, FX conversion, policy evaluation, routing, and ledger posting."""

    def __init__(
        self,
        employee_service: EmployeeService,
        fx_service: FXService,
        policy_service: PolicyService,
        routing_service: RoutingService,
        ledger_service: LedgerService,
    ):
        self.employee_service = employee_service
        self.fx_service = fx_service
        self.policy_service = policy_service
        self.routing_service = routing_service
        self.ledger_service = ledger_service
        self._records: Dict[str, ExpenseRecord] = {}

    def get_expense_record(self, expense_id: str) -> Optional[ExpenseRecord]:
        return self._records.get(expense_id)

    def submit_expense(self, expense: Expense) -> ExpenseRecord:
        emp = self.employee_service.get_employee(expense.employee_id)
        if not emp or not emp.is_active or expense.amount.amount_cents <= 0:
            record = ExpenseRecord(
                expense=expense,
                status=ExpenseStatus.REJECTED,
                usd_amount=expense.amount,
            )
            self._records[expense.expense_id] = record
            return record

        eval_amount = self.fx_service.convert_to_usd(expense.amount)

        action, rule_id = self.policy_service.evaluate_policy(
            department_id=emp.department_id,
            category=expense.category,
            usd_amount=eval_amount,
            role=emp.role,
        )

        if action == PolicyAction.AUTO_APPROVE:
            record = ExpenseRecord(
                expense=expense,
                status=ExpenseStatus.APPROVED,
                usd_amount=eval_amount,
                matched_rule_id=rule_id,
            )
            self.ledger_service.record_expense(
                expense_id=expense.expense_id,
                employee_id=emp.employee_id,
                department_id=emp.department_id,
                category=expense.category,
                usd_amount=eval_amount,
            )
        elif action == PolicyAction.REJECT:
            record = ExpenseRecord(
                expense=expense,
                status=ExpenseStatus.REJECTED,
                usd_amount=eval_amount,
                matched_rule_id=rule_id,
            )
        else:
            chain = self.routing_service.build_approval_chain(
                submitter_id=expense.employee_id,
                usd_amount=eval_amount,
            )
            record = ExpenseRecord(
                expense=expense,
                status=ExpenseStatus.PENDING_APPROVAL,
                usd_amount=eval_amount,
                matched_rule_id=rule_id,
                approver_chain=chain.approvers,
            )

        self._records[expense.expense_id] = record
        return record

    def approve_expense(self, expense_id: str, approver_id: str) -> ExpenseRecord:
        raise NotImplementedError

    def reject_expense(self, expense_id: str, approver_id: str, reason: str = "") -> ExpenseRecord:
        raise NotImplementedError