from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Favorite
from catalog.models import Category
from catalog.models import Report


class FavoriteModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.report = Report.objects.get(pk=1)
        self.favorite = Favorite.objects.create(
            user=self.user,
            report=self.report
        )

    def test_string_representation(self):
        self.assertEqual(str(self.favorite), '1')
        self.assertEqual(type(self.favorite.__str__()), str)

    def test_user_has_favorite(self):
        self.assertEqual(self.favorite.user, self.user)
        favorites = Report.objects.filter(favorite__user=self.user)
        self.assertIn(self.report, favorites)
