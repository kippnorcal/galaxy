from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import Role, Site, Profile


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

