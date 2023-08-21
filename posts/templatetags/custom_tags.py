from django import template

register = template.Library()


@register.simple_tag
def display_stars(rating):
    if (rating == 1):
        return "⭐"
    elif (rating == 2):
        return "⭐⭐"
    elif (rating == 3):
        return "⭐⭐⭐"
    elif (rating == 4):
        return "⭐⭐⭐⭐"
    elif (rating == 5):
        return "⭐⭐⭐⭐⭐"


register.filter('display_stars', display_stars)

