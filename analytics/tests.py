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
