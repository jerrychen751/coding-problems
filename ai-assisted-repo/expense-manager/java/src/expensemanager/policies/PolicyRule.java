package expensemanager.policies;

import expensemanager.employees.Role;

import java.util.Objects;
import java.util.Optional;

public class PolicyRule {
    private final String ruleId;
    private final ExpenseCategory category;
    private final PolicyAction action;
    private final int priority;
    private final String departmentId;
    private final Role role;
    private final Long maxAmountCents;
    private final Long minAmountCents;

    public static class Builder {
        private final String ruleId;
        private final ExpenseCategory category;
        private PolicyAction action = PolicyAction.AUTO_APPROVE;
        private int priority = 100;
        private String departmentId = null;
        private Role role = null;
        private Long maxAmountCents = null;
        private Long minAmountCents = null;

        public Builder(String ruleId, ExpenseCategory category) {
            this.ruleId = Objects.requireNonNull(ruleId, "ruleId cannot be null");
            this.category = Objects.requireNonNull(category, "category cannot be null");
        }

        public Builder action(PolicyAction action) {
            this.action = action;
            return this;
        }

        public Builder priority(int priority) {
            this.priority = priority;
            return this;
        }

        public Builder departmentId(String departmentId) {
            this.departmentId = departmentId;
            return this;
        }

        public Builder role(Role role) {
            this.role = role;
            return this;
        }

        public Builder maxAmountCents(long maxAmountCents) {
            this.maxAmountCents = maxAmountCents;
            return this;
        }

        public Builder minAmountCents(long minAmountCents) {
            this.minAmountCents = minAmountCents;
            return this;
        }

        public PolicyRule build() {
            return new PolicyRule(this);
        }
    }

    private PolicyRule(Builder builder) {
        this.ruleId = builder.ruleId;
        this.category = builder.category;
        this.action = builder.action;
        this.priority = builder.priority;
        this.departmentId = builder.departmentId;
        this.role = builder.role;
        this.maxAmountCents = builder.maxAmountCents;
        this.minAmountCents = builder.minAmountCents;
    }

    public String getRuleId() {
        return ruleId;
    }

    public ExpenseCategory getCategory() {
        return category;
    }

    public PolicyAction getAction() {
        return action;
    }

    public int getPriority() {
        return priority;
    }

    public Optional<String> getDepartmentId() {
        return Optional.ofNullable(departmentId);
    }

    public Optional<Role> getRole() {
        return Optional.ofNullable(role);
    }

    public Optional<Long> getMaxAmountCents() {
        return Optional.ofNullable(maxAmountCents);
    }

    public Optional<Long> getMinAmountCents() {
        return Optional.ofNullable(minAmountCents);
    }
}

