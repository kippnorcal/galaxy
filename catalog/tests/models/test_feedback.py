from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import pytest

from catalog.models import Feedback
from catalog.models import Category
from catalog.models import Report


class TestFeedbackModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.user = User.objects.get(pk=1)
        self.report = Report.objects.get(pk=1)
        self.feedback = Feedback(
            user=self.user, report=self.report, score=5, comment="This is a comment"
        )

    def test_string_representation(self):
        feedback = self.feedback
        user = feedback.user.get_full_name()
        report = feedback.report
        assert str(feedback) == f"{report} -- {user}"

    def test_score_minimum(self):
        with pytest.raises(ValidationError):
            self.feedback.score = 0
            self.feedback.full_clean()

    def test_score_maximum(self):
        with pytest.raises(ValidationError):
            self.feedback.score = 6
            self.feedback.full_clean()

    def test_comments_can_be_blank(self):
        self.feedback.comment = ""
        try:
            self.feedback.full_clean()
        except ValidationError:
            pytest.fail("Blank comments should not raise validation error")

