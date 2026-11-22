package expensemanager.ledger;

import expensemanager.policies.ExpenseCategory;

import java.util.Objects;

public class LedgerEntry {
    private final String expenseId;
    private final String employeeId;
    private final String departmentId;
    private final ExpenseCategory category;
    private final SpendType spendType;
    private final long usdAmountCents;

    public LedgerEntry(
        String expenseId,
        String employeeId,
        String departmentId,
        ExpenseCategory category,
        SpendType spendType,
        long usdAmountCents
    ) {
        this.expenseId = Objects.requireNonNull(expenseId);
        this.employeeId = Objects.requireNonNull(employeeId);
        this.departmentId = Objects.requireNonNull(departmentId);
        this.category = Objects.requireNonNull(category);
        this.spendType = Objects.requireNonNull(spendType);
        this.usdAmountCents = usdAmountCents;
    }

    public String getExpenseId() {
        return expenseId;
    }

    public String getEmployeeId() {
        return employeeId;
    }

    public String getDepartmentId() {
        return departmentId;
    }

    public ExpenseCategory getCategory() {
        return category;
    }

    public SpendType getSpendType() {
        return spendType;
    }

    public long getUsdAmountCents() {
        return usdAmountCents;
    }
}

