const { Currency } = require('../currency/models');
const { ExpenseCategory } = require('../policies/models');
const { SpendType, LedgerEntry } = require('./models');

const CAPEX_CATEGORIES = new Set([ExpenseCategory.HARDWARE, ExpenseCategory.SOFTWARE]);

class LedgerService {
  /**
   * Tracks finalized, approved company expenses by category and CapEx/OpEx classification.
   */
  constructor() {
    this._entries = new Map();
  }

  recordExpense(expenseId, employeeId, departmentId, category, usdAmount) {
    if (usdAmount.currency !== Currency.USD) {
      throw new Error('Ledger entries must be normalized to USD before posting.');
    }
    if (this._entries.has(expenseId)) {
      throw new Error(`Expense ${expenseId} has already been posted to the ledger.`);
    }

    const spendType = CAPEX_CATEGORIES.has(category) ? SpendType.CAPEX : SpendType.OPEX;
    const entry = new LedgerEntry({
      expenseId,
      employeeId,
      departmentId,
      category,
      spendType,
      usdAmountCents: usdAmount.amountCents
    });
    this._entries.set(expenseId, entry);
    return entry;
  }

  getTotalByCategory(category) {
    let total = 0;
    for (const entry of this._entries.values()) {
      if (entry.category === category) {
        total += entry.usdAmountCents;
      }
    }
    return total;
  }

  getTotalCapex(departmentId = null) {
    let total = 0;
    for (const entry of this._entries.values()) {
      if (
        (entry.spendType === SpendType.CAPEX && departmentId === null) ||
        entry.departmentId === departmentId
      ) {
        total += entry.usdAmountCents;
      }
    }
    return total;
  }
}

module.exports = {
  CAPEX_CATEGORIES,
  LedgerService
};
