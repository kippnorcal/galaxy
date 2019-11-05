from django.core.exceptions import ValidationError
from django.db import IntegrityError
import pytest

from catalog.models import Category, SubCategory


class TestCategoryModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.category = Category.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.category) == self.category.name

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.category.name = "x" * 101
            self.category.full_clean()

    def test_is_active_default_true(self):
        c = Category(name="Test Category 2")
        c.save()
        assert c.is_active == True


class TestSubCategoryModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.sub_category = SubCategory.objects.get(pk=1)

    def test_string_representation(self):
        assert (
            str(self.sub_category)
            == f"{self.sub_category.category}: {self.sub_category.name}"
        )

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.sub_category.name = "x" * 101
            self.sub_category.full_clean()

    def test_is_active_default_true(self):
        category = Category.objects.get(pk=1)
        c = SubCategory(name="Test SubCategory 2", category=category)
        c.save()
        assert c.is_active == True

    def test_category_fk_required(self):
        with pytest.raises(ValidationError):
            self.sub_category.category = None
            self.sub_category.full_clean()
