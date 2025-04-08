from django import template

register = template.Library()

@register.filter
def status_color(value):
    value = value.lower() if value else ''
    if value == 'realizada':
        return 'success'
    elif value == 'pendente':
        return 'warning'
    elif value == 'nao_realizada':
        return 'danger'
    return 'secondary'

