from django.core.exceptions import ValidationError
from django.db import IntegrityError
import pytest

from accounts.models import Job, Role, Site, Profile, SchoolLevel
from catalog.models import Report, Favorite


class TestRoleModel:
    @pytest.fixture(autouse=True)
    def setup(self, db, django_db_setup):
        self.role = Role.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.role) == self.role.name

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.role.name = "x" * 101
            self.role.full_clean()


class TestSchoolLevelModel:
    @pytest.fixture(autouse=True)
    def setup(self, db, django_db_setup):
        self.schoollevel = SchoolLevel.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.schoollevel) == self.schoollevel.name

    def test_name_max_length_2(self):
        with pytest.raises(ValidationError):
            self.schoollevel.name = "x" * 3
            self.schoollevel.full_clean()


class TestJobModel:
    @pytest.fixture(autouse=True)
    def setup(self, db, django_db_setup):
        self.job = Job.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.job) == self.job.name

    def test_role_can_be_blank(self):
        self.job.role = None
        try:
            self.job.full_clean()
        except ValidationError:
            pytest.fail("Blank role should not throw validation error")

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.job.name = "x" * 101
            self.job.full_clean()


class TestSiteModel:
    @pytest.fixture(autouse=True)
    def setup(self, db, django_db_setup):
        self.site = Site.objects.get(pk=1)

    def test_string_representation(self):
        str(self.site) == self.site.name

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.site.name = "x" * 101
            self.site.full_clean()


class TestProfileModel:
    @pytest.fixture(autouse=True)
    def setup(self, db, django_db_setup):
        self.report = Report.objects.get(pk=1)
        self.profile = Profile.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.profile) == self.profile.email

    def test_employee_number_max_length_5(self):
        with pytest.raises(ValidationError):
            self.profile.employee_number = "x" * 6
            self.profile.full_clean()

    def test_avatar_url_max_length_5(self):
        with pytest.raises(ValidationError):
            self.profile.avatar_url = "x" * 2001
            self.profile.full_clean()

    def test_avatar_url_can_be_blank(self):
        self.profile.avatar_url = None
        try:
            self.profile.full_clean()
        except ValidationError:
            pytest.fail("Blank avatar_url should not throw validation error")

    def test_profile_linked_to_favorites(self):
        before_count = self.profile.favorites.all().count()
        favorite = Favorite(profile=self.profile, report=self.report)
        favorite.save()
        after_count = self.profile.favorites.all().count()
        assert before_count != after_count
        del favorite

    def test_email_is_unique(self):
        existing_email = self.profile.email
        with pytest.raises(IntegrityError):
            profile = Profile(email=existing_email)
            profile.save()

    def test_employee_number_is_unique(self):
        existing_employee_number = self.profile.employee_number
        with pytest.raises(IntegrityError):
            profile = Profile(employee_number=existing_employee_number)
            profile.save()
