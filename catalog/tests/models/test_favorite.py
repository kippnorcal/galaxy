from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Category, Favorite, Report
from accounts.models import Profile


class FavoriteModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)
        self.report = Report.objects.get(pk=1)
        self.favorite = Favorite.objects.create(
            profile=self.profile,
            report=self.report
        )
        self.favorite.save()

    def test_string_representation(self):
        self.assertEqual(str(self.favorite), 'some_user <3 Test Report 1')
        self.assertEqual(type(self.favorite.__str__()), str)

    def test_user_has_favorite(self):
        self.assertEqual(self.favorite.profile, self.profile)
        favorites = self.profile.favorites.all()
        self.assertIn(self.report, favorites)
