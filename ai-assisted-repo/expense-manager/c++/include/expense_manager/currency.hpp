#pragma once

#include <string>
#include <unordered_map>
#include <stdexcept>
#include <cmath>
#include <iostream>

namespace expense_manager {

enum class Currency {
    USD,
    EUR,
    GBP,
    CAD
};

inline std::ostream& operator<<(std::ostream& os, const Currency& cur) {
    switch (cur) {
        case Currency::USD: return os << "USD";
        case Currency::EUR: return os << "EUR";
        case Currency::GBP: return os << "GBP";
        case Currency::CAD: return os << "CAD";
    }
    return os << "UNKNOWN";
}

struct Money {
    int64_t amount_cents{0};
    Currency currency{Currency::USD};

    Money() = default;
    Money(int64_t cents, Currency cur = Currency::USD)
        : amount_cents(cents), currency(cur) {}

    bool operator==(const Money& o) const {
        return amount_cents == o.amount_cents && currency == o.currency;
    }

    bool operator!=(const Money& o) const {
        return !(*this == o);
    }

    bool operator<(const Money& o) const {
        if (currency != o.currency) {
            throw std::invalid_argument("Cannot compare money across currencies without conversion");
        }
        return amount_cents < o.amount_cents;
    }

    bool operator<=(const Money& o) const {
        return *this == o || *this < o;
    }
};

class FXService {
public:
    FXService();
    Money convert_to_usd(const Money& money) const;

private:
    std::unordered_map<Currency, double> rates_;
};

} // namespace expense_manager

