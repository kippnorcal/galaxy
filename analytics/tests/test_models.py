from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import pytest

from analytics.models import PageView, Search, Login
from catalog.models import Report

class TestPageViewModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.user = User.objects.get(pk=1)
        self.pageview = PageView.objects.get(pk=1)
        self.report = Report.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.pageview) == self.pageview.page

    def test_page_max_length_255(self):
        with pytest.raises(ValidationError):
            self.pageview.page = "x" * 256
            self.pageview.full_clean()

    def test_timestamp_auto_set(self):
        pageview = PageView(user=self.user, page="test2/")
        pageview.save()
        assert pageview.timestamp != None

    def test_user_can_be_null(self):
        self.pageview.user = None
        try:
            self.pageview.full_clean()
        except ValidationError:
            pytest.fail("Null user should not throw validation error")

    def test_page_obect(self):
        self.pageview.page = "/test/1"
        assert self.pageview.page_object == "test"

    def test_page_id(self):
        self.pageview.page = "/test/1"
        assert self.pageview.page_id == "1"

    def test_display_name_high_health(self):
        self.pageview.page = "/high_health/1"
        assert self.pageview.display_name == "High Health"

    def test_display_name_report(self):
        self.pageview.page = "/report/1"
        assert self.pageview.display_name == self.report.name

    def test_display_name_else(self):
        self.pageview.page = "/test_page/1"
        assert self.pageview.display_name == self.pageview.page


class TestSearchModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.user = User.objects.get(pk=1)
        self.search = Search.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.search) == self.search.search_term

    def test_user_can_be_null(self):
        self.search.user = None
        try:
            self.search.full_clean()
        except ValidationError:
            pytest.fail("Null user should not throw validation error")

    def test_search_term_max_length_255(self):
        with pytest.raises(ValidationError):
            self.search.search_term = "x" * 256
            self.search.full_clean()

    def test_timestamp_auto_set(self):
        search = Search(user=self.user, search_term="test2")
        search.save()
        assert search.search_timestamp != None

    def test_destination_max_length_255(self):
        with pytest.raises(ValidationError):
            self.search.destination = "x" * 256
            self.search.full_clean()

    def test_destination_can_be_null(self):
        self.search.destination = None
        try:
            self.search.full_clean()
        except ValidationError:
            pytest.fail("Null destination should not throw validation error")

    def test_click_through_timestamp_can_be_null(self):
        self.search.click_through_timestamp = None
        try:
            self.search.full_clean()
        except ValidationError:
            pytest.fail(
                "Null click through timestamp should not throw validation error"
            )


class TestLoginModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.user = User.objects.get(pk=1)
        self.login = Login.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.login) == "some_user - 2019-07-01 00:00:00+00:00"

    def test_user_can_be_null(self):
        self.login.user = None
        try:
            self.login.full_clean()
        except ValidationError:
            pytest.fail("Null user should not throw validation error")

    # Commented out because this out because this does not appear to be in the Login class
    # def test_referrer_max_length_255(self):
    #     with pytest.raises(ValidationError):
    #         self.login.referrer = "x" * 256
    #         self.login.full_clean()

    def test_user_agent_max_length_255(self):
        with pytest.raises(ValidationError):
            self.login.user_agent = "x" * 256
            self.login.full_clean()

    def test_ip_address_max_length_255(self):
        with pytest.raises(ValidationError):
            self.login.ip_address = "x" * 256
            self.login.full_clean()

    def test_timestamp_auto_set(self):
        login = Login(user=self.user)
        login.save()
        assert login.timestamp != None
