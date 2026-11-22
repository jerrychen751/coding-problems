package expensemanager.routing;

import expensemanager.currency.Money;
import expensemanager.employees.Employee;
import expensemanager.employees.EmployeeService;

import java.util.Collections;
import java.util.Optional;

public class RoutingService {
    private final EmployeeService employeeService;
    private final String financeQueueId;

    public RoutingService(EmployeeService employeeService) {
        this(employeeService, "FINANCE_QUEUE");
    }

    public RoutingService(EmployeeService employeeService, String financeQueueId) {
        this.employeeService = employeeService;
        this.financeQueueId = financeQueueId;
    }

    public ApprovalChain buildApprovalChain(String submitterId, Money usdAmount) {
        Optional<Employee> emp = employeeService.getEmployee(submitterId);
        if (emp.isPresent() && emp.get().getManagerId().isPresent()) {
            return new ApprovalChain(Collections.singletonList(emp.get().getManagerId().get()));
        }
        return new ApprovalChain(Collections.singletonList(financeQueueId));
    }
}

