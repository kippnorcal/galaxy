from django.core.exceptions import ValidationError
import pytest

from catalog.models import PublicStat


class TestPublicStatModel:
    @pytest.fixture(autouse=True)
    def setUp(self, db, django_db_setup):
        self.publicstat = PublicStat.objects.get(pk=1)

    def test_string_representation(self):
        assert str(self.publicstat) == f"{self.publicstat.metric}: {self.publicstat.value}" 

    def test_metric_max_length_255(self):
        with pytest.raises(ValidationError):
            self.publicstat.metric = "x" * 256
            self.publicstat.full_clean()
