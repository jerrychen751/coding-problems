const { Role } = require('../employees/models');

const ExpenseCategory = Object.freeze({
  FOOD_AND_BEVERAGE: 'FOOD_AND_BEVERAGE',
  AIRFARE: 'AIRFARE',
  LODGING: 'LODGING',
  SOFTWARE: 'SOFTWARE',
  HARDWARE: 'HARDWARE'
});

const PolicyAction = Object.freeze({
  AUTO_APPROVE: 'AUTO_APPROVE',
  REQUIRE_APPROVAL: 'REQUIRE_APPROVAL',
  REJECT: 'REJECT'
});

class PolicyRule {
  constructor({
    ruleId,
    category,
    action = PolicyAction.AUTO_APPROVE,
    priority = 100,
    departmentId = null,
    role = null,
    maxAmountCents = null,
    minAmountCents = null
  }) {
    this.ruleId = ruleId;
    this.category = category;
    this.action = action;
    this.priority = priority;
    this.departmentId = departmentId;
    this.role = role;
    this.maxAmountCents = maxAmountCents;
    this.minAmountCents = minAmountCents;
    Object.freeze(this);
  }
}

module.exports = {
  ExpenseCategory,
  PolicyAction,
  PolicyRule
};

