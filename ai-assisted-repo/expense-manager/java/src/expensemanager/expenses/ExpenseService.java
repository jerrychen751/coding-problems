package expensemanager.expenses;

import expensemanager.currency.FXService;
import expensemanager.currency.Money;
import expensemanager.employees.Employee;
import expensemanager.employees.EmployeeService;
import expensemanager.ledger.LedgerService;
import expensemanager.policies.PolicyAction;
import expensemanager.policies.PolicyEvaluation;
import expensemanager.policies.PolicyService;
import expensemanager.routing.ApprovalChain;
import expensemanager.routing.RoutingService;

import java.util.*;

public class ExpenseService {
    private final EmployeeService employeeService;
    private final FXService fxService;
    private final PolicyService policyService;
    private final RoutingService routingService;
    private final LedgerService ledgerService;
    private final Map<String, ExpenseRecord> records = new HashMap<>();

    public ExpenseService(
        EmployeeService employeeService,
        FXService fxService,
        PolicyService policyService,
        RoutingService routingService,
        LedgerService ledgerService
    ) {
        this.employeeService = employeeService;
        this.fxService = fxService;
        this.policyService = policyService;
        this.routingService = routingService;
        this.ledgerService = ledgerService;
    }

    public Optional<ExpenseRecord> getExpenseRecord(String expenseId) {
        return Optional.ofNullable(records.get(expenseId));
    }

    public ExpenseRecord submitExpense(Expense expense) {
        Optional<Employee> emp = employeeService.getEmployee(expense.getEmployeeId());
        if (emp.isEmpty() || !emp.get().isActive()) {
            ExpenseRecord record = new ExpenseRecord(
                expense,
                ExpenseStatus.REJECTED,
                expense.getAmount(),
                null,
                Collections.emptyList(),
                0,
                Collections.emptyList()
            );
            records.put(expense.getExpenseId(), record);
            return record;
        }

        Money evalAmount = expense.getAmount();

        PolicyEvaluation evaluation = policyService.evaluatePolicy(
            emp.get().getDepartmentId(),
            expense.getCategory(),
            evalAmount,
            emp.get().getRole()
        );

        ExpenseRecord record;
        if (evaluation.getAction() == PolicyAction.AUTO_APPROVE) {
            record = new ExpenseRecord(
                expense,
                ExpenseStatus.APPROVED,
                evalAmount,
                evaluation.getMatchedRuleId().orElse(null),
                Collections.emptyList(),
                0,
                Collections.emptyList()
            );
            ledgerService.recordExpense(
                expense.getExpenseId(),
                emp.get().getEmployeeId(),
                emp.get().getDepartmentId(),
                expense.getCategory(),
                evalAmount
            );
        } else if (evaluation.getAction() == PolicyAction.REJECT) {
            record = new ExpenseRecord(
                expense,
                ExpenseStatus.REJECTED,
                evalAmount,
                evaluation.getMatchedRuleId().orElse(null),
                Collections.emptyList(),
                0,
                Collections.emptyList()
            );
        } else {
            ApprovalChain chain = routingService.buildApprovalChain(
                expense.getEmployeeId(),
                evalAmount
            );
            record = new ExpenseRecord(
                expense,
                ExpenseStatus.PENDING_APPROVAL,
                evalAmount,
                evaluation.getMatchedRuleId().orElse(null),
                chain.getApprovers(),
                0,
                Collections.emptyList()
            );
        }

        records.put(expense.getExpenseId(), record);
        return record;
    }

    public ExpenseRecord approveExpense(String expenseId, String approverId) {
        throw new UnsupportedOperationException("Not implemented");
    }

    public ExpenseRecord rejectExpense(String expenseId, String approverId) {
        return rejectExpense(expenseId, approverId, "");
    }

    public ExpenseRecord rejectExpense(String expenseId, String approverId, String reason) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
