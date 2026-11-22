package expensemanager.employees;

import java.util.*;

public class EmployeeService {
    private final Map<String, Employee> employees = new HashMap<>();
    private final Map<String, Department> departments = new HashMap<>();

    public void registerEmployee(Employee employee) {
        employees.put(employee.getEmployeeId(), employee);
    }

    public void registerDepartment(Department department) {
        departments.put(department.getDeptId(), department);
    }

    public Optional<Employee> getEmployee(String employeeId) {
        return Optional.ofNullable(employees.get(employeeId));
    }

    public Optional<Department> getDepartment(String deptId) {
        return Optional.ofNullable(departments.get(deptId));
    }

    public List<Employee> getManagementChain(String startEmployeeId) {
        List<Employee> chain = new ArrayList<>();
        Optional<Employee> curr = getEmployee(startEmployeeId);
        Set<String> visited = new HashSet<>();

        while (curr.isPresent() && curr.get().getManagerId().isPresent() && !visited.contains(curr.get().getManagerId().get())) {
            String mgrId = curr.get().getManagerId().get();
            visited.add(mgrId);
            Optional<Employee> mgr = getEmployee(mgrId);
            if (mgr.isEmpty()) {
                break;
            }
            chain.add(mgr.get());
            curr = mgr;
        }

        return chain;
    }

    public List<String> getDepartmentHierarchy(String deptId) {
        List<String> hierarchy = new ArrayList<>();
        String currId = deptId;
        Set<String> visited = new HashSet<>();

        while (currId != null && !visited.contains(currId)) {
            visited.add(currId);
            hierarchy.add(currId);
            Optional<Department> dept = getDepartment(currId);
            currId = dept.flatMap(Department::getParentDeptId).orElse(null);
        }

        return hierarchy;
    }
}
