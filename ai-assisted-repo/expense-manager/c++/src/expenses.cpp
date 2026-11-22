#include "expense_manager/expenses.hpp"
#include <stdexcept>

namespace expense_manager {

ExpenseService::ExpenseService(EmployeeService& employee_service,
                               FXService& fx_service,
                               PolicyService& policy_service,
                               RoutingService& routing_service,
                               LedgerService& ledger_service)
    : employee_service_(employee_service),
      fx_service_(fx_service),
      policy_service_(policy_service),
      routing_service_(routing_service),
      ledger_service_(ledger_service) {}

const ExpenseRecord* ExpenseService::get_expense_record(const std::string& expense_id) const {
    auto it = records_.find(expense_id);
    if (it != records_.end()) {
        return &it->second;
    }
    return nullptr;
}

ExpenseRecord ExpenseService::submit_expense(const Expense& expense) {
    const Employee* emp = employee_service_.get_employee(expense.employee_id);
    if (!emp || !emp->is_active) {
        ExpenseRecord record;
        record.expense = expense;
        record.status = ExpenseStatus::REJECTED;
        record.usd_amount = expense.amount;
        records_[expense.expense_id] = record;
        return record;
    }

    Money eval_amount = expense.amount;

    PolicyEvaluation evaluation = policy_service_.evaluate_policy(
        emp->department_id,
        expense.category,
        eval_amount,
        emp->role
    );

    ExpenseRecord record;
    record.expense = expense;
    record.usd_amount = eval_amount;
    record.matched_rule_id = evaluation.matched_rule_id;

    if (evaluation.action == PolicyAction::AUTO_APPROVE) {
        record.status = ExpenseStatus::APPROVED;
        ledger_service_.record_expense(
            expense.expense_id,
            emp->employee_id,
            emp->department_id,
            expense.category,
            eval_amount
        );
    } else if (evaluation.action == PolicyAction::REJECT) {
        record.status = ExpenseStatus::REJECTED;
    } else {
        ApprovalChain chain = routing_service_.build_approval_chain(
            expense.employee_id,
            eval_amount
        );
        record.status = ExpenseStatus::PENDING_APPROVAL;
        record.approver_chain = chain.approvers;
    }

    records_[expense.expense_id] = record;
    return record;
}

ExpenseRecord ExpenseService::approve_expense(const std::string& /*expense_id*/, const std::string& /*approver_id*/) {
    throw std::logic_error("Not implemented");
}

ExpenseRecord ExpenseService::reject_expense(const std::string& /*expense_id*/, const std::string& /*approver_id*/, const std::string& /*reason*/) {
    throw std::logic_error("Not implemented");
}

} // namespace expense_manager
