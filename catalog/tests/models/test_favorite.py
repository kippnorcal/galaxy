from django.contrib.auth.models import User
import pytest

from catalog.models import Category, Favorite, Report
from accounts.models import Profile


class TestFavoriteModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.profile = Profile.objects.get(pk=1)
        self.report = Report.objects.get(pk=1)
        self.favorite = Favorite.objects.create(
            profile=self.profile, report=self.report
        )
        self.favorite.save()

    def test_string_representation(self):
        assert str(self.favorite) == "some_user <3 Test Report 1"
        assert type(self.favorite.__str__()) == str

    def test_user_has_favorite(self):
        assert self.favorite.profile == self.profile
        favorites = self.profile.favorites.all()
        assert self.report in favorites
