from currency.models import Currency, Money
from employees.models import Department, Role
from employees.service import EmployeeService
from policies.models import ExpenseCategory, PolicyAction, PolicyRule
from policies.service import PolicyService


def test_default_fallback_requires_approval():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("CORP", "Corp"))
    policy_svc = PolicyService(emp_svc)

    action, rule_id = policy_svc.evaluate_policy(
        "CORP", ExpenseCategory.LODGING, Money(15000, Currency.USD)
    )
    assert action == PolicyAction.REQUIRE_APPROVAL
    assert rule_id is None


def test_policy_exact_boundary_and_priority_order():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("CORP", "Corp"))
    policy_svc = PolicyService(emp_svc)

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_meal_auto",
            category=ExpenseCategory.FOOD_AND_BEVERAGE,
            max_amount_cents=5_000,
            action=PolicyAction.AUTO_APPROVE,
            priority=100,
        )
    )
    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_meal_ban",
            category=ExpenseCategory.FOOD_AND_BEVERAGE,
            min_amount_cents=50_000,
            action=PolicyAction.REJECT,
            priority=10,
        )
    )

    action_50, rule_50 = policy_svc.evaluate_policy(
        "CORP", ExpenseCategory.FOOD_AND_BEVERAGE, Money(5_000, Currency.USD)
    )
    assert action_50 == PolicyAction.AUTO_APPROVE
    assert rule_50 == "r_meal_auto"

    action_600, rule_600 = policy_svc.evaluate_policy(
        "CORP", ExpenseCategory.FOOD_AND_BEVERAGE, Money(60_000, Currency.USD)
    )
    assert action_600 == PolicyAction.REJECT
    assert rule_600 == "r_meal_ban"


def test_unconditional_rule_beats_more_specific_overridable_rule():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("ENG", "Engineering"))
    policy_svc = PolicyService(emp_svc)

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_eng_airfare_auto",
            category=ExpenseCategory.AIRFARE,
            action=PolicyAction.AUTO_APPROVE,
            department_id="ENG",
        )
    )
    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_airfare_always_approval",
            category=ExpenseCategory.AIRFARE,
            action=PolicyAction.REQUIRE_APPROVAL,
            unconditional=True,
        )
    )

    action, rule_id = policy_svc.evaluate_policy(
        "ENG", ExpenseCategory.AIRFARE, Money(80_000, Currency.USD)
    )
    assert action == PolicyAction.REQUIRE_APPROVAL
    assert rule_id == "r_airfare_always_approval"


def test_department_specificity_child_beats_parent_beats_global():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("ENG", "Engineering"))
    emp_svc.register_department(Department("INFRA", "Infra", parent_dept_id="ENG"))
    emp_svc.register_department(Department("CORP", "Corp"))
    policy_svc = PolicyService(emp_svc)

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_global_lodging",
            category=ExpenseCategory.LODGING,
            action=PolicyAction.AUTO_APPROVE,
            max_amount_cents=20_000,
        )
    )
    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_eng_lodging",
            category=ExpenseCategory.LODGING,
            action=PolicyAction.AUTO_APPROVE,
            department_id="ENG",
            max_amount_cents=20_000,
        )
    )
    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_infra_lodging",
            category=ExpenseCategory.LODGING,
            action=PolicyAction.AUTO_APPROVE,
            department_id="INFRA",
            max_amount_cents=20_000,
        )
    )

    _, rule_infra = policy_svc.evaluate_policy(
        "INFRA", ExpenseCategory.LODGING, Money(15_000, Currency.USD)
    )
    assert rule_infra == "r_infra_lodging"

    _, rule_eng = policy_svc.evaluate_policy(
        "ENG", ExpenseCategory.LODGING, Money(15_000, Currency.USD)
    )
    assert rule_eng == "r_eng_lodging"

    _, rule_corp = policy_svc.evaluate_policy(
        "CORP", ExpenseCategory.LODGING, Money(15_000, Currency.USD)
    )
    assert rule_corp == "r_global_lodging"


def test_role_specificity_beats_role_agnostic_within_department():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("ENG", "Engineering"))
    policy_svc = PolicyService(emp_svc)

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_eng_any_role",
            category=ExpenseCategory.SOFTWARE,
            action=PolicyAction.REQUIRE_APPROVAL,
            department_id="ENG",
        )
    )
    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_eng_manager",
            category=ExpenseCategory.SOFTWARE,
            action=PolicyAction.AUTO_APPROVE,
            department_id="ENG",
            role=Role.MANAGER,
        )
    )

    action_mgr, rule_mgr = policy_svc.evaluate_policy(
        "ENG", ExpenseCategory.SOFTWARE, Money(10_000, Currency.USD), role=Role.MANAGER
    )
    assert action_mgr == PolicyAction.AUTO_APPROVE
    assert rule_mgr == "r_eng_manager"

    action_ic, rule_ic = policy_svc.evaluate_policy(
        "ENG", ExpenseCategory.SOFTWARE, Money(10_000, Currency.USD), role=Role.IC
    )
    assert action_ic == PolicyAction.REQUIRE_APPROVAL
    assert rule_ic == "r_eng_any_role"


def test_role_specificity_outranks_department_specificity():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("ENG", "Engineering"))
    emp_svc.register_department(Department("INFRA", "Infra", parent_dept_id="ENG"))
    policy_svc = PolicyService(emp_svc)

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_infra_any_role",
            category=ExpenseCategory.HARDWARE,
            action=PolicyAction.AUTO_APPROVE,
            department_id="INFRA",
        )
    )
    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_eng_manager",
            category=ExpenseCategory.HARDWARE,
            action=PolicyAction.REQUIRE_APPROVAL,
            department_id="ENG",
            role=Role.MANAGER,
        )
    )

    action, rule_id = policy_svc.evaluate_policy(
        "INFRA", ExpenseCategory.HARDWARE, Money(10_000, Currency.USD), role=Role.MANAGER
    )
    assert action == PolicyAction.REQUIRE_APPROVAL
    assert rule_id == "r_eng_manager"


def test_rule_scoped_to_unrelated_department_never_matches():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("ENG", "Engineering"))
    emp_svc.register_department(Department("INFRA", "Infra", parent_dept_id="ENG"))
    emp_svc.register_department(Department("SALES", "Sales"))
    policy_svc = PolicyService(emp_svc)

    policy_svc.register_rule(
        PolicyRule(
            rule_id="r_sales_only",
            category=ExpenseCategory.SOFTWARE,
            action=PolicyAction.AUTO_APPROVE,
            department_id="SALES",
        )
    )

    action, rule_id = policy_svc.evaluate_policy(
        "INFRA", ExpenseCategory.SOFTWARE, Money(10_000, Currency.USD)
    )
    assert action == PolicyAction.REQUIRE_APPROVAL
    assert rule_id is None