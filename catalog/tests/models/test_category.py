from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from catalog.models import Category, SubCategory


class CategoryModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.category = Category.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_name_max_length_100(self):
        with self.assertRaises(ValidationError):
            self.category.name = 'x' * 101
            self.category.full_clean()

    def test_is_active_default_true(self):
        c = Category(name="Test Category 2")
        c.save()
        self.assertTrue(c.is_active)


class SubCategoryModelTest(TestCase):
    fixtures = ['testing']

    def setUp(self):
        self.sub_category = SubCategory.objects.get(pk=1)

    def test_string_representation(self):
        self.assertEqual(str(self.sub_category), self.sub_category.name)

    def test_name_max_length_100(self):
        with self.assertRaises(ValidationError):
            self.sub_category.name = 'x' * 101
            self.sub_category.full_clean()

    def test_is_active_default_true(self):
        category = Category.objects.get(pk=1)
        c = SubCategory(name="Test SubCategory 2", category=category)
        c.save()
        self.assertTrue(c.is_active)

    def test_category_fk_required(self):
        with self.assertRaises(ValidationError):
            self.sub_category.category = None
            self.sub_category.full_clean()
