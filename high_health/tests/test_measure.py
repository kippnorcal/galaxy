import calendar
import datetime
from decimal import *

from django.core.exceptions import ValidationError
import pytest

from high_health.models import Goal, Measure, Metric
from accounts.models import Site


class TestMeasureModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.measure = Measure.objects.get(pk=1)

    def test_string_representation(self):
        expected = f"{self.measure.year}-{self.measure.month} {self.measure.school}: {self.measure.metric}"
        assert str(self.measure) == expected

    def test_value_max_digits_5(self):
        with pytest.raises(ValidationError):
            self.measure.value = Decimal("1000.00")
            self.measure.full_clean()

    def test_value_max_decimal_2(self):
        with pytest.raises(ValidationError):
            self.measure.value = Decimal("0.111")
            self.measure.full_clean()

    def test_value_can_be_null(self):
        self.measure.value = None
        try:
            self.measure.full_clean()
        except ValidationError:
            pytest.fail("Blank value should not throw validation error")

    def test_date_default_value(self):
        today = datetime.date.today()
        assert self.measure.date == today

    def test_is_current_default_value_is_true(self):
        measure = Measure()
        assert measure.is_current == True

    def test_measure_year_returns_date_year(self):
        self.measure.date = datetime.date.today()
        assert self.measure.year == self.measure.date.year

    def test_school_year_returns_expected_value(self):
        for month in range(1, 7):
            self.measure.date = datetime.date(2020, month, 1)
            assert self.measure.school_year == "19-20"
        for month in range(7, 13):
            self.measure.date = datetime.date(2019, month, 1)
            assert self.measure.school_year == "19-20"

    def test_measure_month_returns_date_month(self):
        self.measure.date = datetime.date.today()
        assert self.measure.month == self.measure.date.month

    def test_month_name_returns_expected_value(self):
        assert self.measure.month_name == calendar.month_abbr[self.measure.date.month]

    def test_goal_returns_expected_object(self):
        test_goal = Goal.objects.get(pk=1)
        test_goal.school = Site.objects.get(pk=1)
        test_goal.metric = Metric.objects.get(pk=1)
        test_goal.previous_outcome = Decimal("90.00")
        test_goal.target = Decimal("100.00")
        self.measure.school = Site.objects.get(pk=1)
        self.measure.metric = Metric.objects.get(pk=1)
        assert self.measure.goal == test_goal
