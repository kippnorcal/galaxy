import datetime

from django.core.exceptions import ValidationError
import pytest

from high_health.models import Metric, EssentialQuestion



class TestMetricModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.metric = Metric.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.metric) == self.metric.name

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.metric.name = "x" * 101
            self.metric.full_clean()

    def test_definition_can_be_blank(self):
        self.metric.definition = None
        try:
            self.metric.full_clean()
        except ValidationError:
            pytest.fail("Blank definition should not throw validation error")
    
    def test_essential_question_can_be_null(self):
        self.metric.essentialquestion = None
        try:
            self.metric.full_clean()
        except ValidationError:
            pytest.fail("Blank essential question should not throw validation error")

    def test_frequency_allows_defined_choices(self):
        try:
            self.metric.frequency = "MoM"
            self.metric.full_clean()
            self.metric.frequency = "YoY"
            self.metric.full_clean()
        except ValidationError:
            pytest.fail("Selecting defined choices should not throw validation error")

    def test_frequency_does_not_allow_undefined_choice(self):
        with pytest.raises(ValidationError):
            self.metric.frequency = "Test"
            self.metric.full_clean()

    def test_report_can_be_null(self):
        self.metric.report = None
        try:
            self.metric.full_clean()
        except ValidationError:
            pytest.fail("Blank report should not throw validation error")

    def test_year(self):
        today = datetime.date.today()
        assert self.metric.year == today.year