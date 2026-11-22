package expensemanager.policies;

import expensemanager.currency.Money;
import expensemanager.employees.EmployeeService;
import expensemanager.employees.Role;

import java.util.ArrayList;
import java.util.List;

public class PolicyService {
    private final EmployeeService employeeService;
    private final List<PolicyRule> rules = new ArrayList<>();

    public PolicyService(EmployeeService employeeService) {
        this.employeeService = employeeService;
    }

    public void registerRule(PolicyRule rule) {
        rules.add(rule);
    }

    public PolicyEvaluation evaluatePolicy(String departmentId, ExpenseCategory category, Money usdAmount) {
        return evaluatePolicy(departmentId, category, usdAmount, null);
    }

    public PolicyEvaluation evaluatePolicy(
        String departmentId,
        ExpenseCategory category,
        Money usdAmount,
        Role role
    ) {
        for (PolicyRule rule : rules) {
            if (rule.getDepartmentId().isEmpty() && rule.getCategory() == category) {
                if (rule.getMaxAmountCents().isPresent() && usdAmount.getAmountCents() < rule.getMaxAmountCents().get()) {
                    return new PolicyEvaluation(rule.getAction(), rule.getRuleId());
                }
                return new PolicyEvaluation(PolicyAction.REQUIRE_APPROVAL, rule.getRuleId());
            }
        }

        return new PolicyEvaluation(PolicyAction.REQUIRE_APPROVAL, null);
    }
}
