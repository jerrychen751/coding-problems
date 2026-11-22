from currency.models import Money
from employees.service import EmployeeService
from routing.models import ApprovalChain


class RoutingService:
    def __init__(self, employee_service: EmployeeService, finance_queue_id: str = "FINANCE_QUEUE"):
        self.employee_service = employee_service
        self.finance_queue_id = finance_queue_id

    def build_approval_chain(self, submitter_id: str, usd_amount: Money) -> ApprovalChain:
        emp = self.employee_service.get_employee(submitter_id)
        if emp and emp.manager_id:
            return ApprovalChain(approvers=[emp.manager_id])
        return ApprovalChain(approvers=[self.finance_queue_id])