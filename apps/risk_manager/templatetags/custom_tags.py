import builtins

from django import template

register = template.Library()

@register.filter
def range(value, number):
    try:
        return builtins.range(int(number))  # Convert to integer
    except (ValueError, TypeError):
        return []