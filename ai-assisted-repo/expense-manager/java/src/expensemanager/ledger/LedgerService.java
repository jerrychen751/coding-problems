package expensemanager.ledger;

import expensemanager.currency.Currency;
import expensemanager.currency.Money;
import expensemanager.policies.ExpenseCategory;

import java.util.*;

public class LedgerService {
    public static final Set<ExpenseCategory> CAPEX_CATEGORIES = Collections.unmodifiableSet(
        EnumSet.of(ExpenseCategory.HARDWARE, ExpenseCategory.SOFTWARE)
    );

    private final Map<String, LedgerEntry> entries = new HashMap<>();

    public LedgerEntry recordExpense(
        String expenseId,
        String employeeId,
        String departmentId,
        ExpenseCategory category,
        Money usdAmount
    ) {
        if (usdAmount.getCurrency() != Currency.USD) {
            throw new IllegalArgumentException("Ledger entries must be normalized to USD before posting.");
        }
        if (entries.containsKey(expenseId)) {
            throw new IllegalArgumentException("Expense " + expenseId + " has already been posted to the ledger.");
        }

        SpendType spendType = CAPEX_CATEGORIES.contains(category) ? SpendType.CAPEX : SpendType.OPEX;
        LedgerEntry entry = new LedgerEntry(
            expenseId,
            employeeId,
            departmentId,
            category,
            spendType,
            usdAmount.getAmountCents()
        );
        entries.put(expenseId, entry);
        return entry;
    }

    public long getTotalByCategory(ExpenseCategory category) {
        return entries.values().stream()
            .filter(e -> e.getCategory() == category)
            .mapToLong(LedgerEntry::getUsdAmountCents)
            .sum();
    }

    public long getTotalCapex() {
        return getTotalCapex(null);
    }

    public long getTotalCapex(String departmentId) {
        return entries.values().stream()
            .filter(e -> (e.getSpendType() == SpendType.CAPEX && departmentId == null) || e.getDepartmentId().equals(departmentId))
            .mapToLong(LedgerEntry::getUsdAmountCents)
            .sum();
    }
}
