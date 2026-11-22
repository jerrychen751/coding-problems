import pytest
from currency.models import Currency, Money
from currency.service import FXService
from employees.models import Department, Employee, Role
from employees.service import EmployeeService
from expenses.models import Expense, ExpenseStatus
from expenses.service import ExpenseService
from ledger.service import LedgerService
from policies.models import ExpenseCategory, PolicyAction, PolicyRule
from policies.service import PolicyService
from routing.service import RoutingService


@pytest.fixture
def system():
    emp_svc = EmployeeService()
    fx_svc = FXService()
    policy_svc = PolicyService(emp_svc)
    routing_svc = RoutingService(emp_svc)
    ledger_svc = LedgerService()
    expense_svc = ExpenseService(emp_svc, fx_svc, policy_svc, routing_svc, ledger_svc)

    emp_svc.register_department(Department("CORP", "Corporate"))
    emp_svc.register_department(Department("ENG", "Engineering", parent_dept_id="CORP"))
    emp_svc.register_department(Department("INFRA", "Infrastructure", parent_dept_id="ENG"))

    emp_svc.register_employee(Employee("e_ceo", "Alice", "CORP", Role.C_LEVEL, title="CEO"))
    emp_svc.register_employee(Employee("e_vp", "Bob", "ENG", Role.VP, title="VP Engineering", manager_id="e_ceo"))
    emp_svc.register_employee(Employee("e_mgr", "Charlie", "INFRA", Role.MANAGER, title="Eng Manager", manager_id="e_vp"))
    emp_svc.register_employee(Employee("e_dev", "David", "INFRA", Role.IC, title="Software Engineer", manager_id="e_mgr"))

    return emp_svc, fx_svc, policy_svc, routing_svc, ledger_svc, expense_svc


def test_exact_boundary_auto_approve(system):
    _, _, policy_svc, _, ledger_svc, expense_svc = system

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_food_20",
            category=ExpenseCategory.FOOD_AND_BEVERAGE,
            max_amount_cents=2_000,
            action=PolicyAction.AUTO_APPROVE,
        )
    )

    exp = Expense("exp_1", "e_dev", Money(2_000, Currency.USD), ExpenseCategory.FOOD_AND_BEVERAGE, "Coffee & Bagel")
    record = expense_svc.submit_expense(exp)

    assert record.status == ExpenseStatus.APPROVED
    assert ledger_svc.get_total_by_category(ExpenseCategory.FOOD_AND_BEVERAGE) == 2_000


def test_foreign_currency_fx_normalization(system):
    _, _, policy_svc, _, ledger_svc, expense_svc = system

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_food_100",
            category=ExpenseCategory.FOOD_AND_BEVERAGE,
            max_amount_cents=10_000,
            action=PolicyAction.AUTO_APPROVE,
        )
    )

    exp = Expense("exp_2", "e_dev", Money(9_500, Currency.EUR), ExpenseCategory.FOOD_AND_BEVERAGE, "Berlin Team Dinner")
    record = expense_svc.submit_expense(exp)

    assert record.status == ExpenseStatus.PENDING_APPROVAL
    assert record.usd_amount.amount_cents == 10_450
    assert ledger_svc.get_total_by_category(ExpenseCategory.FOOD_AND_BEVERAGE) == 0


def test_rejects_non_positive_amounts(system):
    _, _, policy_svc, _, ledger_svc, expense_svc = system

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_food_100",
            category=ExpenseCategory.FOOD_AND_BEVERAGE,
            max_amount_cents=10_000,
            action=PolicyAction.AUTO_APPROVE,
        )
    )

    exp_negative = Expense("exp_neg", "e_dev", Money(-5_000, Currency.USD), ExpenseCategory.FOOD_AND_BEVERAGE, "Refund Spoof")
    record = expense_svc.submit_expense(exp_negative)

    assert record.status == ExpenseStatus.REJECTED
    assert ledger_svc.get_total_by_category(ExpenseCategory.FOOD_AND_BEVERAGE) == 0