from django.core.exceptions import ValidationError
import pytest

from catalog.models import Category, SubCategory, Report
from accounts.models import Role, Site
from django.contrib.auth.models import User


class TestReportModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.report = Report.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.report) == self.report.name

    def test_name_max_length_255(self):
        with pytest.raises(ValidationError):
            self.report.name = "x" * 256
            self.report.full_clean()

    def test_url_max_length_2000(self):
        with pytest.raises(ValidationError):
            self.report.url = "x" * 2001
            self.report.full_clean()

    def test_is_active_default_is_true(self):
        assert self.report.is_active == True

    def test_is_embedded_default_is_true(self):
        assert self.report.is_embedded == True

    def test_host_url_returns_correctly(self):
        host_url = "https://tableau/"
        assert self.report.host_url() == host_url

    def test_path_returns_correctly(self):
        path = "/site/Test/views/TestWorkbook/TestWorkSheet"
        assert self.report.path() == path

    def test_embed_name_returns_correctly(self):
        embed_name = "TestWorkbook/TestWorkSheet"
        assert self.report.embed_name() == embed_name
        self.report.url = "https://tableau/#/site/Test/views/TestWorkbook/TestWorkSheet"
        assert self.report.embed_name() == embed_name

    def test_site_root_returns_correctly(self):
        site_root = "/t/Test"
        assert self.report.site_root() == site_root

    def test_target_site_returns_correctly(self):
        target_site = "Test"
        assert self.report.target_site() == target_site

    def test_model_manager_queryset_returns_expected_results(self):
        expected = Report.objects.filter(is_active=True)
        actual = Report.active.all()
        assert actual.count() == expected.count()
        assert list(actual) == list(expected)

    def test_model_manager_queryset_for_user_returns_expected_results(self):
        user = User.objects.get(pk=1)
        role = user.profile.job_title.role
        expected = Report.objects.filter(is_active=True, roles=role)
        actual = Report.active.for_user(user)
        assert actual.count() == expected.count()
        assert list(actual) == list(expected)

    def test_report_clean_fails_when_category_does_not_match(self):
        self.report.subcategory.category = Category.objects.get(pk=1)
        self.report.category = Category.objects.get(pk=2)
        with pytest.raises(ValidationError):
            self.report.clean()

    def test_report_clean_succeeds_when_subcategory_is_none(self):
        self.report.subcategory = None
        try:
            self.report.clean()
        except ValidationError:
            pytest.fail("Blank subcategory should not raise validation error")

    def test_report_clean_succeeds_when_subcategory_matches(self):
        self.report.subcategory.category = Category.objects.get(pk=1)
        self.report.category = Category.objects.get(pk=1)
        try:
            self.report.clean()
        except ValidationError:
            pytest.fail("Matching subcategory's category should not raise validation error")