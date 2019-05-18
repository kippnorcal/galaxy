from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import Job, Role, Site, Profile
from catalog.models import Report, Favorite


class RoleModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.role = Role.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.role), self.role.name)

    def test_name_max_length_100(self):
        with self.assertRaises(ValidationError):
            self.role.name = 'x' * 101
            self.role.full_clean()

class JobModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.job = Job.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.job), self.job.name)


    def test_role_can_be_blank(self):
        self.job.role = None
        try:
            self.job.full_clean()
        except ValidationError:
            self.fail('Blank role should not throw validation error')

    def test_name_max_length_100(self):
        with self.assertRaises(ValidationError):
            self.job.name = 'x' * 101
            self.job.full_clean()

class SiteModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.site = Site.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.site), self.site.name)

    def test_name_max_length_100(self):
        with self.assertRaises(ValidationError):
            self.site.name = 'x' * 101
            self.site.full_clean()


class ProfileModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.report = Report.objects.get(pk=1)
        self.profile = Profile.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.profile), self.profile.email)

    def test_employee_number_max_length_5(self):
        with self.assertRaises(ValidationError):
            self.profile.employee_number = 'x' * 6
            self.profile.full_clean()

    def test_employee_number_can_be_blank(self):
        self.profile.employee_number = None
        try:
            self.profile.full_clean()
        except ValidationError:
            self.fail('Blank employee_number should not throw validation error')

    def test_avatar_url_max_length_5(self):
        with self.assertRaises(ValidationError):
            self.profile.avatar_url = 'x' * 2001
            self.profile.full_clean()

    def test_avatar_url_can_be_blank(self):
        self.profile.avatar_url = None
        try:
            self.profile.full_clean()
        except ValidationError:
            self.fail('Blank avatar_url should not throw validation error')

    def test_profile_linked_to_favorites(self):
        before_count = self.profile.favorites.all().count()
        favorite = Favorite(
            profile=self.profile,
            report=self.report
        )
        favorite.save()
        after_count = self.profile.favorites.all().count()
        self.assertNotEqual(before_count, after_count)
        del favorite


