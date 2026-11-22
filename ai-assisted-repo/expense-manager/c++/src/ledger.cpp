#include "expense_manager/ledger.hpp"
#include <stdexcept>

namespace expense_manager {

static bool is_capex(ExpenseCategory cat) {
    return cat == ExpenseCategory::HARDWARE || cat == ExpenseCategory::SOFTWARE;
}

LedgerEntry LedgerService::record_expense(const std::string& expense_id,
                                          const std::string& employee_id,
                                          const std::string& department_id,
                                          ExpenseCategory category,
                                          const Money& usd_amount) {
    if (usd_amount.currency != Currency::USD) {
        throw std::invalid_argument("Ledger entries must be normalized to USD before posting.");
    }
    if (entries_.find(expense_id) != entries_.end()) {
        throw std::invalid_argument("Expense " + expense_id + " has already been posted to the ledger.");
    }

    SpendType st = is_capex(category) ? SpendType::CAPEX : SpendType::OPEX;
    LedgerEntry entry(expense_id, employee_id, department_id, category, st, usd_amount.amount_cents);
    entries_[expense_id] = entry;
    return entry;
}

int64_t LedgerService::get_total_by_category(ExpenseCategory category) const {
    int64_t total = 0;
    for (const auto& [id, entry] : entries_) {
        if (entry.category == category) {
            total += entry.usd_amount_cents;
        }
    }
    return total;
}

int64_t LedgerService::get_total_capex(const std::optional<std::string>& department_id) const {
    int64_t total = 0;
    for (const auto& [id, entry] : entries_) {
        if ((entry.spend_type == SpendType::CAPEX && !department_id.has_value()) || (department_id.has_value() && entry.department_id == *department_id)) {
            total += entry.usd_amount_cents;
        }
    }
    return total;
}

} // namespace expense_manager
