#pragma once

#include <string>
#include <vector>
#include "employees.hpp"
#include "currency.hpp"

namespace expense_manager {

struct ApprovalChain {
    std::vector<std::string> approvers;
    bool requires_finance_signoff{false};

    ApprovalChain() = default;
    ApprovalChain(std::vector<std::string> apps, bool req = false)
        : approvers(std::move(apps)), requires_finance_signoff(req) {}
};

class RoutingService {
public:
    explicit RoutingService(const EmployeeService& employee_service,
                           std::string finance_queue_id = "FINANCE_QUEUE");

    ApprovalChain build_approval_chain(const std::string& submitter_id,
                                      const Money& usd_amount) const;

private:
    const EmployeeService& employee_service_;
    std::string finance_queue_id_;
};

} // namespace expense_manager

