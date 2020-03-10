from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import pytest

from high_health.models import EssentialQuestion


class TestEssentialQuestionModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.essentialquestion = EssentialQuestion.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.essentialquestion) == self.essentialquestion.name

    def test_name_max_length_100(self):
        with pytest.raises(ValidationError):
            self.essentialquestion.name = "x" * 101
            self.essentialquestion.full_clean()

    def test_description_can_be_blank(self):
        self.essentialquestion.description = None
        try:
            self.essentialquestion.full_clean()
        except ValidationError:
            pytest.fail("Blank description should not throw validation error")
