import re
from django import template

register = template.Library()

@register.filter
def regex_replace(value, arg):
    """
    Substitui com regex no template: {{ value|regex_replace:"pattern,replacement" }}
    """
    try:
        pattern, replacement = arg.split(',', 1)
        return re.sub(pattern, replacement, str(value))
    except ValueError:
        return value  # se não conseguir separar os 2 argumentos
