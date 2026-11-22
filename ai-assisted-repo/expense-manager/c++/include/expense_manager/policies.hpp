#pragma once

#include <string>
#include <vector>
#include <optional>
#include <iostream>
#include "employees.hpp"
#include "currency.hpp"

namespace expense_manager {

enum class ExpenseCategory {
    FOOD_AND_BEVERAGE,
    AIRFARE,
    LODGING,
    SOFTWARE,
    HARDWARE
};

inline std::ostream& operator<<(std::ostream& os, const ExpenseCategory& cat) {
    switch (cat) {
        case ExpenseCategory::FOOD_AND_BEVERAGE: return os << "FOOD_AND_BEVERAGE";
        case ExpenseCategory::AIRFARE: return os << "AIRFARE";
        case ExpenseCategory::LODGING: return os << "LODGING";
        case ExpenseCategory::SOFTWARE: return os << "SOFTWARE";
        case ExpenseCategory::HARDWARE: return os << "HARDWARE";
    }
    return os << "UNKNOWN";
}

enum class PolicyAction {
    AUTO_APPROVE,
    REQUIRE_APPROVAL,
    REJECT
};

inline std::ostream& operator<<(std::ostream& os, const PolicyAction& act) {
    switch (act) {
        case PolicyAction::AUTO_APPROVE: return os << "AUTO_APPROVE";
        case PolicyAction::REQUIRE_APPROVAL: return os << "REQUIRE_APPROVAL";
        case PolicyAction::REJECT: return os << "REJECT";
    }
    return os << "UNKNOWN";
}

struct PolicyRule {
    std::string rule_id;
    ExpenseCategory category;
    PolicyAction action{PolicyAction::AUTO_APPROVE};
    int priority{100};
    std::optional<std::string> department_id;
    std::optional<Role> role;
    std::optional<int64_t> max_amount_cents;
    std::optional<int64_t> min_amount_cents;

    PolicyRule() = default;
    PolicyRule(std::string id, ExpenseCategory cat, PolicyAction act = PolicyAction::AUTO_APPROVE,
               int prio = 100, std::optional<std::string> dept = std::nullopt,
               std::optional<Role> r = std::nullopt, std::optional<int64_t> max_c = std::nullopt,
               std::optional<int64_t> min_c = std::nullopt)
        : rule_id(std::move(id)), category(cat), action(act), priority(prio),
          department_id(std::move(dept)), role(r), max_amount_cents(max_c), min_amount_cents(min_c) {}
};

struct PolicyEvaluation {
    PolicyAction action;
    std::optional<std::string> matched_rule_id;
};

class PolicyService {
public:
    explicit PolicyService(const EmployeeService& employee_service);
    void register_rule(const PolicyRule& rule);
    PolicyEvaluation evaluate_policy(const std::string& department_id,
                                    ExpenseCategory category,
                                    const Money& usd_amount,
                                    std::optional<Role> role = std::nullopt) const;

private:
    [[maybe_unused]] const EmployeeService& employee_service_;
    std::vector<PolicyRule> rules_;
};

} // namespace expense_manager
