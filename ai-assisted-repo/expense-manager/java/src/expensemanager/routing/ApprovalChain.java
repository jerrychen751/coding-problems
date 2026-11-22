package expensemanager.routing;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ApprovalChain {
    private final List<String> approvers;
    private final boolean requiresFinanceSignoff;

    public ApprovalChain() {
        this(Collections.emptyList(), false);
    }

    public ApprovalChain(List<String> approvers) {
        this(approvers, false);
    }

    public ApprovalChain(List<String> approvers, boolean requiresFinanceSignoff) {
        this.approvers = Collections.unmodifiableList(new ArrayList<>(approvers));
        this.requiresFinanceSignoff = requiresFinanceSignoff;
    }

    public List<String> getApprovers() {
        return approvers;
    }

    public boolean isRequiresFinanceSignoff() {
        return requiresFinanceSignoff;
    }
}

