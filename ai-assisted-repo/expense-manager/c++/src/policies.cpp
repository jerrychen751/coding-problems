#include "expense_manager/policies.hpp"

namespace expense_manager {

PolicyService::PolicyService(const EmployeeService& employee_service)
    : employee_service_(employee_service) {}

void PolicyService::register_rule(const PolicyRule& rule) {
    rules_.push_back(rule);
}

PolicyEvaluation PolicyService::evaluate_policy(const std::string& /*department_id*/,
                                              ExpenseCategory category,
                                              const Money& usd_amount,
                                              std::optional<Role> /*role*/) const {
    for (const auto& rule : rules_) {
        if (!rule.department_id.has_value() && rule.category == category) {
            if (rule.max_amount_cents.has_value() && usd_amount.amount_cents < *rule.max_amount_cents) {
                return {rule.action, rule.rule_id};
            }
            return {PolicyAction::REQUIRE_APPROVAL, rule.rule_id};
        }
    }

    return {PolicyAction::REQUIRE_APPROVAL, std::nullopt};
}

} // namespace expense_manager
