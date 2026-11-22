const { ApprovalChain } = require('./models');

class RoutingService {
  constructor(employeeService, financeQueueId = 'FINANCE_QUEUE') {
    this.employeeService = employeeService;
    this.financeQueueId = financeQueueId;
  }

  buildApprovalChain(submitterId, usdAmount) {
    const emp = this.employeeService.getEmployee(submitterId);
    if (emp && emp.managerId) {
      return new ApprovalChain([emp.managerId]);
    }
    return new ApprovalChain([this.financeQueueId]);
  }
}

module.exports = { RoutingService };

