const Currency = Object.freeze({
  USD: 'USD',
  EUR: 'EUR',
  GBP: 'GBP',
  CAD: 'CAD'
});

class Money {
  constructor(amountCents, currency = Currency.USD) {
    this.amountCents = amountCents;
    this.currency = currency;
    Object.freeze(this);
  }

  _checkCurrency(other) {
    if (this.currency !== other.currency) {
      throw new Error(
        `Cannot compare money across currencies without conversion: ${this.currency} vs ${other.currency}`
      );
    }
  }

  isLessThan(other) {
    this._checkCurrency(other);
    return this.amountCents < other.amountCents;
  }

  isLessThanOrEqual(other) {
    this._checkCurrency(other);
    return this.amountCents <= other.amountCents;
  }

  equals(other) {
    return (
      other instanceof Money &&
      this.currency === other.currency &&
      this.amountCents === other.amountCents
    );
  }
}

module.exports = {
  Currency,
  Money
};

