import pytest

from django.contrib.auth.models import Group

from accounts.models import User, Profile
from templatetags.nav_helpers import check_high_health_permissions


class TestNavHighHealthFilter:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.user = User.objects.get(pk=1)
        self.profile = Profile.objects.get(pk=1)
        self.profile.user = self.user
        self.high_health_group, created = Group.objects.get_or_create(
            name="High Health"
        )
        self.site_admin_group, created = Group.objects.get_or_create(name="Site Admin")

    def test_user_with_high_health_group_has_access(self):
        self.high_health_group.user_set.add(self.user)
        assert check_high_health_permissions(self.user) == True

    def test_user_with_site_admin_group_has_access(self):
        self.site_admin_group.user_set.add(self.user)
        assert check_high_health_permissions(self.user) == True

    def test_user_with_high_health_role_has_access(self):
        self.profile.job_title.role.permission_groups.set([self.high_health_group])
        assert check_high_health_permissions(self.user) == True

    def test_user_site_with_admin_role_has_access(self):
        self.profile.job_title.role.permission_groups.set([self.site_admin_group])
        assert check_high_health_permissions(self.user) == True

    def test_user_without_groups_has_no_access(self):
        self.user.groups.clear()
        assert check_high_health_permissions(self.user) == False

    def test_user_without_role_groups_has_no_access(self):
        self.profile.job_title.role.permission_groups.clear()
        assert check_high_health_permissions(self.user) == False
