const { PolicyAction } = require('./models');

class PolicyService {
  constructor(employeeService) {
    this.employeeService = employeeService;
    this._rules = [];
  }

  registerRule(rule) {
    this._rules.push(rule);
  }

  evaluatePolicy(departmentId, category, usdAmount, role = null) {
    /**
     * Evaluates applicable policy rules and returns { action, ruleId }.
     */
    for (const rule of this._rules) {
      if (rule.departmentId === null && rule.category === category) {
        if (rule.maxAmountCents !== null && usdAmount.amountCents < rule.maxAmountCents) {
          return { action: rule.action, ruleId: rule.ruleId };
        }
        return { action: PolicyAction.REQUIRE_APPROVAL, ruleId: rule.ruleId };
      }
    }

    return { action: PolicyAction.REQUIRE_APPROVAL, ruleId: null };
  }
}

module.exports = { PolicyService };
