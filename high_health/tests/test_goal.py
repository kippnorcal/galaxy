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

    def test_goal_type_invalid(self):
        with pytest.raises(ValidationError):
            self.goal.goal_type = "Test"
            self.goal.full_clean()

    def test_previous_outcome_max_digits_5(self):
        with pytest.raises(ValidationError):
            self.goal.previous_outcome = 1000.00
            self.goal.full_clean()

    def test_previous_outcome_max_decimal_2(self):
        with pytest.raises(ValidationError):
            self.goal.previous_outcome = 0.111
            self.goal.full_clean()

    def test_target_max_digits_5(self):
        with pytest.raises(ValidationError):
            self.goal.target = 1000.00
            self.goal.full_clean()

    def test_target_max_decimal_2(self):
        with pytest.raises(ValidationError):
            self.goal.target = 0.111
            self.goal.full_clean()
