package expensemanager.expenses;

import expensemanager.currency.Money;
import expensemanager.policies.ExpenseCategory;

import java.util.Objects;

public class Expense {
    private final String expenseId;
    private final String employeeId;
    private final Money amount;
    private final ExpenseCategory category;
    private final String merchant;

    public Expense(
        String expenseId,
        String employeeId,
        Money amount,
        ExpenseCategory category,
        String merchant
    ) {
        this.expenseId = Objects.requireNonNull(expenseId);
        this.employeeId = Objects.requireNonNull(employeeId);
        this.amount = Objects.requireNonNull(amount);
        this.category = Objects.requireNonNull(category);
        this.merchant = Objects.requireNonNull(merchant);
    }

    public String getExpenseId() {
        return expenseId;
    }

    public String getEmployeeId() {
        return employeeId;
    }

    public Money getAmount() {
        return amount;
    }

    public ExpenseCategory getCategory() {
        return category;
    }

    public String getMerchant() {
        return merchant;
    }
}

