#pragma once

#include <string>
#include <vector>
#include <optional>
#include <unordered_map>
#include <iostream>

namespace expense_manager {

enum class Role {
    IC,
    MANAGER,
    DIRECTOR,
    VP,
    C_LEVEL
};

inline std::ostream& operator<<(std::ostream& os, const Role& role) {
    switch (role) {
        case Role::IC: return os << "Role::IC";
        case Role::MANAGER: return os << "Role::MANAGER";
        case Role::DIRECTOR: return os << "Role::DIRECTOR";
        case Role::VP: return os << "Role::VP";
        case Role::C_LEVEL: return os << "Role::C_LEVEL";
    }
    return os << "Role::UNKNOWN";
}

struct Department {
    std::string dept_id;
    std::string name;
    std::optional<std::string> parent_dept_id;

    Department() = default;
    Department(std::string id, std::string n, std::optional<std::string> p = std::nullopt)
        : dept_id(std::move(id)), name(std::move(n)), parent_dept_id(std::move(p)) {}
};

struct Employee {
    std::string employee_id;
    std::string name;
    std::string department_id;
    Role role{Role::IC};
    std::string title{"Software Engineer"};
    std::optional<std::string> manager_id;
    bool is_active{true};

    Employee() = default;
    Employee(std::string id, std::string n, std::string d, Role r = Role::IC,
             std::string t = "Software Engineer", std::optional<std::string> m = std::nullopt, bool active = true)
        : employee_id(std::move(id)), name(std::move(n)), department_id(std::move(d)),
          role(r), title(std::move(t)), manager_id(std::move(m)), is_active(active) {}
};

class EmployeeService {
public:
    void register_employee(const Employee& employee);
    void register_department(const Department& department);
    const Employee* get_employee(const std::string& employee_id) const;
    const Department* get_department(const std::string& dept_id) const;
    std::vector<Employee> get_management_chain(const std::string& start_employee_id) const;
    std::vector<std::string> get_department_hierarchy(const std::string& dept_id) const;

private:
    std::unordered_map<std::string, Employee> employees_;
    std::unordered_map<std::string, Department> departments_;
};

} // namespace expense_manager

