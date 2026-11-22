package expensemanager.policies;

import java.util.Optional;

public class PolicyEvaluation {
    private final PolicyAction action;
    private final String matchedRuleId;

    public PolicyEvaluation(PolicyAction action, String matchedRuleId) {
        this.action = action;
        this.matchedRuleId = matchedRuleId;
    }

    public PolicyAction getAction() {
        return action;
    }

    public Optional<String> getMatchedRuleId() {
        return Optional.ofNullable(matchedRuleId);
    }
}

