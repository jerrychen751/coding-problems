const ExpenseStatus = Object.freeze({
  APPROVED: 'APPROVED',
  PENDING_APPROVAL: 'PENDING_APPROVAL',
  REJECTED: 'REJECTED'
});

class Expense {
  constructor(expenseId, employeeId, amount, category, merchant) {
    this.expenseId = expenseId;
    this.employeeId = employeeId;
    this.amount = amount;
    this.category = category;
    this.merchant = merchant;
    Object.freeze(this);
  }
}

class ExpenseRecord {
  constructor({
    expense,
    status,
    usdAmount,
    matchedRuleId = null,
    approverChain = [],
    currentStep = 0,
    approvalHistory = []
  }) {
    this.expense = expense;
    this.status = status;
    this.usdAmount = usdAmount;
    this.matchedRuleId = matchedRuleId;
    this.approverChain = [...approverChain];
    this.currentStep = currentStep;
    this.approvalHistory = [...approvalHistory];
  }

  get currentRequiredApprover() {
    if (this.status !== ExpenseStatus.PENDING_APPROVAL) {
      return null;
    }
    if (this.currentStep < this.approverChain.length) {
      return this.approverChain[this.currentStep];
    }
    return null;
  }
}

module.exports = {
  ExpenseStatus,
  Expense,
  ExpenseRecord
};

