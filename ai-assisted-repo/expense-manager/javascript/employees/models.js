const Role = Object.freeze({
  IC: 'IC',
  MANAGER: 'MANAGER',
  DIRECTOR: 'DIRECTOR',
  VP: 'VP',
  C_LEVEL: 'C_LEVEL'
});

class Department {
  constructor(deptId, name, parentDeptId = null) {
    this.deptId = deptId;
    this.name = name;
    this.parentDeptId = parentDeptId;
    Object.freeze(this);
  }
}

class Employee {
  constructor(
    employeeId,
    name,
    departmentId,
    role = Role.IC,
    title = 'Software Engineer',
    managerId = null,
    isActive = true
  ) {
    this.employeeId = employeeId;
    this.name = name;
    this.departmentId = departmentId;
    this.role = role;
    this.title = title;
    this.managerId = managerId;
    this.isActive = isActive;
    Object.freeze(this);
  }
}

module.exports = {
  Role,
  Department,
  Employee
};

