import pytest

from accounts.models import Site
from high_health.models import Measure, Metric, Goal
from templatetags.high_health_helpers import goal_format, addstr, goal_distance


class TestGoalFormat:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        # Ensure that this measure and this goal are associated with
        # each other by setting the metric and school to be the same
        metric = Metric.objects.get(pk=1)
        school = Site.objects.get(pk=1)
        self.goal = Goal.objects.get(metric=metric, school=school)
        self.goal.metric = metric
        self.goal.school = school
        self.measure = Measure.objects.get(pk=1)
        self.measure.metric = metric
        self.measure.school = school

    def test_goal_format_returns_expected_value_above_success(self):
        # value is greater than or equal to target
        self.goal.goal_type = "ABOVE"
        self.measure.value = 100
        self.goal.target = 90
        self.goal.save()
        assert goal_format(self.measure) == "success"

    def test_goal_format_returns_expected_value_above_secondary(self):
        # value is less than target but greater than or equal to previous outcome
        self.goal.goal_type = "ABOVE"
        self.measure.value = 80
        self.goal.target = 90
        self.goal.previous_outcome = 70
        self.goal.save()
        assert goal_format(self.measure) == "secondary"

    def test_goal_format_returns_expected_value_above_danger(self):
        # value is less than target and less than previous outcome
        self.goal.goal_type = "ABOVE"
        self.measure.value = 60
        self.goal.target = 90
        self.goal.previous_outcome = 70
        self.goal.save()
        assert goal_format(self.measure) == "danger"

    def test_goal_format_returns_expected_value_below_success(self):
        # value is less than or equal to target
        self.goal.goal_type = "BELOW"
        self.measure.value = 10
        self.goal.target = 20
        self.goal.save()
        assert goal_format(self.measure) == "success"

    def test_goal_format_returns_expected_value_below_secondary(self):
        # value is greater than target but less than or equal to previous outcome
        self.goal.goal_type = "BELOW"
        self.measure.value = 20
        self.goal.target = 10
        self.goal.previous_outcome = 30
        self.goal.save()
        assert goal_format(self.measure) == "secondary"

    def test_goal_format_returns_expected_value_below_danger(self):
        # value is greater than target and greater than previous outcome
        self.goal.goal_type = "BELOW"
        self.measure.value = 50
        self.goal.target = 10
        self.goal.previous_outcome = 30
        self.goal.save()
        assert goal_format(self.measure) == "danger"


class TestAddStr:
    def test_add_strings(self):
        value1 = "aaa"
        value2 = "bbb"
        expected = value1 + value2
        assert addstr(value1, value2) == expected


class TestGoalDistance:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        # Ensure that this measure and this goal are associated with
        # each other by setting the metric and school to be the same
        metric = Metric.objects.get(pk=1)
        school = Site.objects.get(pk=1)
        self.goal = Goal.objects.get(metric=metric, school=school)
        self.goal.metric = metric
        self.goal.school = school
        self.measure = Measure.objects.get(pk=1)
        self.measure.metric = metric
        self.measure.school = school

    def test_goal_distance_returns_expected_value_for_above_type(self):
        # value is less than target
        self.measure.value = 80
        self.goal.target = 90
        self.goal.save()
        expected = "-10.00% below goal"
        assert goal_distance(self.measure) == expected
        # value is greater than or equal to target
        self.measure.value = 100
        expected = "+10.00% above goal"
        assert goal_distance(self.measure) == expected

    def test_goal_distance_returns_expected_value_for_below_type(self):
        # value is greater than target
        self.measure.value = 30
        self.goal.target = 20
        self.goal.save()
        expected = "+10.00% above goal"
        assert goal_distance(self.measure) == expected
        # value is less than or equal to target
        self.measure.value = 10
        expected = "-10.00% below goal"
        assert goal_distance(self.measure) == expected
