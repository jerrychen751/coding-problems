from currency.models import Currency, Money
from employees.models import Department, Employee, Role
from employees.service import EmployeeService
from routing.service import RoutingService


def test_basic_direct_manager_routing():
    emp_svc = EmployeeService()
    emp_svc.register_department(Department("ENG", "Engineering"))
    emp_svc.register_employee(Employee("e_mgr", "Bob", "ENG", Role.MANAGER))
    emp_svc.register_employee(Employee("e_dev", "Charlie", "ENG", Role.IC, manager_id="e_mgr"))

    routing_svc = RoutingService(emp_svc)
    chain = routing_svc.build_approval_chain("e_dev", Money(50000, Currency.USD))
    assert chain.approvers == ["e_mgr"]