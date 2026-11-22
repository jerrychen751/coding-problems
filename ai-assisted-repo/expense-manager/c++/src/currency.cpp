#include "expense_manager/currency.hpp"

namespace expense_manager {

FXService::FXService() {
    rates_[Currency::USD] = 1.0;
    rates_[Currency::EUR] = 1.10; // 1 EUR = 1.10 USD
    rates_[Currency::GBP] = 1.30; // 1 GBP = 1.30 USD
    rates_[Currency::CAD] = 0.75; // 1 CAD = 0.75 USD
}

Money FXService::convert_to_usd(const Money& money) const {
    if (money.currency == Currency::USD) {
        return money;
    }
    auto it = rates_.find(money.currency);
    if (it == rates_.end()) {
        throw std::invalid_argument("Unsupported currency");
    }
    int64_t converted_cents = static_cast<int64_t>(money.amount_cents * it->second);
    return Money(converted_cents, Currency::USD);
}

} // namespace expense_manager
