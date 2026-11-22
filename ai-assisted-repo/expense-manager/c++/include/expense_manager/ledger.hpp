#pragma once

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <optional>
#include <iostream>
#include "policies.hpp"
#include "currency.hpp"

namespace expense_manager {

enum class SpendType {
    CAPEX,
    OPEX
};

inline std::ostream& operator<<(std::ostream& os, const SpendType& st) {
    switch (st) {
        case SpendType::CAPEX: return os << "CAPEX";
        case SpendType::OPEX: return os << "OPEX";
    }
    return os << "UNKNOWN";
}

struct LedgerEntry {
    std::string expense_id;
    std::string employee_id;
    std::string department_id;
    ExpenseCategory category;
    SpendType spend_type;
    int64_t usd_amount_cents;

    LedgerEntry() = default;
    LedgerEntry(std::string exp_id, std::string emp_id, std::string dept_id,
                ExpenseCategory cat, SpendType st, int64_t cents)
        : expense_id(std::move(exp_id)), employee_id(std::move(emp_id)),
          department_id(std::move(dept_id)), category(cat),
          spend_type(st), usd_amount_cents(cents) {}
};

class LedgerService {
public:
    LedgerEntry record_expense(const std::string& expense_id,
                               const std::string& employee_id,
                               const std::string& department_id,
                               ExpenseCategory category,
                               const Money& usd_amount);

    int64_t get_total_by_category(ExpenseCategory category) const;
    int64_t get_total_capex(const std::optional<std::string>& department_id = std::nullopt) const;

private:
    std::unordered_map<std::string, LedgerEntry> entries_;
};

} // namespace expense_manager

