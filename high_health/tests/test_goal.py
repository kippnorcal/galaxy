from decimal import *

from django.core.exceptions import ValidationError
import pytest

from high_health.models import Goal


class TestGoalModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.goal = Goal.objects.get(pk=1)

    def test_string_representation(self):
        expected = f"{self.goal.school} - {self.goal.metric}"
        assert str(self.goal) == expected

    def test_goal_type_allows_defined_choices(self):
        try:
            self.goal.goal_type = "ABOVE"
            self.goal.full_clean()
            self.goal.goal_type = "BELOW"
            self.goal.full_clean()
        except ValidationError:
            pytest.fail("Selecting defined choices should not throw validation error")

    def test_goal_type_does_not_allow_undefined_choice(self):
        with pytest.raises(ValidationError):
            self.goal.goal_type = "Test"
            self.goal.full_clean()

    def test_previous_outcome_max_digits_5(self):
        with pytest.raises(ValidationError):
            self.goal.previous_outcome = Decimal('9999.99')
            self.goal.full_clean()

    def test_previous_outcome_allows_up_to_5_digits(self):
        self.goal.previous_outcome = Decimal('9.99')
        self.goal.full_clean()
        self.goal.previous_outcome = Decimal('99.99')
        self.goal.full_clean()
        self.goal.previous_outcome = Decimal('999.99')
        self.goal.full_clean()

    def test_previous_outcome_max_decimal_2(self):
        with pytest.raises(ValidationError):
            self.goal.previous_outcome = Decimal('9.999')
            self.goal.full_clean()

    def test_previous_outcome_allows_up_to_2_decimal(self):
        self.goal.previous_outcome = Decimal('99.9')
        self.goal.full_clean()
        self.goal.previous_outcome = Decimal('99.99')
        self.goal.full_clean()

    def test_target_max_digits_5(self):
        with pytest.raises(ValidationError):
            self.goal.target = Decimal('9999.99')
            self.goal.full_clean()

    def test_target_allows_up_to_5_digits(self):
        self.goal.target = Decimal('9.99')
        self.goal.full_clean()
        self.goal.target = Decimal('99.99')
        self.goal.full_clean()
        self.goal.target = Decimal('999.99')
        self.goal.full_clean()

    def test_target_max_decimal_2(self):
        with pytest.raises(ValidationError):
            self.goal.target = Decimal('9.999')
            self.goal.full_clean()

    def test_target_allows_up_to_2_decimal(self):
        self.goal.target = Decimal('99.9')
        self.goal.full_clean()
        self.goal.target = Decimal('99.99')
        self.goal.full_clean()
