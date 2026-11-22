const { Department, Employee } = require('./models');

class EmployeeService {
  constructor() {
    this._employees = new Map();
    this._departments = new Map();
  }

  registerEmployee(employee) {
    this._employees.set(employee.employeeId, employee);
  }

  registerDepartment(department) {
    this._departments.set(department.deptId, department);
  }

  getEmployee(employeeId) {
    return this._employees.get(employeeId) || null;
  }

  getDepartment(deptId) {
    return this._departments.get(deptId) || null;
  }

  getManagementChain(startEmployeeId) {
    const chain = [];
    let curr = this.getEmployee(startEmployeeId);
    const visited = new Set();

    while (curr && curr.managerId && !visited.has(curr.managerId)) {
      visited.add(curr.managerId);
      const mgr = this.getEmployee(curr.managerId);
      if (!mgr) break;
      chain.push(mgr);
      curr = mgr;
    }

    return chain;
  }

  getDepartmentHierarchy(deptId) {
    const hierarchy = [];
    let currId = deptId;
    const visited = new Set();

    while (currId && !visited.has(currId)) {
      visited.add(currId);
      hierarchy.push(currId);
      const dept = this.getDepartment(currId);
      currId = dept ? dept.parentDeptId : null;
    }

    return hierarchy;
  }
}

module.exports = { EmployeeService };
