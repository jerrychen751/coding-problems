const { ExpenseRecord, ExpenseStatus } = require('./models');
const { PolicyAction } = require('../policies/models');

class ExpenseService {
  /**
   * Orchestrates employee validation, FX conversion, policy evaluation, routing, and ledger posting.
   */
  constructor(employeeService, fxService, policyService, routingService, ledgerService) {
    this.employeeService = employeeService;
    this.fxService = fxService;
    this.policyService = policyService;
    this.routingService = routingService;
    this.ledgerService = ledgerService;
    this._records = new Map();
  }

  getExpenseRecord(expenseId) {
    return this._records.get(expenseId) || null;
  }

  submitExpense(expense) {
    const emp = this.employeeService.getEmployee(expense.employeeId);
    if (!emp || !emp.isActive) {
      const record = new ExpenseRecord({
        expense,
        status: ExpenseStatus.REJECTED,
        usdAmount: expense.amount
      });
      this._records.set(expense.expenseId, record);
      return record;
    }

    const evalAmount = expense.amount;

    const { action, ruleId } = this.policyService.evaluatePolicy(
      emp.departmentId,
      expense.category,
      evalAmount,
      emp.role
    );

    let record;
    if (action === PolicyAction.AUTO_APPROVE) {
      record = new ExpenseRecord({
        expense,
        status: ExpenseStatus.APPROVED,
        usdAmount: evalAmount,
        matchedRuleId: ruleId
      });
      this.ledgerService.recordExpense(
        expense.expenseId,
        emp.employeeId,
        emp.departmentId,
        expense.category,
        evalAmount
      );
    } else if (action === PolicyAction.REJECT) {
      record = new ExpenseRecord({
        expense,
        status: ExpenseStatus.REJECTED,
        usdAmount: evalAmount,
        matchedRuleId: ruleId
      });
    } else {
      const chain = this.routingService.buildApprovalChain(
        expense.employeeId,
        evalAmount
      );
      record = new ExpenseRecord({
        expense,
        status: ExpenseStatus.PENDING_APPROVAL,
        usdAmount: evalAmount,
        matchedRuleId: ruleId,
        approverChain: chain.approvers
      });
    }

    this._records.set(expense.expenseId, record);
    return record;
  }

  approveExpense(expenseId, approverId) {
    throw new Error('Not implemented');
  }

  rejectExpense(expenseId, approverId, reason = '') {
    throw new Error('Not implemented');
  }
}

module.exports = { ExpenseService };
