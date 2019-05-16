from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import Job, Role, Site, Profile


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
