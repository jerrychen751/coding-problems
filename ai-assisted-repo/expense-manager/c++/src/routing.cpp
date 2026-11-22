#include "expense_manager/routing.hpp"

namespace expense_manager {

RoutingService::RoutingService(const EmployeeService& employee_service,
                               std::string finance_queue_id)
    : employee_service_(employee_service),
      finance_queue_id_(std::move(finance_queue_id)) {}

ApprovalChain RoutingService::build_approval_chain(const std::string& submitter_id,
                                                   const Money& /*usd_amount*/) const {
    const Employee* emp = employee_service_.get_employee(submitter_id);
    if (emp && emp->manager_id.has_value()) {
        return ApprovalChain({*emp->manager_id});
    }
    return ApprovalChain({finance_queue_id_});
}

} // namespace expense_manager

