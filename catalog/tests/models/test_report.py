from django.test import TestCase
from django.core.exceptions import ValidationError
from catalog.models import Category, SubCategory, Report
from accounts.models import Role, Site
from django.contrib.auth.models import User


class ReportModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.report = Report.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.report), self.report.name)

    def test_name_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.report.name = 'x' * 256
            self.report.full_clean()

    def test_url_max_length_2000(self):
        with self.assertRaises(ValidationError):
            self.report.url = 'x' * 2001
            self.report.full_clean()

    def test_is_active_default_is_true(self):
        self.assertEqual(self.report.is_active, True)

    def test_is_embedded_default_is_true(self):
        self.assertEqual(self.report.is_embedded, True)

    def test_host_url_returns_correctly(self):
        host_url = 'https://tableau/'
        self.assertEqual(self.report.host_url(), host_url)

    def test_path_returns_correctly(self):
        path = '/site/Test/views/TestWorkbook/TestWorkSheet'
        self.assertEqual(self.report.path(), path)

    def test_embed_name_returns_correctly(self):
        embed_name = 'TestWorkbook/TestWorkSheet'
        self.assertEqual(self.report.embed_name(), embed_name)
        self.report.url = 'https://tableau/#/site/Test/views/TestWorkbook/TestWorkSheet'
        self.assertEqual(self.report.embed_name(), embed_name)

    def test_site_root_returns_correctly(self):
        site_root = '/t/Test'
        self.assertEqual(self.report.site_root(), site_root)

    def test_model_manager_queryset_returns_expected_results(self):
        expected = Report.objects.filter(is_active=True)
        actual = Report.active.all()
        self.assertEqual(actual.count(), expected.count())
        self.assertEqual(list(actual), list(expected))

    def test_model_manager_queryset_returns_expected_results(self):
        user = User.objects.get(pk=1)
        role = user.profile.job_title.role
        expected = Report.objects.filter(is_active=True, roles=role)
        actual = Report.active.for_user(user)
        self.assertEqual(actual.count(), expected.count())
        self.assertEqual(list(actual), list(expected))
