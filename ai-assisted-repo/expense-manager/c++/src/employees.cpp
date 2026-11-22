#include "expense_manager/employees.hpp"
#include <unordered_set>

namespace expense_manager {

void EmployeeService::register_employee(const Employee& employee) {
    employees_[employee.employee_id] = employee;
}

void EmployeeService::register_department(const Department& department) {
    departments_[department.dept_id] = department;
}

const Employee* EmployeeService::get_employee(const std::string& employee_id) const {
    auto it = employees_.find(employee_id);
    if (it != employees_.end()) {
        return &it->second;
    }
    return nullptr;
}

const Department* EmployeeService::get_department(const std::string& dept_id) const {
    auto it = departments_.find(dept_id);
    if (it != departments_.end()) {
        return &it->second;
    }
    return nullptr;
}

std::vector<Employee> EmployeeService::get_management_chain(const std::string& start_employee_id) const {
    std::vector<Employee> chain;
    const Employee* curr = get_employee(start_employee_id);
    std::unordered_set<std::string> visited;

    while (curr && curr->manager_id.has_value() && visited.find(*curr->manager_id) == visited.end()) {
        visited.insert(*curr->manager_id);
        const Employee* mgr = get_employee(*curr->manager_id);
        if (!mgr) {
            break;
        }
        chain.push_back(*mgr);
        curr = mgr;
    }

    return chain;
}

std::vector<std::string> EmployeeService::get_department_hierarchy(const std::string& dept_id) const {
    std::vector<std::string> hierarchy;
    std::optional<std::string> curr_id = dept_id;
    std::unordered_set<std::string> visited;

    while (curr_id.has_value() && visited.find(*curr_id) == visited.end()) {
        visited.insert(*curr_id);
        hierarchy.push_back(*curr_id);
        const Department* dept = get_department(*curr_id);
        curr_id = dept ? dept->parent_dept_id : std::nullopt;
    }

    return hierarchy;
}

} // namespace expense_manager
