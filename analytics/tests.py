from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PageView, Search, Login

class PageViewModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.pageview = PageView.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.pageview), self.pageview.page)

    def test_page_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.pageview.page = 'x' * 256
            self.pageview.full_clean()

    def test_timestamp_auto_set(self):
        pageview = PageView(
            user=self.user,
            page='test2/'
        )
        pageview.save()
        self.assertNotEqual(pageview.timestamp, None)

    def test_user_can_be_null(self):
        self.pageview.user = None
        try:
            self.pageview.full_clean()
        except ValidationError:
            self.fail('Null user should not throw validation error')


class SearchModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.search = Search.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.search), self.search.search_term)

    def test_user_can_be_null(self):
        self.search.user = None
        try:
            self.search.full_clean()
        except ValidationError:
            self.fail('Null user should not throw validation error')

    def test_search_term_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.search.search_term = 'x' * 256
            self.search.full_clean()

    def test_timestamp_auto_set(self):
        search = Search(
            user=self.user,
            search_term='test2'
        )
        search.save()
        self.assertNotEqual(search.search_timestamp, None)

    def test_destination_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.search.destination = 'x' * 256
            self.search.full_clean()

    def test_destination_can_be_null(self):
        self.search.destination = None
        try:
            self.search.full_clean()
        except ValidationError:
            self.fail('Null destination should not throw validation error')


    def test_click_through_timestamp_can_be_null(self):
        self.search.click_through_timestamp = None
        try:
            self.search.full_clean()
        except ValidationError:
            self.fail('Null click through timestamp should not throw validation error')


class LoginModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.login = Login.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.login), "some_user - 2019-07-01 00:00:00+00:00")

    def test_user_can_be_null(self):
        self.login.user = None
        try:
            self.login.full_clean()
        except ValidationError:
            self.fail('Null user should not throw validation error')

    def test_referrer_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.login.referrer = 'x' * 256
            self.login.full_clean()

    def test_user_agent_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.login.user_agent = 'x' * 256
            self.login.full_clean()

    def test_ip_address_max_length_255(self):
        with self.assertRaises(ValidationError):
            self.login.ip_address = 'x' * 256
            self.login.full_clean()

    def test_timestamp_auto_set(self):
        login = Login(user=self.user)
        login.save()
        self.assertNotEqual(login.timestamp, None)
