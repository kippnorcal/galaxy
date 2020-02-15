import pytest

from templatetags.feedback_helpers import sentiment, sentiment_icon, sentiment_color


class TestSentimentFilter:
    def test_sentiment_returns_expected_value(self):
        expected_sentiments = {
            1: "very dissatisfied",
            2: "dissatisfied",
            3: "neutral",
            4: "satisfied",
            5: "very satisfied",
        }
        for number, value in expected_sentiments.items():
            assert sentiment(number) == value

    def test_sentiment_accepts_input_greater_than_5(self):
        value = sentiment(6)
        assert value is None

    def test_sentiment_accepts_input_zero(self):
        value = sentiment(0)
        assert value is None


class TestSentimentIconFilter:
    def test_sentiment_icon_returns_expected_value(self):
        expected_sentiments = {
            1: "fa-angry",
            2: "fa-frown",
            3: "fa-meh",
            4: "fa-grin-beam",
            5: "fa-grin-hearts",
        }
        for number, value in expected_sentiments.items():
            assert sentiment_icon(number) == value

    def test_sentiment_icon_accepts_input_greater_than_5(self):
        value = sentiment_icon(6)
        assert value is None

    def test_sentiment_icon_accepts_input_zero(self):
        value = sentiment_icon(0)
        assert value is None

    def test_sentiment_icon_accepts_string_input(self):
        expected_sentiments = {
            "1": "fa-angry",
            "2": "fa-frown",
            "3": "fa-meh",
            "4": "fa-grin-beam",
            "5": "fa-grin-hearts",
        }
        for number, value in expected_sentiments.items():
            assert sentiment_icon(number) == value


class TestSentimentColorFilter:
    def test_sentiment_color_returns_expected_value(self):
        expected_sentiments = {
            1: "text-danger",
            2: "text-warning",
            3: "text-secondary",
            4: "text-success",
            5: "text-primary",
        }
        for number, value in expected_sentiments.items():
            assert sentiment_color(number) == value

    def test_sentiment_color_accepts_input_greater_than_5(self):
        value = sentiment_color(6)
        assert value is None

    def test_sentiment_color_accepts_input_zero(self):
        value = sentiment_color(0)
        assert value is None

    def test_sentiment_color_accepts_string_input(self):
        expected_sentiments = {
            "1": "text-danger",
            "2": "text-warning",
            "3": "text-secondary",
            "4": "text-success",
            "5": "text-primary",
        }
        for number, value in expected_sentiments.items():
            assert sentiment_color(number) == value
