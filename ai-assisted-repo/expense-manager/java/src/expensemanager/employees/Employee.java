package expensemanager.employees;

import java.util.Objects;
import java.util.Optional;

public class Employee {
    private final String employeeId;
    private final String name;
    private final String departmentId;
    private final Role role;
    private final String title;
    private final String managerId;
    private final boolean isActive;

    public Employee(String employeeId, String name, String departmentId) {
        this(employeeId, name, departmentId, Role.IC, "Software Engineer", null, true);
    }

    public Employee(String employeeId, String name, String departmentId, Role role) {
        this(employeeId, name, departmentId, role, "Software Engineer", null, true);
    }

    public Employee(String employeeId, String name, String departmentId, Role role, String managerId) {
        this(employeeId, name, departmentId, role, "Software Engineer", managerId, true);
    }

    public Employee(String employeeId, String name, String departmentId, Role role, String title, String managerId) {
        this(employeeId, name, departmentId, role, title, managerId, true);
    }

    public Employee(
        String employeeId,
        String name,
        String departmentId,
        Role role,
        String title,
        String managerId,
        boolean isActive
    ) {
        this.employeeId = Objects.requireNonNull(employeeId, "employeeId cannot be null");
        this.name = Objects.requireNonNull(name, "name cannot be null");
        this.departmentId = Objects.requireNonNull(departmentId, "departmentId cannot be null");
        this.role = role != null ? role : Role.IC;
        this.title = title != null ? title : "Software Engineer";
        this.managerId = managerId;
        this.isActive = isActive;
    }

    public String getEmployeeId() {
        return employeeId;
    }

    public String getName() {
        return name;
    }

    public String getDepartmentId() {
        return departmentId;
    }

    public Role getRole() {
        return role;
    }

    public String getTitle() {
        return title;
    }

    public Optional<String> getManagerId() {
        return Optional.ofNullable(managerId);
    }

    public boolean isActive() {
        return isActive;
    }
}

