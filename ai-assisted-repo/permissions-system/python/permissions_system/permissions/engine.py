from copy import deepcopy
from typing import Dict, Optional
from employees.service import EmployeeService
from supergroups.service import SupergroupService
from permissions.models import PermissionProfile, Action, AssigneeType, ScopeType


class PermissionService:
    def __init__(
        self,
        employee_service: EmployeeService,
        supergroup_service: SupergroupService,
        privilege_graph=None
    ):
        self.employee_service = employee_service
        self.supergroup_service = supergroup_service
        self.privilege_graph = privilege_graph
        self._profiles: Dict[str, PermissionProfile] = {}

    def upsert_profile(self, profile: PermissionProfile) -> None:
        self._profiles[profile.id] = profile
    
    def get_profile(self, profile_id: str) -> Optional[PermissionProfile]:
        profile = self._profiles.get(profile_id)
        if profile is None:
            return None
        return deepcopy(profile)

    def delete_profile(self, profile_id: str) -> None:
        self._profiles.pop(profile_id, None)

    def has_permission(
        self,
        subject_employee_id: str,
        action: Action,
        privilege: str,
        target_employee_id: str
    ) -> bool:
        if not self.employee_service.is_active(subject_employee_id):
            return False
        if not self.employee_service.is_active(target_employee_id):
            return False

        subject = self.employee_service.get_employee(subject_employee_id)
        target = self.employee_service.get_employee(target_employee_id)
        if subject.company_id != target.company_id:
            return False

        subject_groups = self.supergroup_service.get_user_groups(subject_employee_id)
        assigned_profiles = [
            p for p in self._profiles.values()
            if (p.assignee_type == "EMPLOYEE" and p.assignee_id == subject_employee_id)
            or (p.assignee_type == "GROUP" and p.assignee_id in subject_groups)
        ]

        for profile in assigned_profiles:
            if profile.scope.scope_type == ScopeType.NONE:
                continue
            if profile.scope.scope_type == ScopeType.TARGET_GROUP:
                target_members = self.supergroup_service.get_effective_members(profile.scope.target_group_id)
                if target_employee_id not in target_members:
                    continue

            for grant in profile.grants:
                if grant.privilege == privilege:
                    if grant.action.subsumes(action):
                        return True

        return False

