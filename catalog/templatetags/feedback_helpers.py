from django import template

register = template.Library()


@register.filter
def sentiment(value):
    sentiments = {
        1: "very dissatisfied",
        2: "dissatisfied",
        3: "neutral",
        4: "satisfied",
        5: "very satisfied"
    }
    return sentiments.get(value)

@register.filter
def sentiment_icon(value):
    value = int(value)
    sentiments = {
        1: "fa-angry",
        2: "fa-frown",
        3: "fa-meh",
        4: "fa-grin-beam",
        5: "fa-grin-hearts"
    }
    return sentiments.get(value)

@register.filter
def sentiment_color(value):
    value = int(value)
    sentiments = {
        1: "text-danger",
        2: "text-warning",
        3: "text-secondary",
        4: "text-success",
        5: "text-primary"
    }
    return sentiments.get(value)

register.filter('sentiment', sentiment)
register.filter('sentiment_icon', sentiment_icon)
register.filter('sentiment_color', sentiment_color)

