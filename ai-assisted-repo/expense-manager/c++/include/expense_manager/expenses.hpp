#pragma once

#include <string>
#include <vector>
#include <optional>
#include <unordered_map>
#include <iostream>
#include "currency.hpp"
#include "employees.hpp"
#include "policies.hpp"
#include "routing.hpp"
#include "ledger.hpp"

namespace expense_manager {

enum class ExpenseStatus {
    APPROVED,
    PENDING_APPROVAL,
    REJECTED
};

inline std::ostream& operator<<(std::ostream& os, const ExpenseStatus& status) {
    switch (status) {
        case ExpenseStatus::APPROVED: return os << "APPROVED";
        case ExpenseStatus::PENDING_APPROVAL: return os << "PENDING_APPROVAL";
        case ExpenseStatus::REJECTED: return os << "REJECTED";
    }
    return os << "UNKNOWN";
}

struct Expense {
    std::string expense_id;
    std::string employee_id;
    Money amount;
    ExpenseCategory category;
    std::string merchant;

    Expense() = default;
    Expense(std::string id, std::string emp_id, Money amt, ExpenseCategory cat, std::string merch)
        : expense_id(std::move(id)), employee_id(std::move(emp_id)),
          amount(amt), category(cat), merchant(std::move(merch)) {}
};

struct ExpenseRecord {
    Expense expense;
    ExpenseStatus status{ExpenseStatus::PENDING_APPROVAL};
    Money usd_amount;
    std::optional<std::string> matched_rule_id;
    std::vector<std::string> approver_chain;
    int current_step{0};
    std::vector<std::pair<std::string, std::string>> approval_history;

    std::optional<std::string> current_required_approver() const {
        if (status != ExpenseStatus::PENDING_APPROVAL) {
            return std::nullopt;
        }
        if (current_step < static_cast<int>(approver_chain.size())) {
            return approver_chain[current_step];
        }
        return std::nullopt;
    }
};

class ExpenseService {
public:
    ExpenseService(EmployeeService& employee_service,
                   FXService& fx_service,
                   PolicyService& policy_service,
                   RoutingService& routing_service,
                   LedgerService& ledger_service);

    const ExpenseRecord* get_expense_record(const std::string& expense_id) const;
    ExpenseRecord submit_expense(const Expense& expense);
    ExpenseRecord approve_expense(const std::string& expense_id, const std::string& approver_id);
    ExpenseRecord reject_expense(const std::string& expense_id, const std::string& approver_id, const std::string& reason = "");

private:
    EmployeeService& employee_service_;
    [[maybe_unused]] FXService& fx_service_;
    PolicyService& policy_service_;
    RoutingService& routing_service_;
    LedgerService& ledger_service_;
    std::unordered_map<std::string, ExpenseRecord> records_;
};

} // namespace expense_manager
