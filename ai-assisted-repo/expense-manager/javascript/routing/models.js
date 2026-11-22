class ApprovalChain {
  constructor(approvers = [], requiresFinanceSignoff = false) {
    this.approvers = [...approvers];
    this.requiresFinanceSignoff = requiresFinanceSignoff;
    Object.freeze(this);
  }
}

module.exports = { ApprovalChain };

