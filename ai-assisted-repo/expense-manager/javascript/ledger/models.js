const SpendType = Object.freeze({
  CAPEX: 'CAPEX',
  OPEX: 'OPEX'
});

class LedgerEntry {
  constructor({
    expenseId,
    employeeId,
    departmentId,
    category,
    spendType,
    usdAmountCents
  }) {
    this.expenseId = expenseId;
    this.employeeId = employeeId;
    this.departmentId = departmentId;
    this.category = category;
    this.spendType = spendType;
    this.usdAmountCents = usdAmountCents;
    Object.freeze(this);
  }
}

module.exports = {
  SpendType,
  LedgerEntry
};

