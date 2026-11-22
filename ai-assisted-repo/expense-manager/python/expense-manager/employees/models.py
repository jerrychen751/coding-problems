from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Role(Enum):
    IC = "IC"
    MANAGER = "MANAGER"
    DIRECTOR = "DIRECTOR"
    VP = "VP"
    C_LEVEL = "C_LEVEL"


@dataclass(frozen=True)
class Department:
    dept_id: str
    name: str
    parent_dept_id: Optional[str] = None


@dataclass(frozen=True)
class Employee:
    employee_id: str
    name: str
    department_id: str
    role: Role = Role.IC
    title: str = "Software Engineer"
    manager_id: Optional[str] = None
    is_active: bool = True