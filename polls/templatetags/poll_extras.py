from django import template
from polls.models import Categories, Questions

register = template.Library()

@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag()
def tag_questions(category_slug=None):
    if category_slug and category_slug != 'all':
        return Questions.objects.filter(category__slug=category_slug)
    return Questions.objects.all()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
