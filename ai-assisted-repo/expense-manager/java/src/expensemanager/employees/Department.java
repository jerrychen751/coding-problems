package expensemanager.employees;

import java.util.Objects;
import java.util.Optional;

public class Department {
    private final String deptId;
    private final String name;
    private final String parentDeptId;

    public Department(String deptId, String name) {
        this(deptId, name, null);
    }

    public Department(String deptId, String name, String parentDeptId) {
        this.deptId = Objects.requireNonNull(deptId, "deptId cannot be null");
        this.name = Objects.requireNonNull(name, "name cannot be null");
        this.parentDeptId = parentDeptId;
    }

    public String getDeptId() {
        return deptId;
    }

    public String getName() {
        return name;
    }

    public Optional<String> getParentDeptId() {
        return Optional.ofNullable(parentDeptId);
    }
}

