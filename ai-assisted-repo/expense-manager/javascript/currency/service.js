const { Currency, Money } = require('./models');

class FXService {
  /**
   * Provides currency conversion into normalized USD cents.
   */
  constructor() {
    this._rates = {
      [Currency.USD]: 1.0,
      [Currency.EUR]: 1.10, // 1 EUR = 1.10 USD
      [Currency.GBP]: 1.30, // 1 GBP = 1.30 USD
      [Currency.CAD]: 0.75  // 1 CAD = 0.75 USD
    };
  }

  convertToUsd(money) {
    if (money.currency === Currency.USD) {
      return money;
    }
    const rate = this._rates[money.currency];
    if (rate === undefined) {
      throw new Error(`Unsupported currency: ${money.currency}`);
    }
    const convertedCents = Math.trunc(money.amountCents * rate);
    return new Money(convertedCents, Currency.USD);
  }
}

module.exports = { FXService };
