from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from .utils import get_app_perms

TESTING = True

class SuperUserMixin(UserPassesTestMixin):
    # super_admin_permissions = [
    #     # list of permissions for superusers
    #     'authentication:add_user',
    #     'authentication:change_user',
    #     'authentication:delete_user',
    #     'authentication:add_department',
    #     'authentication:change_department',
    #     'authentication:delete_department',
    #     'authentication:add_globalsettings',
    #     'authentication:change_globalsettings',
    #     'authentication:delete_globalsettings',
    #     'authentication:view_globalsettings',
    # ]

    # if TESTING:
    #     # restrict all permissions to super_admins for testing
    #     super_admin_permissions = get_app_perms(
    #         'authentication',
    #         'risk_manager',
    #     )

    # view_permissions = []   # list of permissions needed for this view requires

    super_admin_only = False

    def test_func(self):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return False

        if self.super_admin_only:
            return self.request.user.is_super_admin  # Only allow if user is a super admin

        return True  # If the permission isn't restricted to super admins

    # def has_elevated_permissions(self):
    #     # Return's True if the user requires elevated actions for this view
    #     return bool([perm for perm in self.view_permissions if perm in self.super_admin_permissions])

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            # The user is logged in but doesn't have the required permissions
            return redirect('risk_register:page_403')

    def is_fetched_request(self, request):
        return request.headers.get('X-Requested-With') == 'XMLHttpRequest'