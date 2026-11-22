package expensemanager.expenses;

import expensemanager.currency.Money;

import java.util.*;

public class ExpenseRecord {
    private final Expense expense;
    private ExpenseStatus status;
    private final Money usdAmount;
    private final String matchedRuleId;
    private final List<String> approverChain;
    private int currentStep;
    private final List<Map.Entry<String, String>> approvalHistory;

    public ExpenseRecord(
        Expense expense,
        ExpenseStatus status,
        Money usdAmount,
        String matchedRuleId,
        List<String> approverChain,
        int currentStep,
        List<Map.Entry<String, String>> approvalHistory
    ) {
        this.expense = Objects.requireNonNull(expense);
        this.status = Objects.requireNonNull(status);
        this.usdAmount = Objects.requireNonNull(usdAmount);
        this.matchedRuleId = matchedRuleId;
        this.approverChain = approverChain != null ? new ArrayList<>(approverChain) : new ArrayList<>();
        this.currentStep = currentStep;
        this.approvalHistory = approvalHistory != null ? new ArrayList<>(approvalHistory) : new ArrayList<>();
    }

    public Expense getExpense() {
        return expense;
    }

    public ExpenseStatus getStatus() {
        return status;
    }

    public void setStatus(ExpenseStatus status) {
        this.status = status;
    }

    public Money getUsdAmount() {
        return usdAmount;
    }

    public Optional<String> getMatchedRuleId() {
        return Optional.ofNullable(matchedRuleId);
    }

    public List<String> getApproverChain() {
        return Collections.unmodifiableList(approverChain);
    }

    public int getCurrentStep() {
        return currentStep;
    }

    public void setCurrentStep(int currentStep) {
        this.currentStep = currentStep;
    }

    public List<Map.Entry<String, String>> getApprovalHistory() {
        return Collections.unmodifiableList(approvalHistory);
    }

    public Optional<String> getCurrentRequiredApprover() {
        if (status != ExpenseStatus.PENDING_APPROVAL) {
            return Optional.empty();
        }
        if (currentStep < approverChain.size()) {
            return Optional.of(approverChain.get(currentStep));
        }
        return Optional.empty();
    }
}

