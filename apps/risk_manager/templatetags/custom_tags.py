import builtins

from django import template

register = template.Library()

@register.filter
def range(value, number):
    try:
        return builtins.range(int(number))  # Convert to integer
    except (ValueError, TypeError):
        return []


@register.filter
def trim(value, arg):
    """
    Trims the text to the specified number of characters and adds ellipses.
    Usage: {{ long_text|trim:"10" }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value  # Return the original value if arg is invalid

    if len(value) > length:
        return value[:length] + "..."
    return value